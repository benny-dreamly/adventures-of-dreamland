from cx_Freeze import setup, Executable
import os

# Add any files or assets your game needs (images, sounds, etc.)
include_files = ['res/', 'save_game.json']  # Include necessary resource folders/files

# Define base as "Win32GUI" if you're building for Windows and don't want a command window
base = None
if os.name == 'nt':
    base = 'Win32GUI'  # Use 'Console' for console-based apps

executables = [
    Executable('adventures-of-dreamland.py', base=base)
]

# Setup configuration
setup(
    name='Adventures of Dreamland',
    version='1.0',
    description='A game where you help Benny escape!',
    options={
        'build_exe': {
            'packages': ['tkinter', 'PIL'],  # Include any additional packages your game needs
            'include_files': include_files  # Include the game resources
        }
    },
    executables=executables
)
