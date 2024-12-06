# Text Preprocessor

## 📝 Overview

Text Preprocessor is a powerful Python library designed for comprehensive text preprocessing tasks, particularly useful for natural language processing (NLP), sentiment analysis, and text classification projects.

## ✨ Features

- 🧹 Remove HTML tags
- 🛑 Remove stopwords
- 🔤 Lemmatization
- 🧼 Remove special characters
- 🔍 Remove duplicates
- 📏 Remove short texts
- 📊 Basic outlier detection

## 🚀 Installation

### Using pip
```bash
pip install sentence-preprocessor
```

### Using Poetry
```bash
poetry add sentence-preprocessor
```

## 💻 Usage

### As a Python Module
```python
from text_preprocessor.preprocessor import TextPreprocessor

# Preprocess a CSV file
preprocessor = TextPreprocessor('input.csv', 'output.csv')
preprocessed_df = preprocessor.preprocess()
preprocessor.save_preprocessed_data()
```

### Command Line Interface
```bash
# Basic usage
text_preprocessor input.csv [output.csv]
```

## 🛠 Development Setup

### Prerequisites
- Python 3.12+
- Poetry

### Installation Steps
```bash
# Install Poetry (if not already installed)
pip install poetry

# Install dependencies
make install

# Activate virtual environment
make shell
```

## 🧪 Running Tests
```bash
# Run tests
make test

# Run tests with coverage
make test-cov
```

## 📦 Build and Publish
```bash
# Build distribution
make build

# Publish to PyPI
make publish
```

## 🔍 Preprocessing Pipeline

The preprocessor applies the following transformations:
1. Remove HTML tags
2. Convert to lowercase
3. Remove special characters
4. Remove stopwords
5. Lemmatize text
6. Remove single characters
7. Remove texts with fewer than 3 words
8. Remove duplicates
9. Basic outlier detection

## 📝 Configuration

You can customize preprocessing by modifying the `preprocess()` method parameters or extending the `TextPreprocessingUtils` class.

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute to this project, please open an issue or submit a pull request.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🛡 Disclaimer

This library is provided as-is. Always review and test thoroughly before using in production environments.

## 📞 Contact

Your Name - your.email@example.com

Project Link: 

## 🙌 Acknowledgements
- [NLTK](https://www.nltk.org/)
- [Pandas](https://pandas.pydata.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

**Star ⭐ the repository if this project helps you!**