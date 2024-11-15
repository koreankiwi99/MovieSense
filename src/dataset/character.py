from functools import cached_property
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
from tqdm import tqdm
from collections import Counter, defaultdict

GENDER_DICT = {'he/him/his' : 'male', 
               'she/her' : 'female', 
               'they/them/their' : 'plural',
               'ze/zem/zir/hir' : 'neutral', 
               'unknown' : 'unknown'}

class Character:
    """
    A class representing a character in a novel.
    """
    def __init__(self, item_dict: Dict[str, str]):
        """Initializes a Character with attributes extracted from a dictionary."""
        self.gender = self.get_gender(item_dict.get('g'))
        self.count = item_dict.get('count', 0)
        self.mentions = item_dict.get('mentions', [])
        self.poss_id, self.poss_word = self._strip(item_dict.get('poss', []))
        self.agent_id, self.agent_word = self._strip(item_dict.get('agent', []))
        self.patient_id, self.patient_word = self._strip(item_dict.get('patient', []))
        self.mod_id, self.mod_word = self._strip(item_dict.get('mod', []))

    def _strip(self, id_with_word: List[Dict[str, str]]) -> Tuple[List[str], List[str]]:
        """
        Extracts IDs and words from a list of dictionaries.
        """
        ids, words = [], []
        for item in id_with_word:
            ids.append(item.get('i', ''))
            words.append(item.get('w', ''))
        return ids, words

    def get_gender(self, gender: Optional[Dict[str, str]]) -> str:
        """
        Determines the gender of the character based on the provided gender dictionary.
        """
        if gender is not None and 'argmax' in gender:
            return GENDER_DICT.get(gender['argmax'], 'unknown')
        return 'unknown'


class CharacterDataset:
    def __init__(self, dir: Path):
        """Initializes the CharacterDataset with a directory path containing character files."""
        self.dir = dir
  
    def _load_json(self, path: Path) -> dict:
        """Loads a JSON file and returns its content."""
        with open(path) as file:
            data = json.load(file)
        return data
  
    @cached_property
    def characters(self) -> list:
        """Loads characters from a single JSON file in the directory and returns them as Character objects."""
        path = list(self.dir.glob('*.book'))
        if len(path) != 1:
            raise ValueError("The directory should contain exactly one '.book' file.")
        return [Character(character_data) for character_data in self._load_json(path[0])['characters']]
  
    def __len__(self) -> int:
        """Returns the number of characters in the dataset."""
        return len(self.characters)
  
    @cached_property
    def gender_count(self) -> Counter:
        """Returns a count of characters by gender."""
        return Counter(ch.gender for ch in self.characters)
  
    @property
    def gender_ratio(self) -> dict:
        """Calculates the gender ratio by dividing the gender count by the total number of characters."""
        total_characters = len(self)
        return {gender: count / total_characters for gender, count in self.gender_count.items()}
  
    @cached_property
    def gender_count_mention(self) -> defaultdict:
        """Returns a dictionary with gender as keys and a list of mention counts as values."""
        count_sum = defaultdict(list)
        for ch in self.characters:
            count_sum[ch.gender].append(ch.count)
        return count_sum
  
    @property
    def gender_ratio_mention(self) -> dict:
        """Calculates the average mention count per character by gender."""
        return {gender: sum(counts) / len(counts) for gender, counts in self.gender_count_mention.items() if counts}
  
    @property
    def gender_sum_mention(self) -> dict:
        """Returns the total mention count for each gender."""
        return {gender: sum(counts) for gender, counts in self.gender_count_mention.items()}
