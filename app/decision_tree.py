"""
Decision Tree class and related algorithms
"""
from __future__ import annotations
from user import User
import math
from typing import Optional
from python_ta.contracts import check_contracts
import csv


# @check_contracts
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
    decision: Optional[str | int | tuple[int, ...] | bool]
    users: Optional[list[User]]
    partitions: dict[str | int | tuple[int, ...] | bool, DecisionTree]

    # def __init__(self, user: User):
    #     self.user = user
    #     # self.user.tree = self
    # @check_contracts
    def __init__(self, category: str, initial_users: Optional[list[User]] = None) -> None:
        self.category = category
        self.decision = None
        self.partitions = {}
        self.users = initial_users

    # @check_contracts
    def get_partitions(self) -> list[DecisionTree]:
        """Return the partitions of this decision tree."""
        return list(self.partitions.values())

    # @check_contracts
    def add_user_to_tree(self, user_to_add: User) -> None:
        """
        This method takes a user and finds their preferences, and then adds them to a leaf that is at the end of a path
        from the root node by calling a helper function that recurses into the tree
        """
        preferences = get_user_preferences(user_to_add)
        self.add_user_to_tree_recursively(user_to_add, preferences)

    # @check_contracts
    def add_user_to_tree_recursively(self,
                                     user_to_add: User,
                                     user_preferences: list[int | str | tuple[int, ...] | bool]) -> None:
        """
        This helper method takes a list of user preferences in order (it will be assumed to always be in order)
        and recurses into the tree to add them in a leaf
        """
        if user_preferences == []:
            if self.users is None:
                self.users = [user_to_add]
            else:
                self.users.append(user_to_add)
            return
        else:
            preference = user_preferences[0]
            if len(user_preferences) == 7:
                if preference:
                    gender = user_to_add.gender.lower()
                    self.partitions[gender].add_user_to_tree_recursively(user_to_add, user_preferences[1:])
                else:
                    self.partitions["any"].add_user_to_tree_recursively(user_to_add, user_preferences[1:])
            else:
                self.partitions[preference].add_user_to_tree_recursively(user_to_add, user_preferences[1:])

    # @check_contracts
    def find_exact_matches(self, user_: User) -> list[User]:
        """
        This method takes a user and finds their preferences, and then finds the leaf (that is at the end of a
        path from the root node) containing the users that have the exact same preferences by calling a helper
        function that recurses into the tree
        """
        preferences = get_user_preferences(user_)
        matches = self.find_exact_matches_recursively(user_, preferences)
        return matches

    # @check_contracts
    def find_exact_matches_recursively(self,
                                       user_: User,
                                       user_preferences: list[int | str | tuple[int, ...] | bool]) -> list[User]:
        """
        Recursively goes through the decision tree using the user's preferences, until it reaches a leaf
        with the list of all users that exactly matches the user's preferences, if none are found an empty list
        is returned instead
        """
        if user_preferences == []:
            if user_ in self.users:
                copy_of_users = self.users.copy()
                copy_of_users.remove(user_)
                return copy_of_users
            return self.users
        else:
            preference = user_preferences[0]
            if len(user_preferences) == 7:
                if preference:
                    gender = user_.gender.lower()
                    matches = self.partitions[gender].find_exact_matches_recursively(user_, user_preferences[1:])
                else:
                    matches = self.partitions["any"].find_exact_matches_recursively(user_, user_preferences[1:])
            else:
                matches = self.partitions[preference].find_exact_matches_recursively(user_, user_preferences[1:])
            return matches

    # @check_contracts
    def find_closest_matches(self, user_: User) -> list[User]:
        """
        This method takes a user and finds their preferences, and then finds the leaf (that is at the end of a
        path from the root node) containing the users that have the exact same preferences by calling a helper
        function that recurses into the tree. If none are found, it goes back one node, and recurses into the next
        leaf to find the next closest match, as the preferences are ordered top down from most to least important.
        If none are found in that node's subtrees, then it goes back again to the previous node and tries again
        from that node until it reaches a hard stop at gender preferences and no matches are returned
        """
        preferences = get_user_preferences(user_)
        matches = self.find_closest_matches_recursively(user_, preferences)
        return matches

    # @check_contracts
    def find_closest_matches_recursively(
        self,
            user_: User, user_preferences: list[int | str | tuple[int, ...] | bool]) -> list[User]:
        """
        Recursively goes through the decision tree using the user's preferences, until it reaches a leaf
        with the list of all users that exactly matches the user's preferences by accessing the other subtrees,
        if none are found an empty list is returned instead
        """
        if user_preferences == []:
            if user_ in self.users:
                copy_of_users = self.users.copy()
                copy_of_users.remove(user_)
                return copy_of_users
            return self.users
        else:
            preference = user_preferences[0]
            if len(user_preferences) == 7:
                if preference:
                    gender = user_.gender.lower()
                    matches = self.partitions[gender].find_closest_matches_recursively(user_, user_preferences[1:])
                else:
                    matches = self.partitions["any"].find_closest_matches_recursively(user_, user_preferences[1:])
            else:
                matches = self.partitions[preference].find_closest_matches_recursively(user_, user_preferences[1:])
            if matches == []:
                if len(user_preferences) >= 7:
                    return matches
                else:
                    partitions_copy = self.partitions.copy()
                    partitions_copy.pop(preference)
                    for alt_pref in partitions_copy:
                        matches = self.partitions[alt_pref].find_closest_matches_recursively(user_, user_preferences[1:])
                        if matches != []:
                            return matches
        return matches


