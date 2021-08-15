from enum import Enum


class IcomoonOptionState(Enum):
    """
    The state of the Icomoon toolbar options
    """
    SELECT = 0,
    EDIT = 1


class IcomoonPage(Enum):
    """
    The available pages on the Icomoon website.
    """
    SELECTION = 0,
    GENERATE_FONT = 1


class IcomoonAlerts(Enum):
    """
    The alerts that Icomoon displayed to the user. There
    could be more but these are the ones we usually see.
    """
    STROKES_GET_IGNORED_WARNING = 0,
    REPLACE_OR_REIMPORT_ICON = 1,
    DESELECT_ICONS_CONTAINING_STROKES = 2,
    UNKNOWN = 3
