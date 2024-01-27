import os
import string

import MeCab
from janome.tokenizer import Tokenizer
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")
nltk.download("omw-1.4")

def neologd():
    dicdir = os.popen("mecab-config --dicdir").read().strip()
    neologd = os.path.join(dicdir, "mecab-ipadic-neologd")
    if (os.path.isdir(neologd)):
        return neologd
    return None
    
def word_seq(text, parser=None):
    """ transforms `text` to a sequence of words
      e.g. 'hello, world' => ['hello','world']
         　'吾輩は猫である'=>['吾輩','は','猫','で','ある']
        (parser= 'mecab' or 'janome' )
      
    """    
    if parser is None:
        return text.split()
    
    if type(parser) is str:
        return text.split(sep=parser)
   
    return parser(text)

def create_parser(worker='janome', parts_of_speech=['名詞'], stop_words=[]):
    """ parser factory generates parser 
      @parms: `parts_of_speech`, `stop_words`
    """
    def _mecab(text):
        """ mecab parser
        """
        neodic = neologd()
        tagger = MeCab.Tagger("-d " + neodic) if neodic else MeCab.Tagger()
        tagger.parse('')
        
        node = tagger.parseToNode(text)
        rs = []
        while node:
            word = node.surface
            if node.feature.split(",")[0] == u"動詞": 
                 word = node.feature.split(",")[6]
            
            hinshi = node.feature.split(",")[0]
            if hinshi in parts_of_speech and word not in stop_words:
                rs += [word]

            node = node.next
            
        return rs
    

    def _janome(text):
        """ janome parser [default]
        """
        t = Tokenizer()
        rs = []
        for token in t.tokenize(text):
            word = token.base_form
            hinshi = token.part_of_speech.split(',')[0]
            if hinshi in parts_of_speech and word not in stop_words:
                rs += [word]
    
        return rs
        
    def _english(text):
        """ english parser
        """
        def _filter_pos(term):
            word = wnl.lemmatize(term, pos="v")
            word = wnl.lemmatize(word, pos="n")
            return wnl.lemmatize(word, pos="s")
            
        wnl = WordNetLemmatizer()
        text_no_punct = text.translate(str.maketrans("", "", string.punctuation))
        word_tokens = word_tokenize(text_no_punct)
        return [_filter_pos(word) for word in word_tokens]

    
    if worker == 'mecab':
        return _mecab
    elif worker == 'english':
        return _english
    else:
        return _janome
