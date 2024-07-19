from cx_Freeze import setup, Executable

# Define the main script of your application
script = "main.py"

# Define additional options if necessary
build_exe_options = {
    "packages": ["keyboard"],
    "excludes": ["cx_Freeze", "cx_Logging", "lief", "setuptools", "wheel"],
    "include_files": ["ui.py", "minesweeper.py"]
}

# Setup configuration
setup(
    name="quantum-minesweeper",
    version="0.2",
    description="A terminal-based Minesweeper game.",
    options={"build_exe": build_exe_options},
    executables=[Executable(script, base=None)]
)
