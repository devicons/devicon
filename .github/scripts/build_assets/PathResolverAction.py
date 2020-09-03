import argparse
from pathlib import Path


class PathResolverAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        path = Path(values).resolve()
        if not path.exists():
            raise ValueError(f"{path} doesn't exist.")

        if self.dest == "icons_folder_path":
            if not path.is_dir():
                raise ValueError("icons_folder_path must be a directory")
            
        elif self.dest == "download_path":
            if not path.is_dir():
                raise ValueError("download_path must be a directory")

        setattr(namespace, self.dest, str(path))
