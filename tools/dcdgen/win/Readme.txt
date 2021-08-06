================
The dcdgen.exe is a tool to convert the .cfg file to a binary file and/or a c-style array file. The tool needs a .cfg file as input that contains all commands to be converted into DCD data block. The bin file will be used as DCD data file when generating boot image. The c file contains an c-style array of DCD data that can be used in c code directly.

================
Terms of Use:
This program can accepte two or three parameters  
    - inputfile=xxx.cfg, xxx.cfg is the name of converted file 
    - bout Convert to binary file 
    - cout convert to C file 
The parameter of filename must be entered. The output will be based on -bout and/or -cout. 

================
For example:
"dcdgen -inputfile=dcd_sdram_166MHz.cfg -bout -cout",the tool will output both CFG_DCD.bin and CFG_DCD.c;

"dcdgen -inputfile=dcd_sdram_166MHz.cfg -bout", the tool will output CFG_DCD.bin only;

"dcdgen -inputfile=dcd_sdram_166MHz.cfg -cout", the tool will output CFG_DCD.c only.


Note: Remember to switch path to the current directory or add where dcdgen.exe locates into PATH environment variables