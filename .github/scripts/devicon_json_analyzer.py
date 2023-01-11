import json
import os
import re
from math import isclose
from pprint import pprint
from typing import Any, Dict

import click
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from tqdm import tqdm

DEVICON_JSON_PATH = "devicon.json"
GECKO_DRIVER_PATH = ".github/scripts/build_assets/geckodriver"

# Functions
## Utility functions
def update_issues(key: str, value: Any, issues: dict):
    """Utility function to update dictionary or add new key."""
    if key in issues:
        issues[key].update(value)
    else:
        issues[key] = value


def get_all_version_refs(icon: dict):
    """Utility function to get all the version references of an icon."""
    versions = icon["versions"]["svg"].copy()
    versions.extend(icon["versions"]["font"])
    return set(versions)


def get_icon_filename(icons_dir, icon_name, version):
    if os.path.exists(f"{icons_dir}/{icon_name}"):
        filename = f"{icons_dir}/{icon_name}/{icon_name}-{version}.svg"
    else:
        filename = f"{icons_dir}/{icon_name}-{version}.svg"
    return filename


def read_icon_svg(icons_dir: str, icon_name: str, version: str):
    filename = get_icon_filename(icons_dir, icon_name, version)
    with open(filename, "r") as svg_file:
        svg_content = svg_file.read()
    return svg_content


def get_webdriver(gecko_driver_path):
    service = Service(executable_path=gecko_driver_path)
    options = Options()
    options.headless = True
    return webdriver.Firefox(service=service, options=options)


def get_bbox(driver, svg_path):
    """
    Get the bounding box of an svg file.
    Couldn't find a reliable Python SVG library for Python so I used Selenium.
    """
    path = os.path.abspath(svg_path)
    driver.get(f"file://{path}")
    return driver.execute_script("return document.rootElement.getBBox();")


def get_svg_file_versions(icons_dir: str, icon_name: str):
    """Get all the svg versions of an icon given its name."""
    if os.path.exists(f"{icons_dir}/{icon_name}"):
        # If the icons_dir is the root icons dir
        svg_filenames = [
            fn for fn in os.listdir(f"{icons_dir}/{icon_name}") if fn.endswith(".svg")
        ]
    else:
        # if this is the directory for a single technology
        svg_filenames = [
            fn for fn in os.listdir(f"{icons_dir}/") if fn.endswith(".svg")
        ]
    return list(
        map(lambda fn: re.sub(rf"{icon_name}-(.+)\.svg", r"\1", fn), svg_filenames)
    )


def sort_json(icons: list):
    """Sort the json files contents."""
    icons = sorted(icons, key=lambda k: k["name"])
    for icon in icons:
        icon["versions"]["svg"] = sorted(icon["versions"]["svg"])
        icon["versions"]["font"] = sorted(icon["versions"]["font"])
        icon["aliases"] = sorted(icon["aliases"], key=lambda k: k["base"])
        icon["tags"] = sorted(icon["tags"])


## Process Step Functions
def fix_svg_versions(icon: dict, svg_versions: list, issues: dict = {}):
    """Fix missing and extra `svg` versions in devicon.json for an icon."""
    missing_versions = []
    extra_versions = []
    for svg_version in svg_versions:
        if svg_version not in icon["versions"]["svg"]:
            missing_versions.append(svg_version)

    for ref in icon["versions"]["svg"]:
        if ref not in svg_versions:
            extra_versions.append(ref)

    # Update the icon's versions.
    icon["versions"]["svg"] = [
        version for version in icon["versions"]["svg"] if version not in extra_versions
    ]
    icon["versions"]["svg"].extend(missing_versions)
    icon["versions"]["svg"] = sorted(icon["versions"]["svg"])

    if len(missing_versions) > 0:
        update_issues(icon["name"], {"missing_svg_versions": missing_versions}, issues)

    if len(extra_versions) > 0:
        update_issues(icon["name"], {"extra_svg_versions": extra_versions}, issues)

    return icon


def remove_extra_font_references(icon: dict, issues: dict = {}):
    """Checks for extra reference(s) in versions.svg[] and removes them."""
    extra_versions = []
    for ref in icon["versions"]["font"]:
        if ref not in icon["versions"]["svg"]:
            extra_versions.append(ref)

    icon["versions"]["font"] = [
        version for version in icon["versions"]["font"] if version not in extra_versions
    ]

    if len(extra_versions) > 0:
        update_issues(icon["name"], {"extra_font_versions": extra_versions}, issues)
    return icon


def fix_aliases(icon: dict, issues: dict = {}):
    """Fix swapped references in aliases and remove redundant aliases."""
    if len(icon["aliases"]) > 0:
        versions = get_all_version_refs(icon)
        missing_base = list(
            filter(lambda f: f["base"] not in versions, icon["aliases"])
        )
        repeated_alias = list(filter(lambda f: f["alias"] in versions, icon["aliases"]))

        new_aliases = []
        redundant_aliases = []
        # Check for swapped references in aliases.
        if len(missing_base) > 0 and len(repeated_alias) > 0:
            for svg_version in missing_base:
                icon["aliases"].remove(svg_version)
                icon["aliases"].append(
                    {"base": svg_version["alias"], "alias": svg_version["base"]}
                )
                new_aliases.append(
                    {"base": svg_version["alias"], "alias": svg_version["base"]}
                )
        # Check for unnecessary aliases.
        elif len(repeated_alias) > 0:
            for svg_version in repeated_alias:
                redundant_aliases.append(svg_version)
                icon["aliases"].remove(svg_version)

        if len(new_aliases) > 0:
            update_issues(icon["name"], {"new_aliases": new_aliases}, issues)

        if len(redundant_aliases) > 0:
            update_issues(
                icon["name"], {"redundant_aliases": redundant_aliases}, issues
            )

    return icon


