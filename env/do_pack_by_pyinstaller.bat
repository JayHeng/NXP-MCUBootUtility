pyinstaller.exe pyinstaller_pack_f.spec
copy .\dist\NXP-MCUBootUtility.exe ..\bin
rd /q /s .\build
rd /q /s .\dist