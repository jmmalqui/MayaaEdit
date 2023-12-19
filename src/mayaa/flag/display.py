import enum


class DisplayMode(enum.IntEnum):
    Vertical = enum.auto()
    """
    Stacks each UIOBject vertically
    """
    Horizontal = enum.auto()
    """
    Stacks each UIOBject horizontally
    """
