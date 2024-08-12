import numpy as np
import torch
from transformers import BertModel, BertTokenizer


class BertEncoder:
    """
    BertEncoder helps to apply BERT encodings to text.
    """

    def __init__(self) -> None:
        """
        Initialize BertEncoder with the BERT tokenizer and model.
        """
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.model = BertModel.from_pretrained("bert-base-uncased")

    def encode(self, text: str) -> np.ndarray:
        """
        Encodes a given string of text.

        Args:
            text (str): The text to encode.

        Returns:
            np.ndarray: Vector representation of the given text.
        """
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.squeeze().mean(dim=0).numpy()
