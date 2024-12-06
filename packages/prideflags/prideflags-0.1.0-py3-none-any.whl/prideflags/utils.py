def color256(col, bg_fg):
    """
    Generates a 256-color ANSI escape code.
    :param col: Color code (0-255)
    :param bg_fg: 'bg' for background, 'fg' for foreground
    :return: ANSI escape code as a string
    """
    return f'\033[{48 if bg_fg == "bg" else 38};5;{col}m'
