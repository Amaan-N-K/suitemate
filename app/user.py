"""
user class
"""
import csv
import random
from dataclasses import dataclass
from typing import Optional
from python_ta.contracts import check_contracts


@check_contracts
@dataclass
class User:
    """
    A custom data type that represents each user

    Instance Attributes:
        - name: The name of the user
        - username: the user's username (log in credentials)
        - id: unique integer identifier for each user
        - age: the age of the user
        - gender: the gender of the user
        - gender_pref: prefered gender of user's roomates
        - smoke: whether user is fine with a smoking environment
        - rent: price range the user is willing to pay monthly
        - pets: whether user is fine with having pets in the place
        - contact: contact information of user
        - location: country and city the user wants to find a place in
        - noise: noise level the user is comfortable with
        - guests: whether user is fine with having guests
        - cleanliness: cleanliness preference of the user
        - num_roomates: number of roomates the user is looking for (e.g. 1, 2, 3, 4+)

    Representation Invariants:
        - 17 <= self.age <= 100
        - 1 <= self.num_roomates <= 100

    """
    name: str
    username: str
    id: int
    age: int
    gender: str
    gender_pref: Optional[str] = None
    smoke: Optional[bool] = None
    rent: Optional[tuple[int, int]] = None  # range
    pets: Optional[bool] = None  # yes, no change to bool
    contact: Optional[str] = None  # ???
    location: Optional[tuple[str, str]] = None  # country city
    noise: Optional[int] = None  # rating 1 - 4 from quite to loud
    guests: Optional[bool] = None  # could be more than just yes or no?? never, often, sometimes
    cleanliness: Optional[int] = None  # rating 1 - 10??
    num_roomates: Optional[int] = None  # 1, 2, 3, 4 or more


@check_contracts
def generate_random_users(name_file: str, num_user: int) -> list[User]:
    """
    generate a random list of users. Number of users will be specified in the function parameter

    >>> people = generate_random_users('csv_files/names.csv', 5)
    >>> len(people)
    5
    """
    users = []
    for i in range(num_user):
        with open(name_file) as csv_file:
            csv_reader = csv.reader(csv_file)
            new_name = random.choice([(line[1], line[3]) for line in csv_reader])
        new_age = random.randint(17, 100)
        new_user = new_name[0].lower() + '_' + str(random.randint(100, 999))
        # we could also randomly choose the gender from 3 options (others) instead of taking from csv
        users.append(User(new_name[0], new_user, i, new_age, new_name[1]))

    return users


@check_contracts
def csv_write(users: list[User]) -> None:
    """
    create csv file
    """
    csv_file = open('csv_files/test.csv', 'w')
    csv_writer = csv.writer(csv_file)
    for item in users:
        csv_writer.writerow([item.name, item.username, str(item.id), str(item.age), item.gender, item.gender_pref,
                             str(item.smoke), str(item.rent), str(item.pets), item.contact, str(item.location),
                             str(item.noise), str(item.guests), str(item.cleanliness), str(item.num_roomates)])
    csv_file.close()


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120
    # })
