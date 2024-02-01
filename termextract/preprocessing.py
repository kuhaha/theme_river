import itertools as it
import functools as func

import re
import os
import MeCab

from collections import namedtuple


class MeCabTokenizer:
    """UniDic品詞体系 cf. https://hayashibe.jp/tr/mecab/dictionary/unidic/pos
    surface,  pos,  pos_s1, pos_s2
    '知能', '名詞', '普通名詞', '一般'   
    '直感', '名詞', '普通名詞', 'サ変可能'
    '多少', '名詞', '普通名詞', '副詞可能'
    '安部', '名詞', '固有名詞', '人名'
    'ソフト', '名詞', '普通名詞', '形状詞可能
    '的', '接尾辞', '形状詞的', '*'
    '用', '接尾辞', '名詞的', '一般'
    '曖昧', '形状詞', '一般', '*'
    """

    Morpheme = namedtuple("Morpheme", "surface pos pos_s1 pos_s2")

    def __init__(self, **kwargs):         
        dicdir = os.popen("mecab-config --dicdir").read().strip()
        neologd = os.path.join(dicdir, "mecab-ipadic-neologd")
        self.use_dic = 'ipadic' if os.path.isdir(neologd) else 'unidic'        
        self.tagger = MeCab.Tagger("-d "+neologd) if os.path.isdir(neologd) else MeCab.Tagger(**kwargs)
        self.tagger.parse("Initialize")

    def iter_token(self, text):
        node = self.tagger.parseToNode(text)
        node = node.next
        while node.next:
            yield self.Morpheme(node.surface, *node.feature.split(",")[:3])
            node = node.next

def filter_noun(n, dic='ipadic'):
    unidic_pos = {
        "名詞"  : ["普通名詞", "固有名詞"],
        "接尾辞": ["名詞的","形状詞的"],
        "形状詞": ["一般"]
    }
    ipadic_pos = {
        "名詞"  : ["一般", "固有名詞", "サ変接続", "ナイ形容詞幹", "接尾"],
        "形容詞": ["自立"]
    }
    comp_pos = ipadic_pos if dic=='ipadic' else unidic_pos 
    
    if re.match(r"[#!「」\(\)\[\]]", n.surface):
        return False
    if n.pos in comp_pos and  n.pos_s1 in comp_pos[n.pos]:
        return True
    return False


def simple_filter_noun(n):
    return lambda n: n.pos == "名詞"


def extract_nouns(tokens, f=filter_noun, stopwords=[], n=1):
    groups = [morphemes_to_surface(g, stopwords) for k, g in it.groupby(tokens, f) if k]
    return [group for group in groups if len(group)>=n]

def morphemes_to_surface(morphemes, stopwords):
    return [m.surface for m in morphemes if m.surface not in stopwords]
