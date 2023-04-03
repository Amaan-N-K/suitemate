"""
CSC111 Winter 2023 Final Project: suitemate

Derek Huynh, James Yung, Andrew Xie, Amaan Khan

================================================

This module represents the matches, suggestions and requests between users within a social network.
This file handles the interactions between users (e.g. Sending an invitation to room together, accepting
a request to room together, find common matches betwen users, etc.) and stores part of the data collected
in a social graph.
"""
from __future__ import annotations
from typing import Optional
from user import User
from python_ta.contracts import check_contracts
import random


# @check_contracts
class _User:
    """
    Nodes representing each user in the social network.

    Instance Attributes:
        - item: The user data class represented
        - user_id: the id of the user
        - suggestions: the _Users suggested to this _User
        - matches: the _Users that decided to match with this User
        - requests: the _Users that want to match with this User

    Representation Invariants:
        - self not in self.suggestions
        - self not in self.matches
        - self not in self.requests
        - all(self in u.suggestions for u in self.suggestions)
        - all(self in u.matches for u in self.matches)
        - all(self not in u.matches for u in self.suggestions)
        - all(self not in u.suggestions for u in self.matches)
        - all(self not in u.matches for u in self.requests)
        - all(u not in self.suggestions for u in self.requests)

    """
    item: User
    user_id: int
    suggestions: set[_User]
    matches: Optional[set[_User]] = set()
    requests: Optional[set[_User]] = set()

    def __init__(self, item: User, suggestions: set[_User]) -> None:
        """
        Initialize a node representing the user's personal information and preferences, suggested users,
        matched users and requested users.
        """
        self.item = item
        self.user_id = item.id
        self.suggestions = suggestions
        self.matches = set()
        self.requests = set()

    def accept_request(self, other: _User) -> None:
        """
        Move use _User from request to match. This function accepts an invitation
        to room with another user.

        Preconditions:
            - self.user_id != other.user_id
        """

        self.requests.remove(other)
        self.matches.add(other)
        other.matches.add(self)

    def send_request(self, other: _User) -> None:
        """
        Move _User from suggestion to request This function sends an invitation
        to room with another user

        Preconditions:
            - self.user_id != other.user_id
        """

        self.suggestions.remove(other)
        other.requests.add(self)

    def find_all_connected_matches(self, visited: set[int]) -> tuple[set[int], list[_User]]:
        """
        Find all users connected to self.

        Preconditions:
            - self not in visited
        """
        visited.add(self.user_id)
        all_users = [self]
        for neighbour in self.matches:
            if neighbour.user_id not in visited:
                seen, recur = neighbour.find_all_connected_matches(visited.copy())
                all_users.extend(recur)
                visited = visited.union(seen)

        return (visited, all_users)


