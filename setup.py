# setup.py

from cx_Freeze import setup, Executable

include_files = ['S-UNIWARD.py', 'icon.ico', 'stego.png']

# http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Stego",                  # Name that will be show on the link
     "TARGETDIR",              # Component_
     "[TARGETDIR]main.exe",    # Target exe to exexute
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

msi_data = {"Shortcut": shortcut_table}

bdist_msi_options = {'data': msi_data}

setup(
    name="Stego",
    version="1.0",
    description='App for steganopraphy',
    options={"build_exe": {"include_files": include_files, 'include_msvcr': True,}, "bdist_msi": bdist_msi_options,},
    executables=[Executable("main.py", 
                            base='Win32GUI', 
                            icon="icon.ico",
                            shortcut_name='Stego',
                            shortcut_dir='DesktopFolder'),
                            ]
)
