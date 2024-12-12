from src.dataset.event import EventDataset
from functools import cached_property
from pathlib import Path
import pandas as pd
from typing import Dict, List, Union, Tuple
import re
import string
from nltk.tokenize.treebank import TreebankWordDetokenizer as Detok

def get_variable_name(index):
    base_vars = ['X', 'Y', 'Z', 'W', 'U', 'V']  # Initial set of variables in uppercase
    all_letters = [chr(i).upper() for i in range(ord('a'), ord('z') + 1)]  # All uppercase letters
    extended_vars = [var for var in all_letters if var not in base_vars]  # Exclude already used
    full_vars = base_vars + extended_vars  # Combine base variables and remaining letters
    
    # Calculate the base index and suffix
    base_index = index % len(full_vars)
    suffix = index // len(full_vars)
    
    # Return the variable name with or without a suffix
    return f"{full_vars[base_index]}{suffix}" if suffix > 0 else full_vars[base_index]

class CometDataset(EventDataset):
    def __init__(self, dir: Path):
        """
        Initialize the CometDataset and pass the directory to the parent class.
        """
        super().__init__(dir)  # Pass 'dir' to the parent class
        self.dir = dir
        self.detokenizer = Detok()
    
    @cached_property
    def entity_df(self) -> pd.DataFrame:
        """
        Load and return the entity data as a pandas DataFrame from '.entities' file.
        """
        entity_files = list(self.dir.glob('*.entities'))
        if len(entity_files) != 1:
            raise ValueError("The directory should contain exactly one '.entities' file.")

        return pd.read_csv(entity_files[0], sep='\t', engine='python', quoting=3)
        
    @cached_property
    def masked_entities(self) -> List[List[Dict[str, Union[str, int]]]]:
        """
        Load and process entity masking information from '.entities' file.
        Returns:
            A list of grouped entity records for masking.
        """
        condition = (
            (self.entity_df['prop'] != 'NOM') |
            (self.entity_df['text'].str.lower().str.startswith('the ')) |
             (self.entity_df['text'].str.split().str.len() < 3)
             )
        # Filter and copy relevant data
        filtered_data = self.entity_df[(self.entity_df['cat'] == 'PER') & condition].copy()
        # Group by 'COREF' and convert each group to a list of dictionaries
        return [group.to_dict('records') for _, group in filtered_data.groupby('COREF')]

    @cached_property
    def token_df(self) -> pd.DataFrame:
        """
        Load and return the token data as a pandas DataFrame from '.tokens' file.
        """
        token_files = list(self.dir.glob('*.tokens'))
        if len(token_files) != 1:
            raise ValueError("The directory should contain exactly one '.tokens' file.")

        # Read the .tokens file into a DataFrame
        df = pd.read_csv(token_files[0], sep='\t', engine='python', quoting=3)

        # Validate that the row count matches the maximum token ID in the document
        if df.shape[0] != df['token_ID_within_document'].tolist()[-1] + 1:
            raise ValueError("The token DataFrame row count does not match the maximum token ID in the document.")

        return df

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
                    # Check if there is any False in the slice
                    if not all(is_possessive[start - start_idx:end - start_idx + 1]):
                      # Set all values in the slice to False
                      is_possessive[start - start_idx:end - start_idx + 1] = [False] * (end - start + 1)
                    

        mask_dict = {}
        order_idx = 0
        output = []
        
        for word, possessive in zip(words, is_possessive):
            if word.startswith('#Person'):
                if word not in mask_dict:
                    mask_dict[word] = f'Person{get_variable_name(order_idx)}'
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
        words = sentence_data['word'].astype(str).tolist()
        is_possessive = list(
            (sentence_data['POS_tag'] == 'PRON') & 
            ((sentence_data['dependency_relation'] == 'poss') | (sentence_data['dependency_relation'] == 'attr'))
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
