from pandas import DataFrame

from .utils import TextPreprocessingUtils, GeneralUtils


class TextPreprocessor:
    def __init__(
        self,
        input_path,
        output_path: str | None = None,
        max_token_length: int | None = 500,
        min_token_length: int | None = 3,
        max_size: int | None = 50000,
        kagglehub: bool = False,
        **kwargs,
    ):
        self.output_path = output_path
        self.max_token_length = max_token_length
        self.min_token_length = min_token_length
        self.max_size = max_size

        self.processor_utils = TextPreprocessingUtils()
        self.general_utils = GeneralUtils(input_path, output_path, kagglehub)

        # Download necessary NLTK resources
        self.processor_utils.download_nltk_resources()

        # Load data
        self.data = self.general_utils.load_csv_data()

    def preprocess(self, input_column: str = "text", output_column: str = "label") -> DataFrame:
        """
        Preprocess the text column in the dataframe.

        :param input_column: Name of the text column to preprocess
        :param output_column: Name of the output column
        :return: Preprocessed dataframe
        """

        columns = [input_column, output_column]
        missing_columns = [col for col in columns if col not in self.data.columns]
        if missing_columns:
            raise KeyError(
                f"The following columns are missing from the DataFrame: {missing_columns}"
            )

        # Select columns
        self.data = self.data[columns]
        # Remove duplicates
        self.data = self.processor_utils.drop_duplicates(self.data, input_column)
        # Check if the columns exist in the DataFrame

        # Preprocess text
        self.data[input_column] = self.data[input_column].apply(self._process_single_text)

        # Remove sentences with more than `max_token_length` words and less than `min_token_length` words
        self.data, self.max_token_length, self.min_token_length = (
            self.processor_utils.remove_outliers(
                self.data,
                input_column,
                max_token_length=self.max_token_length,
                min_token_length=self.min_token_length,
            )
        )

        # Remove sentences with less than `size` words
        self.data = self.processor_utils.balanced_data(self.data, output_column)

        self.data = self.processor_utils.apply_label_encoding(self.data, [output_column])

        self.data = self.processor_utils.shuffle_data(self.data, self.max_size)

        return self.data

    def _process_single_text(self, text):
        """
        Process a single text string through multiple preprocessing steps.

        :param text: Input text
        :return: Preprocessed text
        """
        if not isinstance(text, str):
            return text

        # Preprocessing pipeline
        text = self.processor_utils.remove_html_tags(text)
        text = self.processor_utils.gensim_preprocess(text)
        text = self.processor_utils.remove_stopwords(text)
        text = self.processor_utils.lemmatize_text(text)
        text = self.processor_utils.delete_one_characters(text)

        return text.strip()

    def save(self):
        """Save the preprocessed dataframe to a CSV file."""

        self.general_utils.save_csv_data(self.data, self.output_path)
