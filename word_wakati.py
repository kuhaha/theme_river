import MeCab
from janome.tokenizer import Tokenizer

def word_seq(text, parser=None):
    """ transforms `text` to a sequence of words
      e.g. 'hello, world' => ['hello','world']
         　'吾輩は猫である'=>['吾輩','は','猫','で','ある']
        (parser=<mecab>|<janome>, parser created by `create_parser`)
      
    """
    
    if parser is None:
        return text.split()
    
    if type(parser) is str:
        return text.split(sep=parser)
   
    return parser(text)

def create_parser(worker='janome', parts_of_speech=['名詞'], stop_words=[]):
    """ parser factory generates parser 
      @parms: `parts_of_speech`, `stop_word`
    """
    def _mecab(text):
        """ mecab parser
        """
        # tagger = MeCab.Tagger()
        # tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        tagger = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
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
    
    if worker == 'mecab':
        return _mecab
    else:
        return _janome
