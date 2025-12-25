import sys
import os
import ctypes
import winreg
import shutil

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def register_extension(exe_path, icon_path):
    # Названия ключей реестра
    ext = ".sntr"
    file_type_name = "Sinter.Archive"
    
    try:
        # 1. Ассоциируем расширение .sntr с типом файла Sinter.Archive
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ext) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, file_type_name)

        # 2. Создаем описание типа файла
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, file_type_name) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Архив Sinter")

        # 3. Устанавливаем иконку (та самая желтая S)
        # Windows берет иконку по этому пути
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{file_type_name}\\DefaultIcon") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'"{icon_path}"')

        # 4. Указываем команду для открытия (запуск нашего exe с передачей пути к файлу)
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{file_type_name}\\shell\\open\\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'"{exe_path}" "%1"')

        # Обновляем кэш иконок Windows, чтобы изменения применились сразу
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0, 0, 0)
        
        print("Успешно!")
        print(f"Программа: {exe_path}")
        print(f"Иконка: {icon_path}")
        input("\nНажмите Enter, чтобы выйти...")

    except Exception as e:
        print(f"Ошибка при записи в реестр: {e}")
        input("\nНажмите Enter...")

if __name__ == "__main__":
    # Получаем полные пути к текущему exe и иконке
    current_dir = os.getcwd()
    exe_path = os.path.join(current_dir, "Sinter.exe")
    icon_path = os.path.join(current_dir, "icon.ico")

    if not os.path.exists(exe_path):
        print("Ошибка: Файл Sinter.exe не найден рядом со скриптом!")
        input()
        sys.exit()

    if not os.path.exists(icon_path):
        print("Ошибка: Файл icon.ico не найден рядом со скриптом! Скопируйте его сюда.")
        input()
        sys.exit()

    # Проверка прав администратора (нужны для записи в реестр)
    if is_admin():
        register_extension(exe_path, icon_path)
    else:
        # Перезапуск скрипта с правами админа
        print("Запрос прав администратора...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)