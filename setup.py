from setuptools import setup, find_packages

setup(
    name="minesweeper-v",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "keyboard",
    ],
    entry_points={
        "console_scripts": [
            "not_minesweeper=main:main",
        ],
    },
)
