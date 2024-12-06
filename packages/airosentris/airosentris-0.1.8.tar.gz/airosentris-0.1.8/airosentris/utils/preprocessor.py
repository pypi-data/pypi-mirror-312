import os
import logging
import pandas as pd
import numpy as np
import re
import emoji
import nltk
from nltk.tokenize import word_tokenize

BASE_PATH = os.getcwd()

class DataPreprocessor:
    def __init__(self, 
                 stopword_path='airosentris\data\stopword.txt', 
                 kamus_alay_path='airosentris\data\kamus_alay.csv'):
        
        self.stopword_path = os.path.join(BASE_PATH, stopword_path)
        self.kamus_alay_path = os.path.join(BASE_PATH, kamus_alay_path)
        self.list_stopwords = self.load_stopwords()
        self.normalize_word_dict = self.load_kamus_alay()
        
        nltk.download('punkt')
        nltk.download('punkt_tab')        

        # Logging setup
        logging.basicConfig(level=logging.INFO)

    def load_stopwords(self):
        """Load stopwords dari file."""
        if not os.path.exists(self.stopword_path):
            logging.error(f"Stopword file not found at {self.stopword_path}")
            return []
        try:
            stopwords = pd.read_csv(self.stopword_path, header=None, names=["stopwords"], engine='python')
            return stopwords.stopwords.to_list()
        except Exception as e:
            logging.error(f"Error loading stopwords: {e}")
            return []

    def load_kamus_alay(self):
        """Load kamus alay dan buat dictionary."""
        if not os.path.exists(self.kamus_alay_path):
            logging.error(f"Kamus alay file not found at {self.kamus_alay_path}")
            return {}
        try:
            kamus_alay = pd.read_csv(self.kamus_alay_path)
            return dict(zip(kamus_alay.iloc[:, 0], kamus_alay.iloc[:, 1]))
        except Exception as e:
            logging.error(f"Error loading kamus alay: {e}")
            return {}

    def repeatchar_clean(self, text):
        """Membersihkan karakter berulang menggunakan regex."""
        return re.sub(r"(.)\1{2,}", r"\1", text)

    def clean_text(self, text):
        """Bersihkan teks dari noise."""
        try:
            text = text.lower()
            text = re.sub(r"\n", " ", text)
            text = emoji.demojize(text)
            text = re.sub(r":[A-Za-z_-]+:", " ", text)
            text = re.sub(r"([xX;:]'?[dDpPvVoO3)(])", " ", text)
            text = re.sub(r"(https?:\/\/\S+|www\.\S+)", "", text)
            text = re.sub(r"@[^\s]+[\s]?", " ", text)
            text = re.sub(r"#(\S+)", r"\1", text)
            text = re.sub(r"[^a-zA-Z,.?!]+", " ", text)
            text = self.repeatchar_clean(text)
            text = re.sub(r"[ ]+", " ", text).strip()
            return text
        except Exception as e:
            logging.error(f"Error cleaning text: {e}")
            return ""

    def normalize_text(self, text):
        """Normalize teks berdasarkan kamus alay."""
        try:
            tokens = word_tokenize(text)
            tokens = [self.normalize_word_dict.get(token, token) for token in tokens]
            return " ".join(tokens)
        except Exception as e:
            logging.error(f"Error normalizing text: {e}")
            return text

    def preprocess(self, df, clean=True, normalize=True):
        """
        Preprocess dataframe dengan langkah-langkah opsional.

        Args:
            df (pd.DataFrame): Dataframe input yang memiliki kolom 'text'.
            clean (bool): Jika True, lakukan pembersihan teks.
            normalize (bool): Jika True, lakukan normalisasi teks.
        
        Returns:
            pd.DataFrame: Dataframe yang sudah diproses.
        """
        if not isinstance(df, pd.DataFrame):
            logging.error("Input is not a pandas DataFrame")
            return df
        
        try:
            df_pp = df.copy()
            
            if clean:
                logging.info("Starting text cleaning...")
                df_pp["text"] = pd.Series(df_pp["text"]).apply(self.clean_text)
            
            if normalize:
                logging.info("Starting text normalization...")
                df_pp["text"] = pd.Series(df_pp["text"]).apply(self.normalize_text)
            
            # Replace empty texts with NaN and drop
            df_pp["text"] = df_pp["text"].replace("", np.nan)
            df_pp.dropna(subset=["text"], inplace=True)

            logging.info("Preprocessing complete.")
            return df_pp
        except Exception as e:
            logging.error(f"Error during preprocessing: {e}")
            return df