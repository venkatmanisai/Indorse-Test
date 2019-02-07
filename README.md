# Indorse-Test

A simple full stack django solution for login, signup through email activation

Assuming you have python 3.6.6. If not please install it from here https://www.python.org/downloads/release/python-366/

After downloading the project folder, navigate to IndorseTest folder from your cmd or any other terminal.

Install requirements: pip install -r requirements.txt

Then navigate to worthyvote folder and then settings.py: update your EMAIL_HOST credentials

Run the local server: python manage.py runserver

Note: If you see a SMTPerror then it is caused because you are trying to login to your email account from local server.
Gmail thinks some is trying to login with your credentials. To solve it please turn on "allow less secure apps settings" here.
https://myaccount.google.com/lesssecureapps?utm_source=google-account&utm_medium=web
