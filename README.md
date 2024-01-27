# Term/Phrase/Keyword Extraction and  Visualization

Try to use `mecab-ipadic-neologd` dic in MeCab tagger as long as possible

## 日本語品詞体系


### UniDic品詞体系

cf. https://hayashibe.jp/tr/mecab/dictionary/unidic/pos
- pos1: 名詞、動詞、形容詞、**形状詞**、副詞、助詞、代名詞、接頭辞、接尾辞、助詞、接続詞、助動詞、感動詞、記号
- pos2:
  - [名詞]（普通名詞「教室」「勉強」「安全」「心配」、固有名詞「吉野」「日本」「研究室」、数詞、助動詞語幹）
  - [動詞]（一般「食べる」、非自立可能「（し）始める」「（て）くる」）
  - [形容詞]（一般「美しい」、非自立可能（て）よい」「（て）欲しい」）
  - [形状詞]（一般「静か」「健やか」、タリ釈然」「錚々」、助動詞語幹「そう」「よう」「みたい」）
 
### NAIST-jdic/IPADIC品詞体系

cf. https://hayashibe.jp/tr/juman/dictionary/pos
- pos1: 名詞、動詞、形容詞、副詞、助詞、連体詞、接続詞、接頭詞、助詞、感動詞、助動詞、記号、フィラー、その他
- pos2:
  - [名詞]（一般、固有名詞、サ変接続、ナイ形容詞語幹、形容動詞語幹、接尾、接続詞的、数、代名詞）
  - [動詞]（自立、接尾、非自立）
  - [形容詞]（自立、接尾、非自立）


### JUMAN品詞体系

cf. https://hayashibe.jp/tr/mecab/dictionary/ipadic
- pos1: 名詞、動詞、形容詞、副詞、**指示詞**、**判定詞**、助詞、連体詞、接続詞、接頭詞、接尾辞、助詞、感動詞、助動詞、記号
- pos2:
  - [名詞]（普通名詞、固有名詞、形式名詞、副詞的名詞、サ変名詞、数詞、時相名詞、地名、人名、組織名）
  - [動詞]
  - [形容詞]
 