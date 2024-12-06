# Nlator

Nlator is a simple Python package for translating text between multiple languages and detecting the language of a given text. It uses the Google Translate API for its functionality.

## Installation

You can install the package using pip:

```bash
pip install nlator
```

## Usage

Here are some examples of how to use the Nlator package:

# Importing The Package
```python
import nlator
```

## Translating Text

To translate text from one language to another, you can use the `translate` method. For example, to translate "Hello" from English to Spanish:

```python
translator = nlator.Nlator()
hello_es = translator.translate("Hello", from_lang="en", to_lang="es")
print(hello_es)  # Output: Hola
```

## Detecting Language

You can also detect the language of a given text using the `findlanguage` method. For example, to detect the language of the word "ciao":

```python
language = translator.findlanguage("ciao")
print(language)  # Output: it (Italian)
```

## Supported Languages
The package supports a wide range of languages. You can find the list of supported languages in the https://cloud.google.com/translate/docs/languages