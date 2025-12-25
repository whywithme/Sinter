import sys
import os
import shutil
import zipfile
import tempfile
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
                             QFileDialog, QLabel, QHeaderView, QMessageBox, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette

class SinterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_archive = None
        
        self.setWindowTitle("Sinter Archiver")
        self.resize(800, 500)
        self.apply_modern_theme()
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(10, 10, 10, 10)

        # === Панель инструментов ===
        toolbar_layout = QHBoxLayout()
        self.btn_new = self.create_button("✨ Новый", self.new_archive)
        self.btn_open = self.create_button("📂 Открыть", self.open_archive_dialog)
        self.btn_add = self.create_button("➕ Добавить файл", self.add_file_to_archive)
        self.btn_extract = self.create_button("⬇️ Извлечь всё", self.extract_all)
        
        toolbar_layout.addWidget(self.btn_new)
        toolbar_layout.addWidget(self.btn_open)
        toolbar_layout.addSpacing(20)
        toolbar_layout.addWidget(self.btn_add)
        toolbar_layout.addWidget(self.btn_extract)
        toolbar_layout.addStretch()
        
        self.lbl_status = QLabel("Нет открытого архива")
        self.lbl_status.setStyleSheet("color: #aaaaaa; font-weight: bold;")
        toolbar_layout.addWidget(self.lbl_status)

        layout.addLayout(toolbar_layout)

        # === Таблица ===
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Имя файла", "Размер (сжат)", "Размер (исх)"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #353535;
                color: #ffffff;
                padding: 5px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #4a90e2;
            }
        """)
        layout.addWidget(self.table)

        self.toggle_buttons(False)

    def apply_modern_theme(self):
        QApplication.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        QApplication.setPalette(palette)

    def create_button(self, text, func):
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(func)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d; 
                color: white; 
                padding: 8px 15px; 
                border-radius: 4px;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
                border-color: #777;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
            QPushButton:disabled {
                background-color: #2d2d2d;
                color: #777;
                border: 1px solid #333;
            }
        """)
        return btn

    def toggle_buttons(self, enabled):
        self.btn_add.setEnabled(enabled)
        self.btn_extract.setEnabled(enabled)

    # === ЛОГИКА ===

    def new_archive(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Создать архив", "", "Sinter Archive (*.sntr);;Zip Archive (*.zip)"
        )
        if file_path:
            try:
                # Создаем валидный пустой ZIP-файл
                with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    pass 
                self.load_archive(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось создать архив:\n{e}")

    def open_archive_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть архив", "", "Archives (*.sntr *.zip)"
        )
        if file_path:
            self.load_archive(file_path)

    def load_archive(self, path):
        if not zipfile.is_zipfile(path):
            QMessageBox.warning(self, "Ошибка", "Файл поврежден или не является архивом.")
            return

        self.current_archive = path
        self.lbl_status.setText(f"Открыт: {os.path.basename(path)}")
        self.toggle_buttons(True)
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        try:
            with zipfile.ZipFile(self.current_archive, 'r') as zf:
                infos = zf.infolist()
                self.table.setRowCount(len(infos))
                for row, info in enumerate(infos):
                    self.table.setItem(row, 0, QTableWidgetItem(info.filename))
                    self.table.setItem(row, 1, QTableWidgetItem(self.format_size(info.compress_size)))
                    self.table.setItem(row, 2, QTableWidgetItem(self.format_size(info.file_size)))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось прочитать архив:\n{e}")

    def add_file_to_archive(self):
        if not self.current_archive:
            return
        
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы для добавления")
        if not files:
            return

        # ИСПОЛЬЗУЕМ БЕЗОПАСНЫЙ МЕТОД СОХРАНЕНИЯ ЧЕРЕЗ ВРЕМЕННЫЙ ФАЙЛ
        # Это предотвращает ошибки дозаписи и повреждение архива
        try:
            temp_dir = tempfile.mkdtemp()
            temp_zip_path = os.path.join(temp_dir, 'temp_archive.zip')
            
            # Список имен новых файлов (чтобы не дублировать, если они уже есть)
            new_filenames = [os.path.basename(f) for f in files]

            with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as temp_zip:
                # 1. Сначала копируем все СТАРЫЕ файлы из текущего архива
                # (кроме тех, которые мы хотим перезаписать)
                if os.path.exists(self.current_archive) and zipfile.is_zipfile(self.current_archive):
                    with zipfile.ZipFile(self.current_archive, 'r') as old_zip:
                        for item in old_zip.infolist():
                            if item.filename not in new_filenames:
                                data = old_zip.read(item.filename)
                                temp_zip.writestr(item, data)
                
                # 2. Теперь добавляем НОВЫЕ файлы
                for f in files:
                    arcname = os.path.basename(f)
                    temp_zip.write(f, arcname)
            
            # 3. Заменяем старый архив новым
            shutil.move(temp_zip_path, self.current_archive)
            
            # 4. Убираем мусор
            shutil.rmtree(temp_dir)

            self.refresh_table()
            QMessageBox.information(self, "Успех", "Файлы успешно сохранены!")
            
        except PermissionError:
            QMessageBox.critical(self, "Ошибка доступа", "Нет прав на запись в этот файл. \nПопробуйте сохранить архив в другую папку (например, Документы).")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файлы:\n{e}")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def extract_all(self):
        if not self.current_archive:
            return

        dest_dir = QFileDialog.getExistingDirectory(self, "Куда распаковать?")
        if dest_dir:
            try:
                with zipfile.ZipFile(self.current_archive, 'r') as zf:
                    zf.extractall(dest_dir)
                QMessageBox.information(self, "Успех", f"Распаковано в:\n{dest_dir}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось распаковать:\n{e}")

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SinterApp()
    
    # Поддержка открытия файла по двойному клику
    if len(sys.argv) > 1:
        file_to_open = sys.argv[1]
        if os.path.exists(file_to_open) and (file_to_open.endswith('.sntr') or file_to_open.endswith('.zip')):
            window.load_archive(file_to_open)
            
    window.show()
    sys.exit(app.exec())