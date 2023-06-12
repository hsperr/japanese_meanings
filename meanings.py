# -*- coding: utf-8 -*-
# Copyright: Henning Sperr
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Automatic reading and meaning generation using Yomichan dictionary
# Inspired by Japanese Support Plugin
#

import re
import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from anki.hooks import addHook
from aqt import mw

from . import yomi_dict

config = mw.addonManager.getConfig(__name__)

source_field = config["source_field"]
reading_field = config["reading_field"]
meaning_field = config["meaning_field"]
speech_field = config["speech_field"]
NOTE_TYPE_NAME = config["note_type_name"]
definitions = config["max_entries"]
read_in_def= config["reading_in_definition"]

try:
    import japanese.reading
    DO_READING = False
    MENU_NAME = 'Bulk-add Meanings'
except:
    DO_READING = True
    MENU_NAME = 'Bulk-add Readings/Meanings/Speech'


class YomichanDictionary(object):
    def __init__(self):
        self.lang = yomi_dict.initLanguage()

    def lookup(self, expr):
        expr = expr.strip()
        meaning_expr = expr
        final_meanings = []
        done = set()
        while meaning_expr:
            #returns [list_of_entries,num_entries]
            meanings = self.lang.findTerm(meaning_expr)
            if meanings and meanings[1]>0:
                meaning = meanings[0][0]

                src = meaning['source'] or 'None'
                #if we process a sentence, the same vocab might appear twice
                if not src in done:
                    done.add(src)
                    read = meaning['reading'] or src
                    mn = meaning['glossary'] or 'No Meaning Found'
                    tg = meaning['tags']

		

                    final_meanings.append({'Expression': src, 'Reading': read, 'Meaning': mn, 'Tags':tg})

                    #see if the same source (kanji) has different meanings/readings
                    for meaning in meanings[0][1:]:
                        if not meaning['source'] == src:
                            break

                        read = meaning['reading'] or src
                        mn = meaning['glossary'] or 'No Meaning Found'
                        tag = meaning['tags'] 
                        final_meanings.append({'Expression': src, 'Reading': read, 'Meaning': mn, 'Tags': tg})


                #remove current vocab from expression
                meaning_expr = meaning_expr[len(src):]
            else:
                #we didn't find a vocab so just move one character forward
                meaning_expr = meaning_expr[1:]

        expression_string = expr
        meaning_string = []
        tags_string = []
        idef=0
        #move through the final meanings list and sort them by length of the expression
        #we do this because we replace a kanji in the original sentence with kanji[reading]
        #some kanji could be substring of another kanji.
        for entries in sorted(final_meanings, key=lambda x: -len(x['Expression'])):
            if entries['Reading']:
                #search if the expression actually is a kanji
                if re.search(r'[\u4e00-\u9faf]', entries['Expression']):
                    expression_string = expression_string.replace(entries['Expression'], entries['Expression']+'['+entries['Reading']+']')
            if entries['Meaning']:
              
                #only output meanings for kanji or hiragana/katakana longer than 2 letters
                if expr == entries['Expression'] or len(entries['Expression']) > 2 or re.search(r'[\u4e00-\u9faf]', entries['Expression']):
                    idef=idef+1
                    #only output definitions up to the specified number
                    if idef <= definitions:
                        #output reading - meaning if configured, and more than one meaning
                        if read_in_def & len(final_meanings) > 1:
                            meaning_string.append(entries['Reading']+' - '+entries['Meaning'])
                        else:
                            meaning_string.append('- '+entries['Meaning'])
                    tags_string.append(' '.join(entries['Tags']))
              
        if len(tags_string)>0:
            tt = tags_string[0]
        else:
            tt = ''

        return expression_string, '<br>'.join(meaning_string), tt


def update_note(note):
    """
    :param note: note to be checked whether meaning and reading needs an update
    :return: True if updated, False if not updated
    """

    if NOTE_TYPE_NAME not in note.model()['name'].lower():
        return False

    if not source_field in note:
        return False

    else:
        if not note[speech_field].strip():
            text = mw.col.media.strip(note[source_field])
            if text.strip():
                reading, meaning, tags = yomidict.lookup(text)
                note[speech_field] = tags
              
            
                

    if not meaning_field in note or not reading_field in note:
        return False

    if note[meaning_field].strip() and note[reading_field].strip():
        return False

    text = mw.col.media.strip(note[source_field])
    if not text.strip():
        return False

    try:
        reading, meaning, tags = yomidict.lookup(text)
        if not note[reading_field].strip() and DO_READING:
            note[reading_field] = reading
        if not note[meaning_field].strip():
            note[meaning_field] = meaning
    except Exception as e:
        raise e

    return True


def on_focus_lost(flag, note, fidx):

    if not yomidict:
        return flag

    if NOTE_TYPE_NAME not in note.model()['name'].lower():
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

    # Default parameter trick wasn't working. This is hacky but works
    saved = browser
    a.triggered.connect(lambda: on_regenerate(saved))

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
    print(yomidict.lookup(expr).encode("utf-8"))
    expr = u"昨日、林檎を2個買った。"
    print(yomidict.lookup(expr).encode("utf-8"))
    expr = u"真莉、大好きだよん＾＾"
    print(yomidict.lookup(expr).encode("utf-8"))
    expr = u"彼２０００万も使った。"
    print(yomidict.lookup(expr).encode("utf-8"))
    expr = u"彼二千三百六十円も使った。"
    print(yomidict.lookup(expr).encode("utf-8"))
    expr = u"千葉"
    print(yomidict.lookup(expr).encode("utf-8"))
    expr = u"滅"
    print(yomidict.lookup(expr).encode("utf-8"))
