from setuptools import setup, find_packages

setup(
    name="quantum-minesweeper",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "keyboard",
    ],
    entry_points={
        "console_scripts": [
            "quantum-minesweeper=main:main",
        ],
    },
    package_data={
        # Include additional files like ui.py and minesweeper.py
        '': ['ui.py', 'minesweeper.py'],
    },
)
