import PyInstaller.__main__

options = [
    "main.py",
    "--onefile",
    "--name",
    "Flappy Dappy",
    "--distpath",
    "fappy_dappy_exefile_home"
]

PyInstaller.__main__.run(options)