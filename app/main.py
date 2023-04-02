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
def create_network(net: Network, suggestions: list[User]) -> Network:
    """
    create a network from matches
    """
    for u1 in suggestions:
        for u2 in suggestions:
            if u1.id != u2.id:
                if not net.check_suggestion(u1, u2):
                    net.add_suggestion(u1, u2)
                if not net.check_request(u1, u2):
                    random_request(u1, u2, net)
                    random_accept(u1, u2, net)

    net.print_graph()

    return net


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

    # doctest.testmod()

    test_list = generate_random_users('csv_files/names.csv', 5)
    # test_list = create_data(test_list)
    network = Network()
    network.create_network(test_list)
    import pickle

    with open('test_network.pkl', 'wb') as f:
        pickle.dump(network, f)
    with open('test_network.pkl', 'rb') as f:
        loaded_network = pickle.load(f)
    print(loaded_network._users)
    loaded_network.print_graph

    # # Creating and running flask app
    # from __init__ import create_app
    # app = create_app()
    # app.run(debug=True)

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120
    # })
