import itertools as it
import re
import MeCab

from collections import namedtuple


class MeCabTokenizer:
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

"""
surface='知能', pos='名詞', pos_s1='普通名詞', pos_s2='一般'   
surface='会議', pos='名詞', pos_s1='普通名詞', pos_s2='サ変可能'
surface='多少', pos='名詞', pos_s1='普通名詞', pos_s2='副詞可能'
surface='安部', pos='名詞', pos_s1='固有名詞', pos_s2='人名'
surface='ソフト', pos='名詞', pos_s1='普通名詞', pos_s2='形状詞可能
surface='直感', pos='名詞', pos_s1='普通名詞', pos_s2='サ変可能'
surface='的', pos='接尾辞', pos_s1='形状詞的', pos_s2='*'
surface='用', pos='接尾辞', pos_s1='名詞的', pos_s2='一般'
surface='曖昧', pos='形状詞', pos_s1='一般', pos_s2='*'

"""
def filter_noun(n):
    if re.match(r"[#!「」\(\)\[\]]", n.surface):
        return False
    if n.pos == "名詞" and n.pos_s1 == "普通名詞":
        return True
    if n.pos=="名詞" and n.pos_s1=="固有名詞":
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