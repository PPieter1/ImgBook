"""A collection of functions to generate summaries from epub files."""

import ebooklib
from ebooklib import epub

from summarizer import Summarizer, TransformerSummarizer

from bs4 import BeautifulSoup

from tqdm.notebook import tqdm

# Function to read ePub file
def __read_epub_file__(filename):
    """Reads the ePub file and returns the book object."""
    book = epub.read_epub(filename)
    return book

# Function to get document items from the book object
def __get_document_items__(book):
    """Extracts the document items from the book object."""
    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    return items

# Function to parse a chapter and extract its text
def __parse_chapter__(chapter):
    """Parses the content of a chapter using BeautifulSoup and returns the text as a string."""
    soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
    paragraphs = soup.find_all('p')
    text = []
    for p in paragraphs:
        text.append(p.get_text())
    return ' '.join(text)

# Function to process chapters and store their contents in a dictionary
def __process_chapters__(items):
    """Processes all chapters and stores their contents in a dictionary."""
    texts = {}
    for c in items:
        texts[c.get_name()] = __parse_chapter__(c)
    return texts

# Function to get the book dictionary
def __get_book_dict__(book_path):
    """Returns a dictionary containing the text of each chapter in the ePub file."""
    book = __read_epub_file__(book_path)
    items = __get_document_items__(book)
    text_dict = __process_chapters__(items)
    return text_dict

def __split_string__(input_string, part_length):
    if len(input_string) < part_length:
        #raise ValueError("The input string's length must be greater than the part length.")
        return ['']
        
    """Splits the input string into parts of the specified length."""
    parts = list(map(''.join, zip(*[iter(input_string)] * part_length)))
    if len(input_string) % part_length != 0:
        parts[-1] = parts[-1] + input_string[len(parts) * part_length:]
    return parts

# Class to handle text summarization
class __TextSummarizer__:
    """Handles text summarization using pre-trained models."""
    def __init__(self, transformer_type='XLNet', transformer_model_key='xlnet-base-cased'):
        """Initializes the TextSummarizer with the specified transformer type and model key."""
        self.model = TransformerSummarizer(transformer_type=transformer_type, transformer_model_key=transformer_model_key)

    def generate_summary(self, text, min_length=60, max_length=300):
        """Generates a summary based on the input text and the specified minimum and maximum lengths."""
        summary = ''.join(self.model(text, min_length=min_length, max_length=max_length))
        return summary

def summarize_ebook(ebook_path, part_length, transformer_type='XLNet', transformer_model_key='xlnet-base-cased'):
    """Generates summaries of parts of the ebook's chapters."""
    # Get the book dictionary
    text_dict = __get_book_dict__(ebook_path)

    # Initialize the TextSummarizer
    summarizer = __TextSummarizer__(transformer_type=transformer_type, transformer_model_key=transformer_model_key)

    # Generate summaries for each chapter
    summarized_chapters = {}
    for chapter_title, chapter_text in tqdm(text_dict.items(), desc='Chapters', position=0): # note: tqdm wrapper provides progress bar
        # Split the chapter text into parts
        parts = __split_string__(chapter_text, part_length)

        # Generate summaries for each part
        summary_parts = list()
        for index, part in enumerate(tqdm(parts, desc='Chapter Parts', position=1, leave=False)):
            summary = summarizer.generate_summary(part, min_length=60, max_length=300)
            summary_parts.append(summary)

        # Store the summarized chapter
        summarized_chapters[chapter_title] = summary_parts

    return summarized_chapters
