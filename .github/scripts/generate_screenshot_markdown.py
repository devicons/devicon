import json
import os


if __name__ == "__main__":
    img_urls_list = json.loads(os.environ["IMG_URLS"])
    template = "![Detailed Screenshot]({})"
    markdown = [template.format(img_url) for img_url in img_urls_list]
    print("\n\n".join(markdown))

