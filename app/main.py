"""
Simulation of the suitemate program
"""
from __future__ import annotations

import random

from social_graph import Network
from user import User
from python_ta.contracts import check_contracts
from user import generate_random_users


# @check_contracts
def create_network(suggestions: list[tuple[User, tuple]]) -> Network:
    """
    create a network from matches
    """
    my_network = Network()
    for suggestion in suggestions:
        u1 = suggestion[0]
        for u2 in suggestion[1]:
            if not my_network.check_suggestion(u1, u2):
                my_network.add_suggestion(u1, u2)
            if not my_network.check_request(u1, u2):
                random_request(u1, u2, my_network)
                random_accept(u1, u2, my_network)

    my_network.print_graph()

    return my_network


def random_request(u1: User, u2: User, network: Network) -> None:
    """
    ranomly send a request
    """
    # x = random.choice([True, False])
    # print(x)
    if True:
        network.send_request(u1, u2)


def random_accept(u1: User, u2: User, network: Network) -> None:
    """
    ranomly accept a request
    """
    # x = random.choice([True, False])
    # print(x)
    if True:
        network.accept_request(u1, u2)


def create_data(lst: list[User]) -> list:
    """
    create sugesstions for create network

    Preconditions:
        - len(lst) % 5 == 0
    """
    accum = []
    for i in range(len(lst) // 5):
        accum.append((lst[i], (lst[i * 5 + 1], lst[i * 5 + 2], lst[i * 5 + 3], lst[i * 5 + 4])))
    return accum


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    test_list = generate_random_users('csv_files/names.csv', 5)
    test_list = create_data(test_list)
    create_network(test_list)

    # Creating and running flask app
    # from __init__ import create_app
    # app = create_app()
    # app.run(debug=True)

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120
    # })
