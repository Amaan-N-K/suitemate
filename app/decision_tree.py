"""
Decision Tree class and related algorithms
"""
import numpy as np

from typing import Optional
from numpy.typing import ArrayLike
from user import User
from python_ta.contracts import check_contracts
import csv

CONTINUOUS_TYPES = {np.float, float}

@check_contracts
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
    # prev_subtrees: list[DecisionTree] I don't think this is necessary
    category: Optional[str]
    decision: Optional[str | int | tuple[int | str, ...] | bool]
    users: Optional[list[User]]
    partitions: list[DecisionTree]

    # def __init__(self, user: User):
    #     self.user = user
    #     # self.user.tree = self
    @check_contracts
    def __init__(self, category: str, users: Optional[list[User]] = None) -> None:
       self.category = category
       self.decision = None
       self.partitions = [] 
       self.users = users

    # def add_groups(self, groups: list[tuple[str, DecisionTree]])) -> None:
        # return None
    @check_contracts
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
    @check_contracts
    def add_subtree(self, category: str): #since the decision tree is built and concrete, we likely don't need this
      pass


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
        # else:

        return partitions

@check_contracts
def build_decision_tree(preferences: list[tuple[str, tuple[int | str | tuple[int | str, ...] | bool, ...]]], 
                        decision: Optional[str | int | tuple[int | str, ...]]) -> DecisionTree:
  """
  A function that builds the decision tree for us, following an already set order of choices starting from an empty root 
  node that decides location, then gender preferences, then rent range, and the following choices in order from most to
  least important: number of room mates, pets, cleanliness, guests, smoking, and finally noise.
  """
  if preferences == []:
    subtree = DecisionTree("users", [])
    subtree.decision = decision
    return subtree
  else:
    curr_preference = preferences[0]
    category = curr_preference[0]
    curr_node = DecisionTree(category)
    curr_node.decision = decision
    choices = curr_preference[1]
    for choice in choices:
      subtree = build_decision_tree(preferences[1:], choice)
      curr_node.partitions.append(subtree)
    return curr_node
      
        



if str.isnumeric():
  # make it into a integer
  pass

@check_contracts
def read_file(preferences_file: str) -> list[tuple[str, tuple[int | str | tuple[int | str, ...] | bool, ...]]]:
    """
    Reads a csv file with the preferences and the possible options on each row, returning a list containing a tuple that stores
    the preference name, and the possible choices in a tuple as the choices and all possible preferences are concrete and should
    not be changed. 
    """
    preferences = []
    with open(preferences_file) as file:
        reader = csv.reader(file)

        rent_row = next(reader)
        category = rent_row[0]
        rent_ranges = []
        for i in range(1, len(rent_row) - 1, 2):
          rent_lower_bound = int(rent_row[i])
          rent_upper_bound = int(rent_row[i + 1])
          rent_range = (rent_lower_bound, rent_upper_bound)
          rent_ranges.append(rent_range)
        rent_ranges = tuple(rent_ranges)
        preferences.append((category, rent_ranges))

        for row in reader:
          category = row[0]
          if category in ("roommates", "cleanliness", "noise"):
            choices = []
            for item in row[1:]:
              choice = int(item)
              choices.append(choice)
            choices = tuple(choices)
          elif category in ("pets", "smoking", "guests"):
            choices = (True, False)
          else:
            choices = tuple(row[1:])
          preferences.append((category, choices))

    return preferences