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

    TODO:
        - Create the partitions based on a better learning algorithm; see ID.3, CART.
          Will need a metric like the Gini Impurity or Information Gain (see Wikipedia).
        - 

    Implementation Notes for Andrew
    ---
    - Think of the data array that you are passed as a table with rows and columns.
      Each column is a category that we are dividing into a bunch of groups based on
      values in the column. For continuous variables this will be a continuous interval,
      where as for categorical variables we will be splitting based on each value (i.e T
      or F, values from 1-5 etc.)
    - _partition will give you a list of these grouped users, as well as a decision tree
      to add as a child node.
    - We slice the array to reduce the number of columns by 1 each recursive call. Each
    depth will be partitions on a different category.
    - Assume that the id of each user will be the first item.
    - In my mind, each leaf will correspond to one group of users. We can then use the
      predicted group of each user to label them in a database, then when a user tries
      to get a match, the decision tree will categorize them, then look up all other
      users with the same label in the database for recommendation.

    Instance Attributes
    ---
    user: the user that the tree is making predictions for. The DecisionTree will access
          its data
    category: the category that each child will split up
    _partitions: the segmentations of the population based on the current particular category.
    """
    prev_subtrees: list[DecisionTree]
    category: str
    partitions: list[DecisionTree]

    # def __init__(self, user: User):
    #     self.user = user
    #     # self.user.tree = self

    # def add_groups(self, groups: list[tuple[str, DecisionTree]])) -> None:
        # return None

    def train(self, data: ArrayLike, category_names: list[str] = None) -> DecisionTree:
        if category_names == []:
            return [self]
        else:
            self._category = cat_name
            is_categorical = not any(isinstance(data[:, 0], tp) for tp in continuous_types)
            partitions = self._partition(data[:, 0], category_name[0])

            for partition in partitions:
                subtree, data = partition
                partitions.append(subtree)
                subtree.train(data, category_names[1:])

            return self

    def partition(self, column: np.ndarray, continuous: bool) -> list[tuple[DecisionTree, np.ndarray]]:
        num_partitions = 8
        partitions = []
        if self.partitions == []:
          return self
        if continuous:
            min_val = np.min(column)
            max_val = np.max(column)

            partition_size = (max_val - min_val) / num_partitions

            cur_min = min_val
            for p in range(num_partitions):
                partitioned_data = column[cur_min <= column <= cur_min + partition_size * p]
                partitions.append((DecisionTree(), partitioned_data))
        else:
          for partition in self._partitions:
            tree = [self]
            subtree = partition.partition
            partitions.append(subtree)
            tree.extend(subtree)
            partitions.append(tree)

          return partitions

        # Add the case for categorical data, should be easier
        # Hint: np.unique should help in this case
        else:

        return partitions
