from src.dataset.event import EventDataset
from functools import cached_property
from pathlib import Path
import pandas as pd
from typing import Dict, List, Union, Tuple
import re
from nltk.tokenize.treebank import TreebankWordDetokenizer as Detok

# Define the order for masking entities
ORDERING = ['X', 'Y', 'Z', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V']

class CometDataset(EventDataset):
    def __init__(self, dir: Path):
        """
        Initialize the CometDataset and pass the directory to the parent class.
        """
        super().__init__(dir)  # Pass 'dir' to the parent class
        self.dir = dir
        self.detokenizer = Detok()

    @cached_property
    def masked_entities(self) -> List[List[Dict[str, Union[str, int]]]]:
        """
        Load and process entity masking information from '.entities' file.
        Returns:
            A list of grouped entity records for masking.
        """
        entity_files = list(self.dir.glob('*.entities'))
        if len(entity_files) != 1:
            raise ValueError("The directory should contain exactly one '.entities' file.")

        data = pd.read_csv(entity_files[0], sep='\t')
        filtered_data = data[(data['cat'] == 'PER') & (data['prop'] != 'NOM')].copy()
        return [group.to_dict('records') for _, group in filtered_data.groupby('COREF')]

    @cached_property
    def token_df(self) -> pd.DataFrame:
        """
        Load and return the token data as a pandas DataFrame from '.tokens' file.
        """
        token_files = list(self.dir.glob('*.tokens'))
        if len(token_files) != 1:
            raise ValueError("The directory should contain exactly one '.tokens' file.")

        return pd.read_csv(token_files[0], sep='\t')

    def _join_str(self, tokens: List[str]) -> str:
        """
        Join tokens into a detokenized string, ensuring proper punctuation spacing.
        Returns:
            A detokenized string with corrected spacing and punctuation.
        """
        text = self.detokenizer.detokenize(tokens)
        text = re.sub(r'\s*,\s*', ', ', text)
        text = re.sub(r'\s*\.\s*', '. ', text)
        text = re.sub(r'\s*\?\s*', '? ', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def _masking(self, words: List[str], is_possessive: List[bool], start_idx: int, end_idx: int) -> str:
        """
        Apply masking to a list of words based on entity positions.
        Args:
            words: List of word tokens.
            is_possessive: List of boolean flags indicating possessive tokens.
            start_idx: Start index of the sentence in the document.
            end_idx: End index of the sentence in the document.
        Returns:
            A string representing the context with entities properly masked.
        """
        assert len(words) == len(is_possessive), "Lengths of 'words' and 'is_possessive' must match."

        for idx, group in enumerate(self.masked_entities):
            for entity in group:
                start, end = entity['start_token'], entity['end_token']
                if start >= start_idx and end <= end_idx:
                    mask = [f'#Person{idx}'] + [''] * (end - start)
                    words[start - start_idx:end - start_idx + 1] = mask

        mask_dict = {}
        order_idx = 0
        output = []

        for word, possessive in zip(words, is_possessive):
            if word.startswith('#Person'):
                if word not in mask_dict:
                    mask_dict[word] = f'Person{ORDERING[order_idx]}'
                    order_idx += 1
                word = mask_dict[word] + "'s" if possessive else mask_dict[word]
            output.append(word)

        return self._join_str(output)

    def _get_context(self, word_id: int) -> Tuple[int, str, str]:
        """
        Retrieve the masked context for the sentence containing a given word ID.
        Args:
            word_id: The ID of the target word in the document.
        Returns:
            A tuple containing the word ID, original context, and masked context.
        """
        context_row = self.token_df[self.token_df['token_ID_within_document'] == word_id]
        sentence_id = context_row['sentence_ID'].iloc[0]
        sentence_data = self.token_df[self.token_df['sentence_ID'] == sentence_id]

        indices = sentence_data['token_ID_within_document'].tolist()
        start_idx, end_idx = indices[0], indices[-1]
        words = sentence_data['word'].tolist()
        is_possessive = list(
            (sentence_data['POS_tag'] == 'PRON') & (sentence_data['dependency_relation'] == 'poss')
        )

        original_context = self._join_str(words)
        masked_context = self._masking(words, is_possessive, start_idx, end_idx)

        return word_id, original_context, masked_context

    @cached_property
    def contexts(self) -> List[Tuple[int, str, str]]:
        """
        Retrieve the masked contexts for all events in the dataset.
        Returns:
            A list of tuples, each containing a word ID, original context, and masked context.
        """
        return [self._get_context(event_id) for event_id in self.events]
