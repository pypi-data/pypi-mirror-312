import string
import re
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag
from spellchecker import SpellChecker
import nltk
from IPython.display import display
from typing import List, Optional, Union

# Download required NLTK resources if not already downloaded
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("stopwords")


class TextPreprocessor:
    def __init__(self) -> None:
        self.stopwords: set[str] = set(stopwords.words("english"))
        self.lemmatizer: WordNetLemmatizer = WordNetLemmatizer()
        self.spell: SpellChecker = SpellChecker()
        self.ps: PorterStemmer = PorterStemmer()
        self.wordnet_map: dict[str, wordnet] = {
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "J": wordnet.ADJ,
            "R": wordnet.ADV,
        }

    def remove_punctuation(self, text: Optional[str]) -> Optional[str]:
        if text:
            return text.translate(str.maketrans("", "", string.punctuation))
        return text

    def remove_stopwords(self, text: Optional[str]) -> Optional[str]:
        if text:
            return " ".join(
                [word for word in text.split() if word not in self.stopwords]
            )
        return text

    def remove_special_characters(self, text: Optional[str]) -> Optional[str]:
        if text:
            text = re.sub(r"[^a-zA-Z0-9]", " ", text)
            text = re.sub(r"\s+", " ", text)
            return text
        return text

    def stem_text(self, text: Optional[str]) -> Optional[str]:
        if text:
            return " ".join([self.ps.stem(word) for word in text.split()])
        return text

    def lemmatize_text(self, text: Optional[str]) -> Optional[str]:
        if text:
            pos_text = pos_tag(text.split())
            return " ".join(
                [
                    self.lemmatizer.lemmatize(
                        word, self.wordnet_map.get(pos[0], wordnet.NOUN)
                    )
                    for word, pos in pos_text
                ]
            )
        return text

    def remove_url(self, text: Optional[str]) -> Optional[str]:
        if text:
            return re.sub(r"https?://\S+|www\.\S+", "", text)
        return text

    def remove_html_tags(self, text: Optional[str]) -> Optional[str]:
        if text:
            return re.sub(r"<[^>]+>", "", text)
        return text

    def correct_spellings(self, text: Optional[str]) -> Optional[str]:
        if text:
            corrected_text: List[str] = []
            misspelled_words = self.spell.unknown(text.split())
            for word in text.split():
                if word in misspelled_words:
                    corrected_word = self.spell.correction(word)
                    corrected_text.append(corrected_word)
                else:
                    corrected_text.append(word)
            return " ".join(corrected_text)
        return text

    def lowercase(self, text: Optional[str]) -> Optional[str]:
        if text:
            return text.lower()
        return text

    def preprocess(self, text: str, steps: Optional[List[str]] = None) -> str:
        """
        Automatically preprocess text with a default pipeline.
        User can specify steps for specific preprocessing order.

        Parameters:
        text (str): Text to preprocess.
        steps (list): List of preprocessing steps in desired order.

        Returns:
        str: Preprocessed text.
        """
        default_pipeline = [
            "lowercase",
            "remove_punctuation",
            "remove_stopwords",
            "remove_special_characters",
            "remove_url",
            "remove_html_tags",
            "correct_spellings",
            "lemmatize_text",
        ]
        steps = steps if steps else default_pipeline
        for step in steps:
            text = getattr(self, step)(text)
        return text

    def head(self, texts: Union[List[str], pd.Series], n: int = 5) -> None:
        """
        Display a summary of the first few entries of the dataset for quick visualization.

        Parameters:
        texts (list or pd.Series): The dataset or list of text entries to display.
        n (int): The number of rows to display. Default is 5.

        Returns:
        None
        """
        if isinstance(texts, (list, pd.Series)):
            data = pd.DataFrame({"Text": texts[:n]})
            data["Word Count"] = data["Text"].apply(lambda x: len(x.split()))
            data["Character Count"] = data["Text"].apply(len)
            display(data)


if __name__ == "__main__":
    TextPreprocessor()
