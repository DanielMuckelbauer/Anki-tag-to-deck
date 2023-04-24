from aqt import mw
from aqt import gui_hooks
from aqt.qt import *
from anki.notes import Note

__name__ = "tag-to-deck-mapper"

from aqt.utils import *

mappings_key = 'mappings'
ignore_tags_key = 'ignoredTags'


def set_deck_from_config_tags(note: Note) -> None:
    if len(note.tags) > 1:
        return
    config = mw.addonManager.getConfig(__name__)
    if any(tag in note.tags for tag in config[ignore_tags_key]):
        return
    mappings = config[mappings_key]
    target_deck = next((deck for deck, tags in mappings.items() if any(tag in note.tags for tag in tags)), None)
    if target_deck:
        set_deck(target_deck, note)
    else:
        show_mapping_dialog(note)


def show_mapping_dialog(note) -> None:
    mw.dialog = dialog = QDialog(None)
    dialog.setWindowTitle('Map Tag to Deck')
    combo_box = create_combo_box()
    buttons = create_buttons(dialog, note, combo_box)

    layout = create_layout(combo_box, buttons)

    dialog.setLayout(layout)
    dialog.setGeometry(800, 500, 250, 100)
    dialog.show()


def create_buttons(dialog, note, box) -> QDialogButtonBox:
    buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    ignore_button = create_ignore_button(note, dialog)
    buttons.addButton(ignore_button, QDialogButtonBox.ButtonRole.ActionRole)
    buttons.rejected.connect(dialog.close)
    buttons.accepted.connect(lambda: set_deck_and_update_config(str(box.currentText()), note, dialog))
    return buttons


def create_ignore_button(note, dialog) -> QPushButton:
    ignore_button = QPushButton()
    ignore_button.clicked.connect(lambda: add_tags_to_ignore_list(note, dialog))
    ignore_button.setText('Ignore tag')
    return ignore_button


def create_combo_box() -> QComboBox:
    combo_box = QComboBox(None)
    for deck in mw.col.decks.all_names_and_ids():
        combo_box.addItem(deck.name)
    return combo_box


def create_layout(combo_box, buttons) -> QVBoxLayout:
    layout = QVBoxLayout()
    layout.addWidget(combo_box)
    layout.addWidget(buttons)
    return layout


def update_config(deck, tags) -> None:
    config = mw.addonManager.getConfig(__name__)
    config[mappings_key].setdefault(deck, []).extend(tags)
    mw.addonManager.writeConfig(__name__, config)


def set_deck_and_update_config(deck, note, dialog) -> None:
    set_deck(deck, note)
    update_config(deck, note.tags)
    dialog.close()


def add_tags_to_ignore_list(note, dialog) -> None:
    config = mw.addonManager.getConfig(__name__)
    config[ignore_tags_key] = config[ignore_tags_key] + note.tags
    mw.addonManager.writeConfig(__name__, config)
    dialog.close()


def set_deck(deck: str, note: Note) -> None:
    did = mw.col.decks.id_for_name(deck)
    for card in note.cards():
        card.did = did
        mw.col.update_card(card)
    show_tooltip(deck)


def show_tooltip(deck_name: str) -> None:
    tooltip("Deck was automatically changed to % s" % deck_name)


gui_hooks.add_cards_did_add_note.append(set_deck_from_config_tags)

action = QAction("test", mw)
qconnect(action.triggered, show_tooltip)
mw.form.menuTools.addAction(action)
