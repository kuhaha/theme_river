# Term/Phrase/Keyword Extraction and  Visualization

Try to use `mecab-ipadic-neologd` dic in MeCab tagger if possible
```
# in word_wakati.py
## tagger = MeCab.Tagger() 
## tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
tagger = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
tagger.parse('')
```
