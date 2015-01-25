<b>Anki Automatic Japanese Dictionary Look-Up</b>

This add-on automatically adds the meanings of Japanese words to flashcards in Anki. Both single words and whole sentences are supported.

Like the Japanese Support add-on, this plugin works for all note types that have "Japanese" in the name. It evaluates the "Expression" field and inserts the meaning into the "Meaning" field. You can add meanings in bulk via the "Bulk add meanings" option in the card browser toolbar.

<b>How to install & use</b>

THE EASIEST WAY:

1. Download this add-on using Anki.
2. Download the Japanese Support add-on as well: https://ankiweb.net/shared/info/3918629684
3. Done. Just use the "Japanese" note type that is included in the Japanese Support add-on.

Whenever you change the Expression field when editing a card and select another field, the Meaning and Reading should be generated automatically, if they were empty before.

If the Expression field contains multiple words (or a sentence), they are inserted in the following format into the Meaning field:
"[kanji1] - [meaning1]
[kanji2] - [meaning2] ..."



IF YOU WANT TO USE ANOTHER NOTE TYPE:

1. Make sure your Note Type has 'Japanese' in its name.
2. Make sure that the Note type has the fields 'Expression', 'Reading' and 'Meaning'


<b>Comments</b>

It is recommended (but not necessary) to install the Japanese Support add-on to display furigana and create functional default note types for Japanese: 
https://ankiweb.net/shared/info/3918629684

The add-on uses the JMDict dictionary file (like the browser extensions Rikaichan and Rikaikun). For an explanation of the grammatical information (adj-i, n, v3...) and licence info, check the JMDict project's homepage:
http://www.edrdg.org/jmdict/j_jmdict.html

To generate the meanings, I used code from the Yomichan add-on, which in turn used parts of the Rikaichan browser extension, both of which are highly recommended. You can use Yomichan to read books and extract cards from them:
https://ankiweb.net/shared/info/934748696
Yomichan does not need to be installed for this add-on to work.

So far this add-on has only been tested on OS X, but if Yomichan works for you, this should work too.

If you have any issues or comments, want to contribute or donate, just post here or on GitHub: 
https://github.com/hsperr/japanese_meanings

DogeCoin:
DKJeyQ8iaQBKqJ5v3ANd6y3J73Xux48UJV

BTC:
1NtsE4okrA9SruxcS5hVEyjDDGetFMeEL5

Enjoy!


<b>More comments, known issues</b>

- In ambiguous cases with many dictionary entries(今日, 私, hiragana homophones...), the generated meaning may be wrong. Use Yomichan or Rikaichan to see all the dictionary entries. Don't add vocab blindly, anyway.
- If Japanese support is not installed, readings will be generated from the dictionary.
