# -*- coding: utf-8 -*-
# Copyright: Henning Sperr
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Automatic reading and meaning generation using Yomichan dictionary
# Inspired by Japanese Support Plugin
#

import re
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw

import yomi_dict


source_field = 'Expression'
reading_field = 'Reading'
meaning_field = 'Meaning'
NOTE_TYPE_NAME = 'japanese'

try:
    import japanese.reading
    DO_READING = False
    MENU_NAME = 'Bulk-add Meanings'
except:
    DO_READING = True
    MENU_NAME = 'Bulk-add Readings/Meanings'


class YomichanDictionary(object):
    def __init__(self):
        self.lang = yomi_dict.initLanguage()

    def lookup(self, expr):
        meaning_expr = expr
        final_meanings = []
        done = set()
        while meaning_expr:
            meanings = self.lang.findTerm(meaning_expr)
            if meanings and meanings[1]>0:
                meaning = meanings[0][0]

                src = meaning['source'] or 'None'
                if not src in done:
                    done.add(src)
                    read = meaning['reading'] or None
                    mn = meaning['glossary'] or None

                    final_meanings.append({'Expression': src, 'Reading': read, 'Meaning': mn})

                for meaning in meanings[0][1:]:
                    if not meaning['source']==src:
                        break

                    read = meaning['reading'] or None
                    mn = meaning['glossary'] or None
                    final_meanings.append({'Expression': src, 'Reading': read, 'Meaning': mn})


                meaning_expr = meaning_expr[len(src):]
            else:
                meaning_expr = meaning_expr[1:]

        expression_string = expr
        meaning_string = []
        for entries in sorted(final_meanings, key=lambda x: -len(x['Expression'])):
            if entries['Reading']:
                if re.search(ur'[\u4e00-\u9faf]', entries['Expression']):
                    expression_string = expression_string.replace(entries['Expression'], entries['Expression']+'['+entries['Reading']+']')
            if entries['Meaning']:
                if len(final_meanings) == 1:
                    meaning_string.append(entries['Meaning'])
                else:
                    if len(entries['Expression']) > 4 or re.search(ur'[\u4e00-\u9faf]', entries['Expression']):
                        meaning_string.append(entries['Reading']+' - '+entries['Meaning'])

        return expression_string, '<br>'.join(meaning_string)


def update_note(note):
    """
    :param note: note to be checked whether meaning and reading needs an update
    :return: True if updated, False if not updated
    """

    if NOTE_TYPE_NAME not in note.model()['name'].lower():
        return False

    if not source_field in note:
        return False

    if not meaning_field in note or not reading_field in note:
        return False

    if note[meaning_field].strip() and note[reading_field].strip():
        return False

    text = mw.col.media.strip(note[source_field])
    if not text.strip():
        return False

    try:
        reading, meaning = yomidict.lookup(text)
        if not note[reading_field].strip() and DO_READING:
            note[reading_field] = reading
        if not note[meaning_field].strip():
            note[meaning_field] = meaning
    except Exception, e:
        raise e

    return True


def on_focus_lost(flag, note, fidx):

    if not yomidict:
        return flag

    #check whether the event comes from the source field
    if fidx != mw.col.models.fieldNames(note.model()).index(source_field):
        return flag

    if update_note(note):
        return True
    return flag


def regenerate_bulk_readings(note_ids):
    if not yomidict:
        raise Exception('Yomidict not working.')

    mw.checkpoint(MENU_NAME)
    mw.progress.start()

    for nid in note_ids:
        note = mw.col.getNote(nid)
        update_note(note)
        note.flush()

    mw.progress.finish()
    mw.reset()

def setup_menu_item(browser):
    a = QAction(MENU_NAME, browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: on_regenerate(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def on_regenerate(browser):
    regenerate_bulk_readings(browser.selectedNotes())

yomidict = YomichanDictionary()
addHook('editFocusLost', on_focus_lost)
addHook("browser.setupMenus", setup_menu_item)

if __name__ == "__main__":
    #examples are shamelessly taken from Japanese Support Anki Plugin
    expr = u"カリン、自分でまいた種は自分で刈り取れ"
    print yomidict.lookup(expr).encode("utf-8")
    expr = u"昨日、林檎を2個買った。"
    print yomidict.lookup(expr).encode("utf-8")
    expr = u"真莉、大好きだよん＾＾"
    print yomidict.lookup(expr).encode("utf-8")
    expr = u"彼２０００万も使った。"
    print yomidict.lookup(expr).encode("utf-8")
    expr = u"彼二千三百六十円も使った。"
    print yomidict.lookup(expr).encode("utf-8")
    expr = u"千葉"
    print yomidict.lookup(expr).encode("utf-8")
    expr = u"滅"
    print yomidict.lookup(expr).encode("utf-8")
