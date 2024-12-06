import gensim
import kagglehub
import nltk
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pandas import DataFrame


class TextPreprocessingUtils:

    @staticmethod
    def download_nltk_resources():
        """Download necessary NLTK resources."""

        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
        nltk.download("wordnet", quiet=True)

    @staticmethod
    def remove_html_tags(text):
        """Remove HTML tags from text."""

        if not isinstance(text, str):
            return text
        return BeautifulSoup(text, "html.parser").get_text(strip=True)

    @staticmethod
    def gensim_preprocess(text: str):
        """Remove special characters and convert to lowercase."""

        return " ".join(gensim.utils.simple_preprocess(text, deacc=True))

    @staticmethod
    def remove_stopwords(text: str):
        """Remove stopwords from text."""

        stop_words = set(stopwords.words("english"))
        return " ".join([word for word in text.split() if word.lower() not in stop_words])

    @staticmethod
    def lemmatize_text(text: str):
        """Lemmatize text."""

        lemmatizer = WordNetLemmatizer()
        return " ".join([lemmatizer.lemmatize(word) for word in text.split()])

    @staticmethod
    def delete_one_characters(text: str):
        """Delete words with only one character."""

        deleted = [word if len(word) > 1 else "" for word in text.split()]
        final_text = " ".join(deleted)
        return final_text

    @staticmethod
    def remove_outliers(
        data: DataFrame,
        column: str,
        threshold: float = 1.5,
        max_token_length: int | None = None,
        min_token_length: int | None = None,
    ):
        """Remove the outliers."""

        # Calculate q1, q2, and iqr
        token_len = data[column].apply(lambda x: len(str(x).split()))
        q1 = token_len.quantile(0.25)  # First quartile (25th percentile)
        q2 = token_len.quantile(0.75)  # Third quartile (75th percentile)
        iqr = q2 - q1  # Interquartile range

        # Calculate fences
        lower_fence = int(q1 - threshold * iqr)
        upper_fence = int(q2 + threshold * iqr)

        upper_fence = (
            upper_fence
            if max_token_length is None or max_token_length > upper_fence
            else max_token_length
        )
        lower_fence = (
            lower_fence
            if min_token_length is None or min_token_length < lower_fence
            else min_token_length
        )

        return (
            data[(token_len >= lower_fence) & (token_len <= upper_fence)],
            upper_fence,
            lower_fence,
        )

    @staticmethod
    def drop_duplicates(data: DataFrame, column: str) -> DataFrame:
        """Drop duplicate rows based on a specific column."""

        return data.drop_duplicates(subset=[column])

    @staticmethod
    def balanced_data(data: DataFrame, column: str):
        """Balance the data by down sampling the majority class."""

        column_val, count = (
            data.value_counts(column).sort_values().head(1).index[0],
            data.value_counts(column).sort_values().head(1).values[0],
        )
        _df_temp_1 = data[data[column] != column_val].sample(count)
        _df_temp_2 = data[data[column] == column_val]
        return pd.concat([_df_temp_1, _df_temp_2])

    @staticmethod
    def shuffle_data(data: DataFrame, max_size: int | None = None, columns: list[str] = None):
        """Shuffle the data. Use `size` parameter to limit the number of rows."""

        seed = np.random.randint(0, 1000)
        data = data.sample(frac=1, random_state=seed).reset_index(drop=True)
        max_size = data.shape[0] if max_size is None or max_size > data.shape[0] else max_size
        data = data[:max_size]

        # If columns are specified, return only those columns
        if columns is not None:
            return data[columns]
        else:
            return data

        # return data

    @staticmethod
    def remove_small_sentences(data: DataFrame, column: str, size: int = 3):
        """Remove sentences with less than `size` words."""

        return data[data[column].apply(lambda x: len(str(x).split()) >= size)]

    @staticmethod
    def apply_label_encoding(data: DataFrame, columns: list[str]):
        """Apply label encoding to a column."""
        return pd.get_dummies(data, columns=columns, drop_first=True, dtype=int, prefix="is")


class GeneralUtils:

    def __init__(self, input_path, output_path: str | None = None, kagglehub: bool = False):
        self.input_path = input_path
        self.output_path = output_path
        self.kagglehub: bool = kagglehub
        self.kagglehub_dataset_path = None
        self.kagglehub_dataset_name = None

        if kagglehub:
            self.kagglehub_dataset_path, self.kagglehub_dataset_name = input_path.rsplit("/", 1)
            if output_path is None:
                self.output_path = self.kagglehub_dataset_name

        if output_path is None:
            self.output_path = self.input_path

    def load_csv_data(self):
        """Load CSV data from a file."""

        if self.kagglehub:
            return self.load_csv_from_kagglehub(
                self.kagglehub_dataset_path, self.kagglehub_dataset_name
            )
        else:
            return self.load_csv_from_file(self.input_path)

    def save_csv_data(self, data: DataFrame):
        """Save CSV data to a file."""
        data.to_csv(self.output_path, index=False)

    @staticmethod
    def load_csv_from_file(file_path: str):
        """Load CSV data from a file."""

        return pd.read_csv(file_path)

    @staticmethod
    def load_csv_from_kagglehub(path: str, dataset_name: str):
        """Load CSV data from KaggleHub."""

        file_path = kagglehub.dataset_download(path)
        file_path = f"{file_path}/{dataset_name}"
        return GeneralUtils.load_csv_from_file(file_path)
