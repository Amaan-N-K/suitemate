"""
Decision Tree class and related algorithms
"""
import numpy as np

from typing import Optional
from numpy.typing import ArrayLike
from user import User

CONTINUOUS_TYPES = {np.float, float}

class DecisionTree:
    """
    A decision tree model for segmenting the population of potential roommates
    based on a given user's personal preferences and data.

    Simple personalized model trained using the CART/ID/5 (whatever will work best) algorithm, 
    meant for categorization to make resonable recommendation.

    Instance Attributes
    ---
    user: the user that the tree is making predictions for. The DecisionTree will access
          its data
    category: the category that each child will split up
    _partitions: the segmentations of the population based on the current particular category.
    """
    user: User
    category: str
    _partitions: list[tuple[str, DecisionTree]]

    def __init__(self, user: User):
        self.user = user
        # self.user.tree = self

    # def add_groups(self, groups: list[tuple[str, DecisionTree]])) -> None:
        # return None

    def train(self, data: ArrayLike, category_names: list[str] = None) -> DecisionTree:
        if category_names == []:
            return self
        else:
            self._category = cat_name
            is_categorical = not isinstance(data[:, 0])
            partitions = self._partition(data[:, 0], category_name[0])

            for partition in partitions:
                return self.train(data[:, 1:], category_names[1:])
            return self

    def _partition(self, column: np.ndarray) -> list[np.ndarray]:
        num_partitions = 8
        if any(tp == column.dtype for tp in CONTINUOUS_TYPES):
            min_val = np.min(column)
            max_val = np.max(column)

            partition_size = (max_val - min_val) / num_partitions


