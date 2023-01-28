Devops challenge

In py/server there is a quick and dirty api server which serves data from a sql lite database. 

To run it, you will have to have poetry installed. To install poetry, see https://python-poetry.org/

To run it you will also have to have a recent python (3.9). You can manage python versions with pyenv. See https://github.com/pyenv/pyenv

To get the server running:
Using poetry, install the necessary packages. Activate the poetry shell. 
Then in the py/server directory run the following command to have the server run in development mode:
flask --app server.app --debug run --host 0.0.0.0 --port 5001

Now you should be able to go to your browser and get json data for various endpoints served by the URL like:
http://localhost:5001/api/awards
http://localhost:5001/api/applications

Here are some things you can do to show off your devops skills. You don't have to do them all, spend about 2 hours. 
Try to focus on one category and get 2 or 3 done for that category.
Alternatively, try to get get one done from 2 or 3 categories.

Docker:
1. Create a docker container to run the server
2. Create a docker-compose file that will run the docker container for the server
3. Get the server running in "production mode" (on your local host), with gunicorn or uwsgi
4. Incorporate that into the Docker container

Database:
1. Set up a postgres or mysql with docker and get that running
2. Copy the data from SQLlite to postgres or mysql. 
3. Change the connector in app.py to use the postgres or mysql database. 
4. Run the database from docker-compose.yml. 
5. hook everything up with environment variables and get things working so you can query the server 

Cloud:
1. Run the server on a cloud instance (ec2, for instance)
2. Run the server on a cloud instance in production mode (uwsgi or gunicorn) 
3. Set up a domain name and have the server serve at that domain name
4. Put a load balancer which will terminate ssl infront of the cloud instance

Refactoring:
There is code in the app.py to genreate the sqllite enchantments.db database from scratch. To use it, delete
enchantments.db and run app.py on it's own. This is kind of hokey.
1. Refactor the creating of the database into a seperate python file 
2. When the server attempts to start, check if the database file exists,and if not create it using your refactored module.
3. Run a postgres or mysql with docker 
4. Change the database connection to use postgres or mysql in the code
5. Change the create_db method to insert data into the postgres or mysql 

You can expense up to $50.00 USD of cloud services as you deem necessary. Send me the receipts and your account and I will reimburse you.
