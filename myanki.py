from __future__ import annotations

from aqt.profiles import ProfileManager
from anki.collection import Collection
from anki.notes import Note


class MyAnki:
    def __init__(self, profile_name: str) -> None:
        self.pm = ProfileManager(ProfileManager._default_base())
        self.pm.setupMeta()
        self.pm.openProfile('tutorial')
        self.col = Collection(self.pm.collectionPath())

    def new_note_to_collection(self, deck_name: str, model_name: str,
                               note_contents: list | dict) -> Note | None:
        deck = self.col.decks.by_name(deck_name)
        if not deck:
            print("deck not found")
            return

        model = self.col.models.by_name(model_name)
        if not model:
            print("model not found")
            return

        fields = self.col.models.field_names(model)

        note = self.col.new_note(model)

        if isinstance(note_contents, list):
            count = min(len(fields), len(note_contents))
            for i in range(count):
                note[fields[i]] = note_contents[i]
        elif isinstance(note_contents, dict):
            for fld, text in note_contents.items():
                if fld in fields:
                    note[fld] = text
        else:
            print('note contents can only be list or dict type')
            return

        if not note.duplicate_or_empty():
            self.col.add_note(note, deck['id'])
            return note
        else:
            return


if __name__ == '__main__':
    myanki = MyAnki('tutorial')
    myanki.new_note_to_collection('Default', 'Basic',
                                  ['Hello Anki', "It's from Python"])
