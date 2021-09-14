@echo off

call C:\Users\dasss\miniconda3\Scripts\activate.bat C:\Users\dasss\Desktop\my_project\env
set KMP_DUPLICATE_LIB_OK=TRUE
python abhilipi.py
call conda deactivate
