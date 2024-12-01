from PyQt6.QtWidgets import QApplication , QInputDialog
from PyQt6.QtWidgets import QMainWindow
from ui import Ui_MainWindow
app = QApplication([])
win = QMainWindow()
import json
ui = Ui_MainWindow()
ui.setupUi(win)

NOTES = {
    "купи хліба": {
        "текст": "не забудь купити хліба по 20 грн",
        "теги": ["покупка", "хліб",],
    },
    "погодуй кота": {
        "текст": "не забудь погодувати кота",
        "теги": ["кіт", "смерть",],
    },
}
with open("notes_data.json","r", encoding='UTF-8') as file:
    NOTES = json.load(file)


ui.notes_list.addItems(NOTES)

def show_note():
    not_names = ui.notes_list.selectedItems()[0].text()
    note = NOTES[not_names] 
    ui.textEdit.setText(note["текст"])
    ui.tags_list.clear()
    ui.tags_list.addItems(note['теги'])

ui.notes_list.itemClicked.connect(show_note)
def add_note():
    note_name, ok = QInputDialog.getText(
        win, "Додати нотаток", "Назва нотатки:"
    )
    if ok:
        NOTES[note_name] = {
            "текст": "",
            "теги": [],
        }
        ui.notes_list.addItem(note_name)


ui.btn_create_note.clicked.connect(add_note)
def save_note():
    if ui.notes_list.selectedItems():
        note_name = ui.notes_list.currentItem().text()
        note_text = ui.textEdit.toPlainText()

        NOTES[note_name] = {
            "текст": note_text,
            "теги": [],
        }

        with open("notes_data.json","w", encoding='UTF-8') as file:
            json.dump(NOTES, file)

ui.btn_save_note.clicked.connect(save_note)


win.show()
app.exec()