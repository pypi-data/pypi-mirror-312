from colorama import just_fix_windows_console
from random import randint

just_fix_windows_console()

class Color:
    RED =        f"\u001b[38;5;{1}m"
    ORANGE =     f"\u001b[38;5;{166}m"
    YELLOW =     f"\u001b[38;5;{11}m"
    GREEN =      f"\u001b[38;5;{34}m"
    DARK_GREEN = f"\u001b[38;5;{64}m"
    TURQUOISE =  f"\u001b[38;5;{30}m"
    BLUE =       f"\u001b[38;5;{39}m"
    DARK_BLUE =  f"\u001b[38;5;{20}m"
    PINK =       f"\u001b[38;5;{210}m"
    PURPLE =     f"\u001b[38;5;{125}m"
    VIOLET =     f"\u001b[38;5;{55}m"
    BROWN =      f"\u001b[38;5;{94}m"
    WHITE =      f"\u001b[38;5;{255}m"
    LIGHT_GRAY = f"\u001b[38;5;{243}m"
    GRAY =       f"\u001b[38;5;{239}m"
    BLACK =      f"\u001b[38;5;{16}m"
    RESET = 	 f"\u001b[0m"

    def __new__(self, ANSICode = randint(0, 255)) -> str: return f"\u001b[38;5;{ANSICode}m"

class BgColor:
    RED =        f"\u001b[48;5;{1}m"
    ORANGE =     f"\u001b[48;5;{166}m"
    YELLOW =     f"\u001b[48;5;{11}m"
    GREEN =      f"\u001b[48;5;{34}m"
    DARK_GREEN = f"\u001b[48;5;{64}m"
    TURQUOISE =  f"\u001b[48;5;{30}m"
    BLUE =       f"\u001b[48;5;{39}m"
    DARK_BLUE =  f"\u001b[48;5;{20}m"
    PINK =       f"\u001b[48;5;{210}m"
    PURPLE =     f"\u001b[48;5;{125}m"
    VIOLET =     f"\u001b[48;5;{55}m"
    BROWN =      f"\u001b[48;5;{94}m"
    WHITE =      f"\u001b[48;5;{255}m"
    LIGHT_GRAY = f"\u001b[48;5;{243}m"
    GRAY =       f"\u001b[48;5;{239}m"
    BLACK =      f"\u001b[48;5;{16}m"
    RESET = 	 f"\u001b[0m"

    def __new__(ANSICode = randint(0, 255)) -> str: return f"\u001b[48;5;{ANSICode}m"
        

def coloring(keywords: dict, string: str):
    words = string.split()
    return_string = f''

    for word in keywords:
        match word:
            case '__all__':   return keywords[word] + string
            case '__start__': return keywords[word] + string[:1] + "\u001b[0m" + string[1:]
            case '__end__':   return string[:-1] + keywords[word] + string[-1:] + "\u001b[0m"
            case '__mid__':   i = len(string) // 2; return string[:i] + keywords[word] + string[i] + "\u001b[0m" + string[i + 1:] if len(string) % 2 == 1 else string[:i - 1] + keywords[word] + string[i - 1:i + 1] + "\u001b[0m" + string[i + 1:]

    for word in words:
        if word in keywords.keys():
            return_string += f'{keywords[word]}{word}\u001b[0m '
        else:
            return_string += f'{word} '

    return return_string