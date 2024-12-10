from unicodedata import normalize
import regex as re
from typing import List, Dict
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def clean(text: str) -> str:
    """
    Strips, normalizes, and removes non-printable characters from the text.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    return re.sub(r'[^\x20-\x7E\u00A0-\u024F]', '', normalize('NFC', text.strip()))

def filter_texts(texts: List[str]) -> List[str]:
    """
    Filters texts containing only Unicode letters.
    """
    return [t for t in map(clean, texts) if not re.search(r'[^\p{L}]', t)]

def display_wordclouds(male_bag_of_words: Dict[str, int],
                       female_bag_of_words: Dict[str, int],
                       title: str,
                       max_words: int = 100) -> None:
    """
    Displays side-by-side word clouds for male and female bag of words.
    
    Args:
        male_bag_of_words (Dict[str, int]): Bag of words for male characters.
        female_bag_of_words (Dict[str, int]): Bag of words for female characters.
        title (str): Title of the plot.
        max_words (int, optional): Maximum number of words to display in the word clouds. Defaults to 100.
    """
    # Generate word clouds
    wordcloud_female = WordCloud(
        width=400, 
        height=400, 
        background_color='white',
        colormap='Reds',
        max_words=max_words
    ).generate_from_frequencies(female_bag_of_words)

    wordcloud_male = WordCloud(
        width=400, 
        height=400, 
        background_color='white',
        colormap='Blues',
        max_words=max_words
    ).generate_from_frequencies(male_bag_of_words)

    # Create the figure and axes
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(title, fontsize=18, weight='bold')

    # Display the female word cloud
    axes[0].imshow(wordcloud_female, interpolation='bilinear')
    axes[0].set_title("Female Characters", fontsize=14)
    axes[0].axis('off')

    # Display the male word cloud
    axes[1].imshow(wordcloud_male, interpolation='bilinear')
    axes[1].set_title("Male Characters", fontsize=14)
    axes[1].axis('off')

    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Leaves space for the title
    plt.show()
