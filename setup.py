from cx_Freeze import setup, Executable
import os

# Add any files or assets your game needs (images, sounds, etc.)
include_files = ['res/']  # Include necessary resource folders/files

# Determine the base for the executable
base = None
if os.name == 'nt':
    base = 'Win32GUI'  # Use 'Console' for console-based apps on Windows
elif os.name == 'posix':
    base = 'Console'  # Generally leave as Console for macOS and Linux

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