# @check_contracts
class Network:
    """
    The graph representing the social network and connections between users

    Representation Invariants:
        - all(u_id == self._users[u_id].user_id for u_id in self._users)
    """
    _users: dict[int, _User]

    def __init__(self):
        """
        Initialize an empty network
        """
        self._users = {}

    def is_empty(self) -> bool:
        """
        Return whether the graph is empty or not

        Preconditions:
            - isinstance(self._users, dict)
        """
        return len(self._users) == 0

    def get_user(self, id_of_user: int) -> Optional[_User]:
        """
        Return the user with the coresponding id

        Preconditions:
            - id_of_user >= 0
        """
        if id_of_user in self._users:
            return self._users[id_of_user]
        else:
            return None

    def add_user(self, user: User) -> None:
        """
        Add a user to the graph

        Preconditions:
            - user not in self._users
        """
        self._users[user.id] = _User(user, set())

    def add_suggestion(self, user1: User, user2: User) -> None:
        """
        Add a suggestion between 2 users

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

    def send_request(self, user1: User, user2: User) -> None:
        """
        Send a request to be matched from user1 to user2

        Preconditions:
            - user1 != user2
            - user1.user_id in self._users and user2.user_id in self._users
        """
        u1 = self._users[user1.id]
        u2 = self._users[user2.id]
        u1.send_request(u2)

    def accept_request(self, user1: User, user2: User) -> None:
        """
        user1 accepts request from user2

        Preconditions:
            - user1 != user2
            - user1.user_id in self._users and user2.user_id in self._users
        """
        u1 = self._users[user1.id]
        u2 = self._users[user2.id]
        u1.accept_request(u2)

    def check_suggestion(self, user1: User, user2: User) -> bool:
        """
        check whether 2 users have a suggestion

        Preconditions:
            - user1 != user2
        """
        if user1.id in self._users and user2.id in self._users:
            u1 = self._users[user1.id]
            return any(u2.user_id == user2.id for u2 in u1.suggestions)
        elif self.check_request(user1, user2):
            return True
        else:
            return False

    def check_request(self, user1: User, user2: User) -> bool:
        """
        check if user2 sent a request to user1 or if they are a match

        Preconditions:
            - user1 != user2
            - user1.user_id in self._users and user2.user_id in self._users
        """
        if user1.id in self._users and user2.id in self._users:
            if self._users[user2.id] in self._users[user1.id].requests:
                return True
            elif self._users[user2.id] in self._users[user1.id].matches:
                return True
            else:
                return False
        else:
            return False

    def get_suggestions(self, user: User) -> set[int]:
        """
        return a set of user ids for the matches of the given user

        Preconditions:
            - user.user_id in self._users
        """
        if user.id in self._users:
            u = self._users[user.id]
            return {suggestion.user_id for suggestion in u.suggestions}
        else:
            raise ValueError

    def find_new_suggestion(self, user: User) -> None:
        """
        if 2 or more matches of user have another user in common, suggest the common user to user. Common user cannot
        already be a suggestion

        Preconditions:
            - user.user_id in self._users
        """
        u = self._users[user.id]
        if len(u.matches) < 2:
            return
        else:
            common_matches = set()
            for u1 in u.matches:
                for u2 in u.matches:
                    if u1.user_id != u2.user_id:
                        c = self._find_common_matches(u1, u2, u)
                        common_matches = common_matches.union(c)
            for suggested_user in common_matches:
                self.add_suggestion(u.item, suggested_user.item)

    def _find_common_matches(self, u1: _User, u2: _User, avoid: _User) -> set[_User]:
        """
        find all the common matches between users and return them in a set. avoid is not a common user.

        Preconditions:
            - u1 != u2 and avoid != u1 and avoid != u2
        """
        common_matches = u1.matches.intersection(u2.matches)
        if avoid in common_matches:
            common_matches.remove(avoid)
        return common_matches

    def find_all_new_suggestions(self) -> None:
        """
        Find all new suggestions if they exist for every node.

        Preconditions:
            - u_id is unique
        """
        for u_id in self._users:
            self.find_new_suggestion(self._users[u_id].item)

    def find_connected_communities(self) -> list[list[_User]]:
        """
        Find all connected communities in the network.

        Preconditions:
            - all u_id in self is unique
        """
        communities = []
        visited = set()
        for u_id in self._users:
            if u_id not in visited:
                connected = self._users[u_id].find_all_connected_matches(set())
                visited = visited.union(connected[0])
                communities.append(connected[1])
        return communities

    def random_suggestions(self, n: Optional[int] = 1) -> None:
        """
        Randomly suggest users to each other from different communities.

        Preconditions:
            - all users in Network is unique
        """
        for _ in range(n):
            keys = list(self._users.keys())
            u1 = self._users[random.choice(keys)]
            u2 = self._users[random.choice(keys)]
            self.add_suggestion(u1.item, u2.item)

    def random_suggestion_user(self, user: User, simple: Optional[bool] = True) -> None:
        """
        Randomly suggest across different communities for this user.

        Preconditions:
            - len(self._users) >= 2
        """
        if simple:
            u1 = self._users[user.id]
            keys = list(self._users.keys())
            u2 = self._users[random.choice(keys)]
            self.add_suggestion(u1.item, u2.item)
        else:
            u1 = self._users[user.id]
            community = u1.find_all_connected_matches(set())
            s = set(self._users.keys()).difference(community[0])
            keys = list(self._users.keys())
            u2 = self._users[random.choice(keys)]
            random_user_id = random.choice(list(s))
            u2 = self._users[random_user_id]
            self.add_suggestion(u1.item, u2.item)

    def print_graph(self):
        """
        prints the network
        """
        for key in self._users:
            vertex = self._users[key]
            print(f"suggestions: {key}, {[u.user_id for u in vertex.suggestions]}")
            print(f"matches: {key}, {[u.user_id for u in vertex.matches]}")

    def random_request(self, u1: User, u2: User) -> None:
        """
        Send a request that is paired with random acceptence

        Precondition:
            - u1.id in self._users
            - u2.id in self._users
        """
        self.send_request(u1, u2)

    def random_accept(self, u1: User, u2: User) -> None:
        """
        ranomly accept a request

        Precondition:
            - u1.id in self._users
            - u2.id in self._users
        """
        if random.choice([True, False]):
            self.accept_request(u1, u2)

    def create_network_single_community(self, suggestions: list[User], exclude: User) -> None:
        """
        Create a network from suggestions. Do not add any matches between any users in suggestions and
        exclude

        Precondition:
            - exclude in suggestions
        """
        if len(suggestions) == 1:
            self.add_user(suggestions[0])
        visited = set()
        for u1 in suggestions:
            for u2 in suggestions:
                if u1.id != u2.id and (u1.id, u2.id) not in visited and (u2.id, u1.id) not in visited:
                    if not self.check_suggestion(u1, u2):
                        self.add_suggestion(u1, u2)
                    if u1.id != exclude.id and u2.id != exclude.id and not self.check_request(u1, u2):
                        self.random_request(u1, u2)
                        self.random_accept(u2, u1)

                visited.add((u1.id, u2.id))

    def create_network_all(self, all_suggestions: list[list[User]], exclude: User, n: Optional[int] = 1000) -> None:
        """
        Create a network from all suggestions. Do not add any matches between any users in all_suggestions and
        exclude

        Precondition:
            - any(exclude in suggestions for suggestions in all_suggestions)
        """
        for suggestion in all_suggestions:
            self.create_network_single_community(suggestion, exclude)

        self.random_suggestions(n)
