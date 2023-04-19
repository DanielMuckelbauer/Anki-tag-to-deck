# import the main window object (mw) from aqt
import collections

from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
import anki
from anki.notes import Note

from aqt import gui_hooks


# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction() -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("Card count: %d" % cardCount)


def hook_function(note: Note) -> None:
    if any(item == "test" for item in note.tags):
        print("inside if")
        did = mw.col.decks.id_for_name("Root::01Programming")
        print("did:" + str(did))
        for card in note.cards():
            card.did = did
            mw.col.update_card(card)


gui_hooks.add_cards_did_add_note.append(hook_function)
# gui_hooks.add_cards_will_add_note.append(hook_function)

# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
