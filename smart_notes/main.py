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

        NOTES[note_name]["теги"] = note_text


        with open("notes_data.json","w", encoding='UTF-8') as file:
            json.dump(NOTES, file)

ui.btn_save_note.clicked.connect(save_note)

def del_note():
    if ui.notes_list.selectedItems():
        note_name = ui.notes_list.currentItem().text()
        del NOTES [note_name]
        ui.notes_list.clear()
        ui.notes_list.addItems(NOTES)

        with open("notes_data.json", "w", encoding = "UTF-8") as file:
            json.dump(NOTES, file)

ui.btn_delete_note.clicked.connect(del_note)

def add_tag():
    if ui.notes_list.selectedItems():
        note_name = ui.notes_list.currentItem().text()

        tag = ui.tag_search.text()

        if tag not in NOTES[note_name]["теги"]:
            NOTES[note_name]["теги"].append(tag)
            ui.tags_list.addItem(tag)
            ui.tag_search.clear()

            with open("notes_data.json", "w", encoding = "UTF-8") as file:
                json.dump(NOTES, file)

ui.btn_add_tag.clicked.connect(add_tag)
            
def search_tag():
    if ui.btn_search.text() == "шукати по тегу":
        tag = ui.tag_search.text()
        filtered_notes = {}
        for note_name, note in NOTES.items():
            if tag in note['теги']:
                filtered_notes[note_name] = note

        
        ui.notes_list.clear()
        ui.notes_list.addItems(filtered_notes)

        ui.btn_search.setText("Скинути пошук")

    elif ui.btn_search.text() == "Скинути пошук":
        ui.notes_list.clear()
        ui.notes_list.addItems(NOTES)
        ui.btn_search.setText("шукати по тегу")
        ui.tag_search.clear()


ui.btn_search.clicked.connect(search_tag)

def del_tag():
    if ui.notes_list.selectedItems():
        note_name = ui.notes_list.currentItem().text()
        if ui.tags_list.selectedItems():
            tag = ui.tags_list.currentItem().text()
            NOTES[note_name]["теги"].remove(tag)

            ui.tags_list.clear()
            ui.tags_list.addItems(NOTES[note_name]["теги"])

            with open("notes_data.json", "w", encoding="UTF-8") as file:
                    json.dump(NOTES, file)

ui.btn_delete_tag.clicked.connect(del_tag)


win.show()
app.exec()