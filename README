wordmorph
=========

Finds the shortest number of steps to morph one word into another by changing one letter at a time. The initial, target and intermediate words must be valid from a given dictionary.

Usage:

    wordmorph.py [-h] [--verbose] file_name word_length start end

    Shortest steps to morph one word into another one letter at a time.

    positional arguments:
      file_name    text file with list of words
      word_length  number of letters per word
      start        start word
      end          end word

    optional arguments:
      -h, --help   show this help message and exit
      --verbose    show debug information

Examples:

    ./wordmorph.py words_5_letters.txt 5 smart brain

Output:

    Morph: smart to brain
    Path : 5 steps
    smart
    slart
    slait
    slain
    blain
    brain

Unit tests:
    ./tests.py

Word data sets:
1. words_all.txt: All English words taken from OS X /usr/share/dict/words
2. words_5_letters.txt: Only 5-letter words from the original list.
3. words_3_letters.txt: Only 3-letter words from the original list.

