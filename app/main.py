"""
Simulation of the suitemate program
"""
from __future__ import annotations
from social_graph import Network, _User
from user import User
from python_ta.contracts import check_contracts


@check_contracts
def create_network(suggestions: list[dict[User, set[User]]]) -> Network:
    """
    create a network from matches
    """
    my_network = Network()
    for suggestion in suggestions:
        for u1 in suggestion:
            for u2 in suggestion[u1]:
                if not my_network.check_connection(u1, u2):
                    my_network.add_connection(u1, u2)
                if not my_network.check_match(u1, u2):
                    my_network.add_match(u1, u2)

    return my_network
