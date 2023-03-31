# suitemate: The Roommate Finder
As students going into our second year, we know the struggles of finding a suitable roommate with similar interests when it comes to occupations and living habbits. Furthermore, it is especially difficult for international students who are new to Toronto and have yet to build their local network.

However, our initial call to action was to provide assistance to those who do not have the financial means to afford living in a unit on their own. In recent years, inflation has been an ongoing threat towards the people of Canada, which limited housing options for many people. Our biggest fear is having students not be able to complete their education due to housing complications, which is also our main drive towards making our project as successful as possible.

Conveniently, SuiteMate is a roommate finding platform designed for students at the University of Toronto that matches its users with potential partners based on their preferences. Whether the user wants a roommate of the same gender, or someone who refrains from smoking, we keep many variables into consideration when pairing two users.

# How to Run
You will need python 3.x and an up to date version of Flask and FlaskSQLAlchemy. 
Dependencies are in the `requirements.txt` file which can be downloaded by running
`pip3 install -r requirements.txt`.
Run the following command to start up the app in dev mode and type 
`localhost:<port-name>` in your web browser of choice (`<port-name>`) defaults to 5000.
```sh
flask --app app run --debug --port=<port-name>
```

# TODO
- [x] Generate User Data + figure out what fields are required - James
    - [x] id (some int)
    - [x] Gender Preferences + User's Gender
    - [x] User's Age
    - [x] Smoking Habits
    - [x] Desired Rent
    - [x] Sleeping Habits (when they go to bed)
    - [x] Pets
    - [x] Contact information
    - [x] Location
    - [x] Noise Level
    - [x] Guests
    - [x] Cleanliness level
    - [x] Number of roomates
        - Discrete intervals (i.e 1, 2, 3, 4+)
    - [x] CSV Reader and Writer
    - [ ] More sophisticated random user generation algos (i.e make rent normally distributed,
          fine tune the probabilities per attribute)
- [x] User dataclass - James
    - [x] Add the attributes
    - [x] Methods?
    - [x] get user from id (return user)
        - [x] Simple things like get_id
    - [x] Representation Invariants for User dataclass
- [ ] Decision tree model - Andrew & Derek
    - [x] Either make from scratch (probably) or use sklearn if we don't have time
    - [x] get_depth type of function?
    - [x] We can segment differently based on the attributes that the user prefers 
          (i.e one might be more concerned about rent than another)
          These will kinda be the subtrees (i.e one path will divide based on rent, another on gender etc)
    - [x] get_category (get to one of the leafs)
    - [ ] Augment with more sophisticated learning algorithm (Derek)
- [ ] Database (SQL or NoSQL or CSV) - Derek
    - [ ] Consolidate the storage types for the Flask db
    - [ ] Integrate with the User class that James made. Make a convert_to_python_user function
          that converts from a query from the db to our custom object in user.py (James pls)
    - [ ] How CSV fits into this?
        - [ ] We already have code for generating users into CSV, now just write code that
              generates users and inserts into DB so we have more fully featured demo in the
              main webapp (James pls)
    - [ ] Add a matches field, will contain the ids of the users people have matched with
- [ ] Graph Datastructure - Amaan & Derek
    - [x] Matcher Graph
    - [x] Social Graph - keeps track of the matches that people have with others
- [ ] Simulation/Logger Class - James & Derek
    - [ ] User Login
    - [ ] Enter information
    - [ ] Match Roommates
    - [ ] Dashboard of Matched Roommates -> allow them to cycle them
        - [ ] "Like"/Save
        - [ ] Skip
        - [ ] The match graph - you can look at the matches of your matches
- [ ] Frontend
    - [ ] Figure out what the "Find me a Match" will look like. Carousel or list view with cards?
    - [ ] Homepage (low priority)
- [ ] Flask backend
    - [ ] Integrate social graph into the webapp (Amaan)
        - [ ] Store connections that user has made into the DB
        - [ ] Do we update mutually or when user accepts as well (I think automatically update
        mutually)
        - [ ] Use the graph to serve next suggestions
    - [ ] Getting matches from decision tree, will likely have to do via ids
    - [ ] Updating profile
    - [ ] Pfp upload (low priority)
- [ ] If we have time
    - [ ] Dashboards for user/admin
    - [ ] Location graph
