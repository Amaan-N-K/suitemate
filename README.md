# suitemate: The Roommate Finder
As students going into our second year, we know the struggles of finding a suitable roommate with similar interests when it comes to occupations and living habbits. Furthermore, it is especially difficult for international students who are new to Toronto and have yet to build their local network.

However, our initial call to action was to provide assistance to those who do not have the financial means to afford living in a unit on their own. In recent years, inflation has been an ongoing threat towards the people of Canada, which limited housing options for many people. Our biggest fear is having students not be able to complete their education due to housing complications, which is also our main drive towards making our project as successful as possible.

Conveniently, SuiteMate is a roommate finding platform designed for students at the University of Toronto that matches its users with potential partners based on their preferences. Whether the user wants a roommate of the same gender, or someone who refrains from smoking, we keep many variables into consideration when pairing two users.

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
    - [ ] CSV Reader and Writer
- [x] User dataclass - James
    - [x] Add the attributes
    - [ ] Methods?
        - [ ] Simple things like get_id
    - [ ] Representation Invariants for User dataclass
- [ ] Decision tree model - Andrew & Derek
    - [ ] Either make from scratch (probably) or use sklearn if we don't have time
    - [ ] get_depth type of function?
    - [ ] We can segment differently based on the attributes that the user prefers 
          (i.e one might be more concerned about rent than another)
          These will kinda be the subtrees (i.e one path will divide based on rent, another on gender etc)
    - [ ] get_category (get to one of the leafs)
- [ ] Database (SQL or NoSQL or CSV) - Derek
- [ ] Graph Datastructure - Amaan & Derek
    - [ ] Matcher Graph
    - [ ] Social Graph - keeps track of the matches that people have with others
- [ ] Simulation/Logger Class - James & Derek
    - [ ] User Login
    - [ ] Enter information
    - [ ] Match Roommates
    - [ ] Dashboard of Matched Roommates -> allow them to cycle them
        - [ ] "Like"/Save
        - [ ] Skip
        - [ ] The match graph - you can look at the matches of your matches
- [ ] If we have time
    - [ ] Flask backend
    - [ ] Dashboards for user/admin
    - [ ] Location graph
