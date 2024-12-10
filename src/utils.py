from unicodedata import normalize
import regex as re
from typing import List, Dict

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

def show_wordcloud(male_bag_of_words : Dict[str, int],
                   female_bag_of_words : Dict[str, int],
                   title : str,
                   max_words : int = 100):
  wordcloud_female = WordCloud(
    width=400, 
    height=400, 
    background_color='white',
    colormap = 'Reds',
    ).generate_from_frequencies(female_bag_of_words)
  
  wordcloud_male = WordCloud(
    width=400, 
    height=400, 
    background_color='white',
    colormap = 'Blues',
    ).generate_from_frequencies(male_bag_of_words)

  # Display the word clouds side by side
  fig, axes = plt.subplots(1, 2, figsize=(10, 5))
  fig.suptitle(title, fontsize=16)

  # Female verbs word cloud
  axes[0].imshow(wordcloud_female, interpolation='bilinear')
  axes[0].set_title("Female Characters")
  axes[0].axis('off')

  # Male verbs word cloud
  axes[1].imshow(wordcloud_male, interpolation='bilinear')
  axes[1].set_title("Male Characters")
  axes[1].axis('off')

  plt.tight_layout()
  plt.show()
