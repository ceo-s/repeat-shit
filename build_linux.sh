pyinstaller --distpath repeat_shit --add-data="assets:assets" -F --contents-directory . --hidden-import PIL._tkinter_finder main.py
tar -zcvf linux-build.tar.gz repeat_shit