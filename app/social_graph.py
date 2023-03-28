"""
Social graph connecting user matches
"""
from __future__ import annotations

from user import User
from python_ta.contracts import check_contracts


@check_contracts
class _User:
    """
    vertex of the graph representing each user
    """
    item: User
    matches: set[_User]

    def __init__(self, item: User, matches: set[_User]):
        self.item = item
        self.matches = matches


@check_contracts
class Network:
    """
    The graph representing the network of matches betwen users
    """
    _users: dict[User, _User]

    def __init__(self) -> None:
        """
        Initialized an empty network
        """
        self._users = {}

    def add_user(self, user: User) -> None:
        """
        add user to given graph

        Preconditions:
            - user not in self._users
        """
        self._users[user] = _User(user, set())

    def add_connection(self, user1: User, user2: User) -> None:
        """
        add a match/ connection between 2 users

        Preconditions:
            - user1 != user2
        """
        if user1 in self._users and user2 in self._users:
            u1 = self._users[user1]
            u2 = self._users[user2]

            u1.matches.add(u2)
            u2.matches.add(u1)
        else:
            raise ValueError

    def check_connection(self, user1: User, user2: User) -> bool:
        """
        check whether 2 users have a connection/ matched
        """
        if user1 in self._users and user2 in self._users:
            u1 = self._users[user1]
            return any(u2.item == user2 for u2 in u1.matches)
        else:
            return False

    def get_matches(self, user: User) -> set:
        """
        return a set of matches of the give user
        """
        if user in self._users:
            u = self._users[user]
            return {match.user for match in u.matches}
        else:
            raise ValueError


def create_network(matches: list[dict[User, set[User]]]) -> Network:
    """
    create a network from matches
    """
    my_network = Network
    for match in matches:
        ...
