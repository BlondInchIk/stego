# setup.py

from cx_Freeze import setup, Executable

include_files = ['S-UNIWARD.py']  # Добавление второго файла в сборку

setup(
    name="MyProgram",
    version="1.0",
    options={"build_exe": {"include_files": include_files}},
    executables=[Executable("main.py", base=None, icon="icon.ico")]
)
