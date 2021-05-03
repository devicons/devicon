import re
from pathlib import Path


class SvgIdUpdater:
    """
    Update an svg's id reference so it's unique among other
    svg files in this repo.
    """

    # look for anything that is between ` id="` and `"`
    id_declare_pattern = r"(?<= id=(\"|')).+?(?=(\"|'))"

    # look for anything that is between `"url(#` and `)"`
    id_use_pattern = r"(?<=\"url\(#).+?(?=\)\")"

    # pattern made up of both
    id_pattern = f"{id_declare_pattern}|{id_use_pattern}"

    def __init__(self):
        """
        The id generator that we will use throughout the process.
        """
        self.id_generator = None

        """
        Tracks the ids that we are swapping out.
        """
        self.old_to_new_ids_dict = None

        """
        The search reg exp that we will use to update the id.
        Can switch to other patterns if needed.
        """
        self.search_regexp = re.compile(SvgIdUpdater.id_pattern)



    def update_id(self, filepath: Path):
        """
        Update the ids inside an svg file.
        :return True if the file's id was changed. Else returns False.
        """
        self.reset(filepath.stem)

        with open(filepath, "r+") as file:
            print("Opening " + file.name)
            file_content = file.read()

            # stop early to save time from subbing and writing back to file
            if self.search_regexp.search(file_content) is None:
                print("No ids found. Ending function.")
                return False

            file.seek(0)
            file.write(self.search_regexp.sub(self.sub_id, file_content))  
            file.truncate()
            print("Finished substituting id.")
            return True


    def reset(self, filename: str):
        """
        Reset the instance variables for a new file.
        """
        self.id_generator = self.id_generator_setup(filename)
        self.old_to_new_ids_dict = {}


    def id_generator_setup(self, filename: str):
        """
        Set up the id generator with the new filename.
        :param filename - the file name without an extension/suffix.
        """
        num = 0
        while True:
            yield f"{filename}-{num}"
            num += 1


    def sub_id(self, match):
        """
        A 'callback' function that will return the appropriate
        new id for an id that was found.
        """
        old = match.group()
        try:
            # see if we already have an id for this
            new = self.old_to_new_ids_dict[old]
        except KeyError:
            # if not, make one
            new = next(self.id_generator)
            self.old_to_new_ids_dict[old] = new
        finally:
            return new
