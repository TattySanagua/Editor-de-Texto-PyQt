from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QLabel, QWidget, QPushButton, QFontDialog,
                             QVBoxLayout, QMessageBox, QTextEdit, QInputDialog, QFileDialog, QColorDialog)
from PyQt5.QtGui import QFont, QIcon, QTextCursor, QColor
from PyQt5.QtCore import Qt
import sys

class Editor(QMainWindow):

    def __init__(self):
        super(Editor, self).__init__()
        self.resize(400,500)
        self.setWindowTitle("Editor de Texto")
        self.widgets()
        self.menu()

    def widgets(self):
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
    def menu(self):
        #ARCHIVO
        new_action = QAction(QIcon("new.png"), "Nuevo", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.clear_text)

        open_action = QAction(QIcon("open.png"), "Abrir", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)

        save_action = QAction(QIcon("save.png"), "Guardar", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)

        exit_action = QAction(QIcon("exit.png"), "Salir", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        #EDICION DE TEXTO
        undo_action = QAction(QIcon("undo.png"), "Deshacer", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.text_edit.undo)

        redo_action = QAction(QIcon("redo.png"), "Rehacer", self)
        redo_action.setShortcut("Ctrl+Shift+Z")
        redo_action.triggered.connect(self.text_edit.redo)

        cut_action = QAction(QIcon("cut.png"), "Cortar", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.text_edit.cut)

        copy_action = QAction(QIcon("copy.png"), "Copiar", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.text_edit.copy)

        paste_action = QAction(QIcon("paste.png"), "Pegar", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.text_edit.paste)

        find_action = QAction(QIcon("find.png"), "Buscar", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.find_action)

        #HERRAMIENTAS
        font_action = QAction(QIcon("font.png"), "Fuente", self)
        font_action.setShortcut("Ctrl+T")
        font_action.triggered.connect(self.choose_font)

        color_action = QAction(QIcon("color.png"), "Color", self)
        color_action.setShortcut("Ctrl+Shift+C")
        color_action.triggered.connect(self.choose_color)

        highlight_action = QAction(QIcon("highlight.png"), "Remarcar", self)
        highlight_action.setShortcut("Ctrl+Shift+H")
        highlight_action.triggered.connect(self.choose_background_color)

        #AYUDA
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.about_dialog)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Archivo")
        file_menu.addAction(new_action)
        file_menu.addSeparator()
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        edit_menu = menu_bar.addMenu("Edición")
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(cut_action)
        edit_menu.addSeparator()
        edit_menu.addAction(find_action)

        tools_menu = menu_bar.addMenu("Herramientas")
        tools_menu.addAction(font_action)
        tools_menu.addAction(color_action)
        tools_menu.addAction(highlight_action)

        help_menu = menu_bar.addMenu("Ayuda")
        help_menu.addAction(about_action)

    def clear_text(self):
        answer = QMessageBox.question(self, "Nuevo archivo", "Estas seguro que quieres crear un nuevo archivo?", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if answer == QMessageBox.Yes:
            self.text_edit.clear()
        else:
            pass

    def open_file(self):

        try:
            name, ext = QFileDialog.getOpenFileName(self, "Abrir archivo", "",
                                                    "HTML (*.html);; Archivo de Texto (*.txt)")

            if name:
                with open(name, "r") as f:
                    texto = f.read()
                    self.text_edit.setText(texto)
            else:
                QMessageBox.information(self, "Error", "No es posible abrir este archivo", QMessageBox.Ok)

        except:
            QMessageBox.information(self, "Error", "No es posible abrir este archivo", QMessageBox.Ok)

    def save_file(self):
        name, ext = QFileDialog.getSaveFileName(self, "Guardar Archivo", "", "HTML (*.html);; Archivo de Texto (*.txt)")

        if name.endswith(".txt"):
            texto = self.text_edit.toPlainText()
            with open(name, "w") as f:
                f.write(texto)
        elif name.endwith(".html"):
            texto = self.text_edit.toHtml()
            with open(name, "w") as f:
                f.write(texto)

    def find_action(self):
        buscador, _ = QInputDialog.getText(self, "Buscar Texto", "Texto")
        selecciones = []

        if _ and not self.text_edit.isReadOnly():
            self.text_edit.moveCursor(QTextCursor.Start)
            color = QColor(Qt.yellow)

            while (self.text_edit.find(buscador)):
                seleccion = QTextEdit.ExtraSelection()
                seleccion.format.setBackground(color)

                seleccion.cursor = self.text_edit.textCursor()

                selecciones.append(seleccion)

        for i in selecciones:
            self.text_edit.setExtraSelections(selecciones)

    def choose_font(self):
        actual = self.text_edit.currentFont()
        fondo, ok = QFontDialog.getFont(actual, self)

        if ok:
            self.text_edit.setCurrentFont(fondo)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextColor(color)

    def choose_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextBackgroundColor(color)

    def about_dialog(self):
        QMessageBox.about(self, "Acerca del Editor", "Esto es un editor de texto avazado creado por mi para practicar Python con PyQt5")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("noteblock.png"))
    window = Editor()
    window.show()
    sys.exit(app.exec_())
