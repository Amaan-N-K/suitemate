"""
CSC111 Winter 2023 Final Project: suitemate

Derek Huynh, James Yung, Andrew Xie, Amaan Khan

================================================

Main file responsible for running the flask app. Simply type "python main.py"
to launch the website and navigate to localhost:5000 in your browser (or just
click the link provided in the console).
"""
from __future__ import annotations

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
    import python_ta
    
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': [],
        'disable': ['unused-import', 'R1702', 'E9998', 'E9999', 'W0125'],
        'allowed-io': ['read_packet_csv']
    })

    # Creating and running flask app
    from __init__ import create_app, db

    app = create_app()
    app.run(debug=False)
