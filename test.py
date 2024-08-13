import ctypes
import ctypes.util

# Загружаем библиотеку GTK
libgtk = ctypes.CDLL(ctypes.util.find_library('gtk-3'))

# Инициализация GTK
libgtk.gtk_init(None, None)

# Создаем окно выбора файла
libgtk.gtk_file_chooser_dialog_new.restype = ctypes.c_void_p
dialog = libgtk.gtk_file_chooser_dialog_new(
    b"Choose a file", None,
    0,  # GTK_FILE_CHOOSER_ACTION_OPEN
    b"_Cancel", 1,  # GTK_RESPONSE_CANCEL
    b"_Open", 0  # GTK_RESPONSE_OK
)

# Отображаем диалог
libgtk.gtk_widget_show_all(dialog)

# Получаем ответ пользователя
response = libgtk.gtk_dialog_run(dialog)

# Обработка ответа пользователя
if response == 0:  # GTK_RESPONSE_OK
  libgtk.gtk_file_chooser_get_filename.restype = ctypes.c_char_p
  filename = libgtk.gtk_file_chooser_get_filename(dialog)
  print(f"Выбранный файл: {filename.decode('utf-8')}")

# Уничтожаем диалог
libgtk.gtk_widget_destroy(dialog)
