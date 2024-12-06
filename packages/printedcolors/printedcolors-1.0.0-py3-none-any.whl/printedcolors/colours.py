class ColourClass:
    # ANSI escape codes for text colors
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        yellow = '\033[33m'
        blue = '\033[34m'
        magenta = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        lightyellow = '\033[93m'
        lightblue = '\033[94m'
        lightmagenta = '\033[95m'
        lightcyan = '\033[96m'

    # ANSI escape codes for background colors
    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        yellow = '\033[43m'
        blue = '\033[44m'
        magenta = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

    # ANSI escape codes for styles
    bold = '\033[01m'
    dim = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    # Reset code to revert back to default terminal color
    reset = '\033[0m'

Colour = ColourClass()