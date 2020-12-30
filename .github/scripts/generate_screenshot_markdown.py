from typing import List
import json

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
    args = arg_getters.get_generate_markdown_args()
    print(args.img_urls)
    img_urls_list = json.loads(args.img_urls)
    markdown = generate_screenshot_markdown(img_urls_list)
    print("\n\n".join(markdown))  # format it before printing
