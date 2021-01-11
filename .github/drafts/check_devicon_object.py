from typing import List

# abandoned since it's not too hard to check devicon objects using our eyes
# however, still keep in case we need it in the future

def check_devicon_objects(icons: List[dict]):
    """
    Check that the devicon objects added is up to standard.
    """
    err_msgs = []
    for icon in icons:
        if type(icon["name"]) != str:
            err_msgs.append("'name' must be a string, not: " + str(icon["name"]))

        try:
            for tag in icon["tags"]:
                if type(tag) != str:
                    raise TypeError()
        except TypeError:
            err_msgs.append("'tags' must be an array of strings, not: " + str(icon["tags"]))
            break


        if type(icon["versions"]["svg"]) != list or len(icon["versions"]["svg"]) == 0:
            err_msgs.append("Icon name must be a string")
        
        if type(icon["versions"]["font"]) != list or len(icon["versions"]["svg"]) == 0:
            err_msgs.append("Icon name must be a string")

        if type(icon["color"]) != str or "#" not in icon["color"]:
            err_msgs.append("'color' must be a string in the format '#abcdef'")

        if type(icon["aliases"]) != list:
            err_msgs.append("'aliases' must be an array of dicts")
    
    if len(err_msgs) > 0:
        raise Exception("Error found in devicon.json: \n" + "\n".join(err_msgs))
