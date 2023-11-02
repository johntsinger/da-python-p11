# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

   Run tests with [unittest](https://docs.python.org/3/library/unittest.html#module-unittest) :

       python -m unittest discover tests

   Get tests coverage with [Coverage](https://coverage.readthedocs.io/en/coverage-5.1/) :
   
     - Update coverage file :
    
           coverage run -m unittest discover tests

       Note : a cover file already exists, but you can update it with this command.

     - Get console report :
  
           coverage report

     - Get html report :

           coverage html

   You can find the report in the htmlcov folder by openning the index.html file.

   Run performance tests with [Locust](https://locust.io/):

     - First lauch Flask server :

           flask run
       
     - Then open another terminal and activate virtual environement and run Locust :

           locust

     - Then go to http://localhost:8089
     - Set :
       - number of users : 1 to 3
       - spawn rate : 1
       - host : this should be http://127.0.0.1:5000 if not check the address in the terminal where you are running the flask server
    - Click start swarming
    - You must stop the test manually by clicking on the stop button.
