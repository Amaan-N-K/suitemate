"""
Social graph connecting user matches
"""
from __future__ import annotations
from typing import Optional
from user import User
from python_ta.contracts import check_contracts


@check_contracts
class _User:
    """
    vertex of the graph representing each user
    """
    item: User
    user_id: int
    suggestions: set[_User]
    matches: Optional[set[_User]] = set()
    requests: Optional[set[_User]] = set()

    def __init__(self, item: User, suggestions: set[_User]) -> None:
        self.item = item
        self.user_id = item.id
        self.suggestions = suggestions
        self.matches = set()
        self.requests = set()

    def accept_request(self, id_num: int) -> None:
        """
        move request to match.
        """
        for user in self.requests:
            if user.user_id == id_num:
                self.requests.remove(user)
                self.matches.add(user)
                return

    def send_request(self, id_num: int) -> None:
        """
        move suggestion to request
        """
        for user in self.requests:
            if user.user_id == id_num:
                self.suggestions.remove(user)
                self.requests.add(user)
                return


@check_contracts
class Network:
    """
    The graph representing the network of matches betwen users
    """
    _users: dict[int, _User]

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
        self._users[user.id] = _User(user, set())

    def add_connection(self, user1: User, user2: User) -> None:
        """
        add a suggestion between 2 users

        Preconditions:
            - user1 != user2
        """
        if user1.id not in self._users:
            self.add_user(user1)
        if user2.id not in self._users:
            self.add_user(user2)
        u1 = self._users[user1.id]
        u2 = self._users[user2.id]

        u1.suggestions.add(u2)
        u2.suggestions.add(u1)

    def add_match_random(self, user1: User, user2: User) -> None:
        """
        Only adds a match between two users if the sum of their user ids is divisible by 2.

        Preconditions:
            - user1 != user2
            - user1.user_id in self._users and user2.user_id in self._users
        """
        if (user1.id + user2.id) % 2 == 0:
            u1 = self._users[user1.id]
            u2 = self._users[user2.id]
            u1.matches.add(u2)
            u2.matches.add(u1)

    def send_request(self, user1: User, user2: User) -> None:
        """
        send request from user1 to user2
        Preconditions:
            - user1 != user2
            - user1.user_id in self._users and user2.user_id in self._users
        """
        u1 = self._users[user1.id]
        u2 = self._users[user2.id]
        u1.send_request(u2.user_id)

    def accept_request(self, user1: User, user2: User) -> None:
        """
        user1 accepts request from user2
        Preconditions:
            - user1 != user2
            - user1.user_id in self._users and user2.user_id in self._users
        """
        u1 = self._users[user1.id]
        u2 = self._users[user2.id]
        u1.accept_request(u2.user_id)

    def check_connection(self, user1: User, user2: User) -> bool:
        """
        check whether 2 users have a suggestion
        """
        if user1.id in self._users and user2.id in self._users:
            u1 = self._users[user1.id]
            return any(u2.user_id == user2.id for u2 in u1.suggestions)
        else:
            return False

    def check_match(self, user1: User, user2: User) -> bool:
        """
        check match
        Preconditions:
            - user1 != user2
            - user1.user_id in self._users and user2.user_id in self._users
        """
        if user1.id in self._users and user2.id in self._users:
            if self._users[user2.id] in self._users[user1.id].matches:
                return True
            else:
                return False
        else:
            return False

    def get_suggestions(self, user: User) -> set[int]:
        """
        return a set of user ids for the matches of the given user
        """
        if user.id in self._users:
            u = self._users[user.id]
            return {suggestion.user_id for suggestion in u.suggestions}
        else:
            raise ValueError

    def print_graph(self):
        """
        prints the network
        """
        for key in self._users:
            vertex = self._users[key]
            print(f"suggestions: {key}, {[u.user_id for u in vertex.suggestions]}")
            print(f"matches: {key}, {[u.user_id for u in vertex.matches]}")
