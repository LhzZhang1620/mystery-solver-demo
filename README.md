# The Midnight Chime

## Game Type

The Midnight Chime is a single-player desktop mystery game with a graphical user interface.

The player investigates six locations, collects evidence and witness statements, compares statements with independently verified facts, finds contradictions, and submits a final accusation. The game is implemented in Python with Tkinter and runs locally; it does not require a browser, database, network connection, or Node.js.

## Requirements for a Full Run

Keep the whole project directory intact and run the game from this directory. The application loads Python modules and image assets from relative project paths.

### Required Environment

- Python **3.10 or later**
- Python's built-in **Tkinter** GUI component, including Tcl/Tk
- Windows 10 or Windows 11 is the tested platform

The current development environment was verified with Python 3.13.5 and Tk 8.6.

### Runtime Packages

No third-party packages are required to run the game.

The runtime uses only Python standard-library modules:

- tkinter and ttk for the desktop interface
- pathlib for file paths
- dataclasses and typing for game state definitions
- copy for the bilingual case data

### Required Project Content

Do not remove the following while preparing a full version of the game:

- app.py, launcher.py, engine.py, and i18n.py
- the cases directory, including cases/night_clock.py
- the assets directory, including the UI images, six location images, and five character portraits

If an image is missing, the game can still open and shows a fallback label. Keeping all assets is required for the intended visual experience.

## Run on Windows with PowerShell

Open PowerShell and run the following commands:

~~~powershell
Set-Location D:\desk\9001\mystery-solver-demo
py --version
py -c "import tkinter as tk; print(f'tkinter {tk.TkVersion}')"
py app.py
~~~

The last command opens the Case Files window. Select **Open Case 01** to start playing.

If the py command is unavailable, replace py with the installed python command.

## Optional Development Package

Pillow is needed only when regenerating placeholder image assets with tools/generate_placeholder_assets.py. It is not needed to play the game.

~~~powershell
py -m pip install Pillow
~~~

Do not run the placeholder-image generator over finished artwork unless you intend to replace the current location images.

## Tkinter Troubleshooting

If the Tkinter check fails, reinstall Python with the **Tcl/Tk** option enabled.

On Debian or Ubuntu, install the system Tkinter package before running the game:

~~~bash
sudo apt install python3-tk
~~~
