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
