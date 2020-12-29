from typing import List


def generate_screenshot_markdown(img_urls: List[str]):
    """
    Generate the markdown for the screenshots using the
    img_urls then print it to the console.
    :param img_urls are valid image links.
    """
    template = "![Detailed Screenshot]({})"
    return [template.format(img_url) for img_url in img_urls]


if __name__ == "__main__":
    markdown = generate_screenshot_markdown()
    print("\n\n".join(markdown))  # format it before printing
