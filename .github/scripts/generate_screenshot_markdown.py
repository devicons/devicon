from typing import List
import json
import os

from build_assets import arg_getters


def generate_screenshot_markdown(img_urls: List[str]):
    """
    Generate the markdown for the screenshots using the
    img_urls then print it to the console.
    :param img_urls are valid image links.
    """
    template = "![Detailed Screenshot]({})"
    return [template.format(img_url) for img_url in img_urls]


if __name__ == "__main__":
    img_urls_list = json.loads(os.environ["IMG_URLS"])
    markdown = generate_screenshot_markdown(img_urls_list)
    os.environ["DETAILED_IMGS_MARKDOWN"] = "\n\n".join(markdown)
    print(os.environ["DETAILED_IMGS_MARKDOWN"])

