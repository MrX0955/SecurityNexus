import os

def clear():
    """
    Clears the terminal screen. Uses 'cls' command for Windows and 'clear' for other systems.
    """
    os.system("cls" if os.name == "nt" else "clear") 