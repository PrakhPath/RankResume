from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

import re
import unicodedata
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


class PreProcessor:
    _pos_tag_dict = {
        "a": wordnet.ADJ,
        "s": wordnet.ADJ_SAT,
        "r": wordnet.ADV,
        "n": wordnet.NOUN,
        "v": wordnet.VERB
    }

    @staticmethod
    def _remove_unicode_space(text) -> str:
        text = " ".join(text.split(r"\xa0"))
        return text

    @staticmethod
    def _remove_accents(text) -> str:
        text = unicodedata.normalize('NFKD', text) \
            .encode('ASCII', 'ignore') \
            .decode('utf-8', 'ignore')
        return text

    @staticmethod
    def _remove_email_web(text) -> str:
        pattern = r'[\S]+@[\S]+\.[\S]+[\s]?'
        text = re.sub(pattern, '', text)

        pattern = r'[\S]+\.(?:gov|com|in|net|org|edu)'
        text = re.sub(pattern, '', text)
        return text

    @staticmethod
    def _remove_phone(text) -> str:
        return text
        # pattern = r"(\+\d{1,3})?\s?\(?\d{1,10}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
        # pattern = r"(\+\d{1,3})?\s\(?\d{1,4}\)?[\s\.\-]?\d{3}[\s\.\-]?\d{4}"
        # print(re.findall(pattern, '+1 (555) 123-4567'))

    @staticmethod
    def _remove_symbols(text) -> str:
        pattern = r'[^A-Za-z0-9\s\/\-]+'
        text = re.sub(pattern, '', text)
        text = text.replace(r'/', ' ')
        text = text.replace(r'-', ' ')
        return text

    @staticmethod
    def _tokenize_words(text) -> list:
        token_list = word_tokenize(text)
        return token_list

    @staticmethod
    def _remove_stopwords(token_list) -> list:
        stopwords_eng = stopwords.words('english')
        token_list = [token for token in token_list[:] if token not in stopwords_eng]
        return token_list

    @staticmethod
    def _get_pos(token) -> str:
        pos_tag = nltk.pos_tag(list(token))[0][1][0].lower()
        pos_tag = PreProcessor._pos_tag_dict.get(pos_tag, wordnet.NOUN)
        return pos_tag

    def _lemmatize_tokens(self, token_list) -> list:
        lemmatizer = WordNetLemmatizer()
        lem_token_list = []
        for token in token_list:
            lem_token = lemmatizer.lemmatize(token, self._get_pos(token))
            lem_token_list.append(lem_token)

        return lem_token_list

    @staticmethod
    def _stem_tokens(token_list) -> str:
        port_stemmer = PorterStemmer()
        token_list = [port_stemmer.stem(token) for token in token_list[:]]
        token_list = list(set(token_list))
        text = ' '.join(token for token in token_list)

        return text

    def pre_process(self, init_text):
        init_text = init_text.lower()
        init_text = init_text.replace(r'\n', ' ')
        text = self._remove_unicode_space(init_text)
        text = self._remove_accents(text)
        text = self._remove_email_web(text)
        text = self._remove_phone(text)
        text = self._remove_symbols(text)
        token_list = self._tokenize_words(text)
        token_list = self._remove_stopwords(token_list)
        token_list = self._lemmatize_tokens(token_list)
        text = self._stem_tokens(token_list)

        return text
