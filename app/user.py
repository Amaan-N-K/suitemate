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
    rent: Optional[tuple[float, float]] = None  # range
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
def csv_write(users: list[User], overwrite_file: str) -> None:
    """
    create csv file. Overwrite a given csv file with user data.
    """
    # csv_file = open('csv_files/test.csv', 'w')
    csv_file = open(overwrite_file, 'w')
    csv_writer = csv.writer(csv_file)
    for item in users:
        csv_writer.writerow([item.name, item.username, str(item.id), str(item.age), item.gender, str(item.gender_pref),
                             str(item.smoke), str(item.rent), str(item.pets), str(item.contact), str(item.location),
                             str(item.noise), str(item.guests), str(item.cleanliness), str(item.num_roomates)])
    csv_file.close()


@check_contracts
def csv_read(user_file: str) -> list[User]:
    """
    csv file reader. Returns a list of users from csv_file
    """
    users = []
    with open(user_file) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            name = row[0]
            username = row[1]
            id = int(row[2])
            age = int(row[3])
            gender = row[4]

            if row[5] == 'None':
                gender_pref = None
            else:
                gender_pref = row[5]

            if row[6] == 'None':
                smoke = None
            else:
                smoke = bool(row[6])

            if row[7] == 'None':
                rent = None
            else:
                rent = eval(row[7])

            if row[8] == 'None':
                pets = None
            else:
                pets = bool(row[8])

            if row[9] == 'None':
                contact = None
            else:
                contact = row[9]

            if row[10] == 'None':
                location = None
            else:
                location = eval(row[10])

            if row[11] == 'None':
                noise = None
            else:
                noise = int(row[11])

            if row[12] == 'None':
                guests = None
            else:
                guests = bool(row[12])

            if row[13] == 'None':
                cleanliness = None
            else:
                cleanliness = int(row[13])

            if row[14] == 'None':
                num_roomates = None
            else:
                num_roomates = int(row[14])

            new_user = User(name, username, id, age, gender, gender_pref, smoke, rent, pets, contact, location, noise,
                            guests, cleanliness, num_roomates)
            users.append(new_user)

    return users


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # csv_write(generate_random_users('csv_files/names.csv', 5), 'csv_files/test.csv')

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120
    # })
