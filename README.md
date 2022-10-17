# quiz_mgmt_app
new web structure for quiz_app
#How to install
1. Flask app
    a.  Install virtual environment if you use python3.x you can skip this step
        since python3.x has its virual environment build-in
    b.  Create an environment in Linux and MacOS
        python3 -m venv <name of environment>
        exp for this project: $python3 -m venv auth
    c.  Activate the environment
        .<name of environment>/bin/activate
        exp: $./auth/bin/activate
    d. Install FLask
        $pip3 install Flask (outside the virtual environment)
    e. how to run
        -   go to virtual environment
            source <environment name>/bin/activate
            exp: $source auth/bin/activate
        - $export FLASK_APP=<name of project>
        - $export FLASK_DEBUG=1 //turn on the debug mode
        - $flask run
    f. Flask tutorials: https://www.tutorialspoint.com/flask/flask_environment.htm
2   Install sqlalchemy
    For MacOS
        pip3 install sqlalchemy
        pip3 insatll Flask-SQLALchemy
        reference: https://www.geeksforgeeks.org/how-to-install-sqlalchemy-in-python-on-macos/
        if face with error ModuleNotFoundError: No module named ‘flask_sqlalchemy’
        reference: https://itsmycode.com/no-module-named-flask-sqlalchemy/
        https://pymodule.com/no-module-named-sqlalchemy/

3. SQLALChemy support: https://www.sqlalchemy.org/support.html
    working with Sqlalchemy: https://www.section.io/engineering-education/flask-database-integration-with-sqlalchemy/

4. Webservice


5. Project structure
--auth--(virtual environment)
--instance--
    |-db.sqlite (database)
--project--
    |-static
    |    |-css
    |    |  |-style.css (css file that is used for the whole application)
    |    |-images
    |-templates
    |__init__.py (initialize the system variable, database)
    |-auth.py (used to manage login authentication)
    |-main.py (used to manage the navigation in the system)
    |-models.py (used to map the object with the database)