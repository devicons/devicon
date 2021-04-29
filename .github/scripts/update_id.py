from pathlib import Path

from build_assets.SvgIdUpdater import SvgIdUpdater


def main():
    # get all files
    # run the script for each file
    id_updater = SvgIdUpdater()
    id_updater.update_id(Path("./icons/elixir/elixir-test.svg"))
    id_updater.update_id(Path("./icons/ruby/ruby-test.svg"))


if __name__ == "__main__":
    main()
