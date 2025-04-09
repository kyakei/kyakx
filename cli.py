#!/usr/bin/env python3

import os
import sys

# Add the project root directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import functions from the kyakx module
from kyakx.core.banner import funky_loading
from kyakx.core.loader import loading_animation
from kyakx.core.main_menu import main_menu

def main():
    funky_loading()
    loading_animation()
    main_menu()

if __name__ == "__main__":
    main()