# @check_contracts
def build_decision_tree(preferences: list[tuple[str, tuple[int | str | tuple[int, ...] | bool, ...]]],
                        decision: Optional[str | int | tuple[int, ...] | bool]) -> DecisionTree:
    """
    A function that builds the decision tree for us by creating then recursing into its partitions (subtrees),
    following an already set order of choices starting from an empty root node that decies between rent range, then
    gender preferences, and then the following choices in order from most to least important: number of roommates,
    pets, cleanliness, guests, smoking, and finally noise.
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
            curr_node.partitions[choice] = subtree
        return curr_node


# @check_contracts
def read_file(preferences_file: str) -> list[tuple[str, tuple[int | str | tuple[int, ...] | bool, ...]]]:
    """
    Reads a csv file with the preferences and the possible options on each row, returning a list containing
    a tuple that stores the preference name, and the possible choices in a tuple as the choices and all
    possible preferences are concrete and should not be changed.
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
        rent_ranges = tuple(rent_ranges + [(3201, 12000)])
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


# @check_contracts
def get_user_preferences(user_: User) -> list[int | str | tuple[int, ...] | bool]:
    """
    Returns a list of the user's preferences in the same order as seen in the decision_tree
    """
    rent_ranges = ( (0, 800),
        (801, 1100), (1101, 1400), (1401, 1700),
        (1701, 2000), (2001, 2300), (2301, 2600),
        (2601, 2900), (2901, 3200), (3201, math.inf)
    )
    user_rent_range = None
    mid = (user_.rent[0] + user_.rent[1]) // 2
    for low, high in rent_ranges:
        if low <= mid <= high:
            user_rent_range = (low, high)
            break

    return [user_rent_range, user_.gender_pref, user_.num_roommates, user_.pets,
            user_.cleanliness, user_.guests, user_.smoke, user_.noise]


# @check_contracts
def get_users_preferences(users: list[User]) -> list[list[int | str | tuple[int, ...] | bool]]:
    """
    Returns a list of users preferences
    """
    preferences = []
    for user in users:
        preference = get_user_preferences(user)
        preferences.append(preference)
    return preferences


if __name__ == '__main__':
    parameters = read_file("csv_files/decision_tree_parameters.csv")
    decision_tree = build_decision_tree(parameters, None)

    import user
    file = 'csv_files/big_test.csv'
    users = user.csv_read(file)# list of users
    for u in users[:10]:
        decision_tree.add_user_to_tree(u)
    new_user = User("a", "user", 12, 1, "Male", True, True, (1401, 1700), False, "nah", None, 2, True, 2, 3)
    print(get_user_preferences(new_user))
    decision_tree.add_user_to_tree(new_user)
    new_user = User("b", "user", 100, 1, "Male", True, True, (1401, 1700), True, "nah", None, 2, True, 2, 2)
    print(get_user_preferences(new_user))
    decision_tree.add_user_to_tree(new_user)
    user_to_match = users[0]
    print(get_user_preferences(user_to_match))
    print("------")
    matches_tree = decision_tree.find_closest_matches(user_to_match)
    print(matches_tree)
