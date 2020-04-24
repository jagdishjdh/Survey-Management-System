# SSL-Project
CS 251 (SSL)  course Project.

Project Name :- Survey Management System (SMS)
--like google form

Take a look of our website at http://jsuthar.pythonanywhere.com/

Team Name :- Bash Overflow
Teammates :- Jagdish Suthar, Akram Khan, Kaushal U

HOW TO USE:
1) install any one of the database if not already installed. (sqlite3 or mySQL or postgreSQL)
PostgreSQL installation guid (https://computingforgeeks.com/installing-postgresql-database-server-on-ubuntu/)
For sqlite3 and mysql Databases you can google how to install

2) setup virtualenv 
create virtual envirement : virtualenv -p python3.7 venv
activate it using : source venv/bin/activate

3) clone this repo

4) if you are using postgreSQL then run these 3 commands
sudo apt install libpq-dev python3-dev
pip3 install -r requirments.txt
pip3 install psycopg2==2.8.5

If using sqlite3 or mysql run just this command
pip3 install -r requirments.txt

5) now go to sms/sms/settings.py file and modify your Database information accordingly.
  (username, password, host etc.)

6) run these 2 commands to setup database
python3 manage.py makemigrations
python3 manage.py migrate

7) to start server run this
python3 manage.py runserver

