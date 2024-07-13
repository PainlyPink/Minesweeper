from cx_Freeze import setup, Executable

# Define the main script of your application
script = "main.py"  # Replace with the name of your main Python file

# Define additional options if necessary
build_exe_options = {
    "packages": ["keyboard"],  # List any additional packages your project requires
    "excludes": ["cx_Freeze", "cx_Logging", "lief", "setuptools", "wheel"],  # List any packages you want to exclude
    "include_files": ["ui.py", "minesweeper.py"]  # Add ui.py to the included files
}

# Setup configuration
setup(
    name="not-minesweeper",  # Replace with your project name
    version="0.1",
    description="A terminal-based Minesweeper game.",  # Description of your project
    options={"build_exe": build_exe_options},
    executables=[Executable(script, base=None)],  # base=None is for console applications
)
