HOSPITAL MANAGEMENT SYSTEM - By Ujjval (18103077), Suhel (18103092)


Instructions to run the project server:
1. Open the project directory in command prompt.
2. Go to settings.py file in the hospital folder inside the main directory and change the username and password to your own in the databases dictionary.
3. Make migrations by using the following commands - a. python manage.py makemigrations
					        b. python manage.py migrate
4. To run the project server use the command - python manage.py runserver
5. Open the web browser and go to http://localhost:8000 to view the website.


Technology Stack:
1. HTML,CSS,BOOTSTRAP
2. Django, Python3
3. Crispy Forms, Pillow


Directory Description:
1. HMS - Main Web Application for displaying the home page and availability status of hospital personnel.
2. hospital - Main project folder containing all the settings and configuration files required to run the project.
3. media - Folder containing the profile pictures of the users.
4. users - Web application for handling all the user related queries from registration to appointments.
5. manage.py - File for running the django web server.
6. readme.txt - File containing instructions, technology stack and directory information.