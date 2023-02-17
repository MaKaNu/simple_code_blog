from argparse import ArgumentParser
import os
from pathlib import Path
from typing import Dict, Tuple


def main():
    parser = ArgumentParser(description="Simple Background Designer")
    parser.add_argument(
        '-f', '--file',
        default='test.txt',
        help='Textfile with data to embed in bg.'
    )
    parser.add_argument(
        '-s', '--scheme',
        default='dracula',
        help='Selected Scheme for Highlights.'
    )

    args = parser.parse_args()

    selected_scheme = get_color_scheme(args.scheme)
    loaded_text = load_text(Path(args.file))
    encoded_text = encode_text(loaded_text)
    print_encoded_text(encoded_text, selected_scheme)


def get_color_scheme(scheme:str = "dracula") -> Dict[str,str]:
    supported_schemes = ["dracula", "neon-vommit"]
    if scheme not in supported_schemes:
        raise NameError(f"Theme {scheme} is not supported yet!")
    
    schemes = dict()

    # Source: https://draculatheme.com/contribute
    schemes["dracula"] = {
        "bg": "#282a36",
        "fg": "#f8f8f2",
        "cyan": "#8be9fd",
        "green": "#50fa7b",
        "orange": "#ffb86c",
        "pink": "#ff79c6",
        "purple": "#bd93f9",
        "red": "#ff5555",
        "yellow": "#f1fa8c"
    }

    # Source: https://github.com/ghgofort/vscode-neon-vommit-theme/blob/master/themes/NeonVommitTheme.json
    schemes["neon-vommit"] = {
        "bg": "#222222",
        "fg": "#f0f0f0",
        "cyan": "#4499FF",
        "green": "#76EE00",
        "orange": "#FD971F",
        "pink": "#FF00AA",
        "purple": "#CC33FF",
        "red": "#f44747",
        "yellow": "#FFFF00"
    }

    return schemes[scheme]

def load_text(textfile:Path) -> str:
    if not textfile.exists():
        raise FileNotFoundError(f"File {textfile} not found!")
    with open(textfile) as file:
        data = file.read()
        return data

def encode_text(data:str):
    binary_list = [bin(ord(char))[2:] for char in data]
    binary_data = ''.join(binary_list)
    return binary_data

def print_encoded_text(data: str, scheme: Dict[str,str]) -> None:
    terminal_size = os.get_terminal_size()
    total_num_of_chars = terminal_size.columns * terminal_size.lines
    for _ in range(terminal_size.lines):
        print(color_text("EASY", scheme["red"], scheme["bg"],))

def color_text(text:str,
               rgb: str,
               rgb_bg: str) -> str:
    r, g, b = convert_web_to_rgb(rgb)
    r2, g2, b2 = convert_web_to_rgb(rgb_bg)
    return f"\033[38;2;{r};{g};{b};48;2;{r2};{g2};{b2}m{text}\033[0m"

def convert_web_to_rgb(color: str) -> Tuple[int, int, int]:
    rgb = color.lstrip("#")
    return (int(rgb[0:2],16),int(rgb[2:4],16), int(rgb[4:6],16))




if __name__ == "__main__":
    main()