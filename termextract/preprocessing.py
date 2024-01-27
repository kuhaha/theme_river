import itertools as it
import re
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
        self.tagger = MeCab.Tagger(**kwargs)
        self.tagger.parse("Initialize")

    def iter_token(self, text):
        node = self.tagger.parseToNode(text)
        node = node.next
        while node.next:
            yield self.Morpheme(node.surface, *node.feature.split(",")[:3])
            node = node.next

def filter_noun(n):
    if re.match(r"[#!「」\(\)\[\]]", n.surface):
        return False
    if n.pos == "名詞" and n.pos_s1 in ["普通名詞", "固有名詞"]:
        return True
    if n.pos == "接尾辞" and n.pos_s1 in ["名詞的","形状詞的"] :
        return True
    if n.pos == "形状詞" and n.pos_s1 in ["一般"]:
        return True
    return False


def simple_filter_noun(n):
    return lambda n: n.pos == "名詞"


def extract_nouns(tokens, f=filter_noun):
    return [morphemes_to_surface(g) for k, g in it.groupby(tokens, f) if k]


def morphemes_to_surface(morphemes):
    return [m.surface for m in morphemes]