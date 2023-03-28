"""
Decision Tree class and related algorithms
"""
from typing import Optional
from user import User


class DecisionTree:
    """
    A decision tree model for segmenting the population of potential roommates
    based on a given user's personal preferences and data.

    Simple personalized model trained using the CART algorithm, meant for categorization
    to make resonable recommendation.

    Instance Attributes
    ---
    user: the user that the tree is making predictions for. The DecisionTree will access
          its data
    category: the category that each child will split up
    filters: the segmentation of the population based on particular category.
    """
    user: User
    category: str
    _filters: list[tuple[str, DecisionTree]]