def remove_multicolor_font_versions(icons_dir: str, icon: dict, issues: dict = {}):
    """
    Remove multicolor font versions from devicon.json.

    Note: Currently it does not remove anything it just reports it.
    """
    multicolor_versions = []
    for version in icon["versions"]["font"]:
        svg_content = read_icon_svg(icons_dir, icon["name"], version)
        colors = re.findall(r"fill=\"[#]([A-Fa-f0-9]{6})\"", svg_content)
        colors = [color.lower() for color in colors]
        unique_colors = set(colors)
        if len(unique_colors) > 1 or re.search(r"[gG]radient", svg_content):
            multicolor_versions.append(version)
            # TODO: Ask the team if theses versions should be removed.
            # icon["versions"]["font"].remove(version)

    if len(multicolor_versions) > 0:
        update_issues(
            icon["name"], {"multicolor_font_version": multicolor_versions}, issues
        )
    return icon


def check_view_port(icons_dir: str, icon: dict, issues: dict):
    """Check if the view port is set to 0 0 128 128"""
    bad_view_port = []
    for version in icon["versions"]["svg"]:
        svg_content = read_icon_svg(icons_dir, icon["name"], version)
        if not re.search(r"viewBox=\"0 0 128 128\"", svg_content):
            bad_view_port.append(version)

    if len(bad_view_port) > 0:
        update_issues(icon["name"], {"bad_view_port": bad_view_port}, issues)


def check_icon_bbox(icons_dir, icon: dict, issues: dict, driver):
    """Check if the maximum height and width of the icon is 128."""
    larger = []
    smaller = []
    for version in icon["versions"]["svg"]:
        filename = get_icon_filename(icons_dir, icon["name"], version)
        bbox = get_bbox(driver, filename)
        if bbox["width"] > 128.0 or bbox["height"] > 128.0:
            larger.append(version)
            continue

        width_in_tol = isclose(bbox["width"], 128.0, abs_tol=2.0)
        height_in_tol = isclose(bbox["height"], 128.0, abs_tol=2.0)
        if not width_in_tol and not height_in_tol:
            smaller.append(version)

    if len(larger) > 0:
        update_issues(icon["name"], {"larger_bbox": larger}, issues)

    if len(smaller) > 0:
        update_issues(icon["name"], {"smaller_bbox": smaller}, issues)


def generate_markdown_report(issues: dict):
    """Generate a markdown report of the issues."""
    report = ""
    for icon_name, icon_issues in issues.items():
        report += f"## {icon_name}\n"
        for issue_type, issue in icon_issues.items():
            report += f"  - {issue_type}\n"
            for issue in issue:
                report += f"    - {issue}\n"
        report += "\n"

    with open("report.md", "w") as report_file:
        report_file.write(report)


@click.option("--update-json", "-u", is_flag=True, help="Update devicon.json file.")
@click.option("--print-issues", "-p", is_flag=True, help="Print issues.")
@click.option("--generate-report", "-g", is_flag=True, help="Generate markdown report.")
@click.option(
    "--check-bbox",
    "-b",
    is_flag=True,
    default=False,
    help="Check the bounding box. This requires a selenium driver and it's a slow process",
)
@click.option(
    "--devicon-json-path",
    "-d",
    default=DEVICON_JSON_PATH,
    help="Path to devicon.json file.",
)
@click.option(
    "--gecko-driver-path",
    "-g",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default=GECKO_DRIVER_PATH,
    help="Path to gecko driver.",
)
@click.argument(
    "icons_dir",
    type=click.Path(exists=True, file_okay=False),
    default="icons/",
)
@click.command(
    help="Analyze devicon.json file.\n\nThe default ICONS_DIR is `icons/` which contains all icons. When running for a PR a single-technology directory can be selected instead."
)
def main(
    icons_dir: str,
    devicon_json_path: str,
    update_json: bool,
    print_issues: bool,
    generate_report: bool,
    check_bbox: bool,
    gecko_driver_path: str,
):
    with open(devicon_json_path) as devicon_json_file:
        devicon_json = json.load(devicon_json_file)

    issues: Dict[Any, Any] = {}
    for i, icon in enumerate(tqdm(devicon_json)):
        if not any(
            [
                True if filesindir.startswith(icon["name"]) else False
                for filesindir in os.listdir(icons_dir)
            ]
        ):
            continue

        # Get existing icon versions
        svg_file_versions = get_svg_file_versions(icons_dir, icon["name"])

        # Fix missing and extra `svg` versions in devicon.json for an icon.
        icon = fix_svg_versions(icon, svg_file_versions, issues)
        devicon_json[i] = icon

        # Check for extra reference(s) in versions.svg[]
        icon = remove_extra_font_references(icon, issues)
        devicon_json[i] = icon

        # Fix swapped references in aliases and remove redundant aliases.
        icon = fix_aliases(icon, issues)
        devicon_json[i] = icon

        # Remove multicolor font versions from devicon.json.
        icon = remove_multicolor_font_versions(icons_dir, icon, issues)
        devicon_json[i] = icon

        # Check if the view port is set to 0 0 128 128
        check_view_port(icons_dir, icon, issues)

        # Check Bounding Box
        if check_bbox:
            with get_webdriver(gecko_driver_path) as driver:
                check_icon_bbox(icons_dir, icon, issues, driver)

    if print_issues:
        pprint(issues)

    if generate_report:
        generate_markdown_report(issues)

    if update_json:
        sort_json(devicon_json)
        with open(devicon_json_path, "w") as devicon_json_file:
            json.dump(devicon_json, devicon_json_file, indent=4)


if __name__ == "__main__":
    main()
