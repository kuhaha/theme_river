import itertools as it
import functools as func

import re
import os
import MeCab

from collections import namedtuple


class MeCabTokenizer:

    Morpheme = namedtuple("Morpheme", "surface pos pos_s1 pos_s2")
    
    IPADIC_POS = {
        "名詞"  : ["一般", "固有名詞", "サ変接続", "ナイ形容詞幹","副詞可能 ","形容動詞語幹","数","接尾"],
        "接頭詞" : ["名詞接続","数接続"],
        "形容詞": ["自立"]
    }
    UNIDIC_POS = {
        "名詞"  : ["普通名詞", "固有名詞", "数詞"],
        "接尾辞": ["名詞的","形状詞的"],
        "形状詞": ["一般"]
    }

    def __init__(self, **kwargs):
        dicdir = os.popen("mecab-config --dicdir").read().strip()
        neologd = os.path.join(dicdir, "mecab-ipadic-neologd")
        if os.path.isdir(neologd):
            self.use_dic = 'ipadic'  
            self.tagger = MeCab.Tagger("-d "+neologd) 
        else:
            self.use_dic = 'unidic'
            self.tagger = MeCab.Tagger(**kwargs)
            
        self.tagger.parse("Initialize")

    def iter_token(self, text):
        node = self.tagger.parseToNode(text)
        node = node.next
        while node.next:
            yield self.Morpheme(node.surface, *node.feature.split(",")[:3])
            node = node.next

    def filter_noun(self, n):
        comp_pos = self.IPADIC_POS if self.use_dic=='ipadic' else self.UNIDIC_POS 
        
        if re.match(r"[#!「」\(\)\[\]]", n.surface):
            return False
        if n.pos in comp_pos and  n.pos_s1 in comp_pos[n.pos]:
            return True
        return False
    
    def simple_filter_noun(self, n):
        return lambda n: n.pos == "名詞"
    
    def extract_nouns(self, tokens):
        return [self.morphemes_to_surface(g) for k, g in it.groupby(tokens, self.filter_noun) if k]
    
    def morphemes_to_surface(self, morphemes):
        return [m.surface for m in morphemes]

    def filter_nouns(self, comp_nouns, n=1, stopwords=[], stopwords_begin=[], stopwords_end=[]):
        has_stopword = lambda x: (set(x) & set(stopwords)) or x[0] in stopwords_begin or x[-1] in stopwords_end
        return [cn for cn in comp_nouns if len(cn)>=n and not has_stopword(cn)]
