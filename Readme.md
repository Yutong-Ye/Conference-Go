####1. How to create a Conference management project 🌎

-Web-based conference management application is going to be an API-based application (*application-programmatic interface)*, which means that your Django back-end will send JSON to the browser.

-When building API-based applications, quite often we must use an API client, which is Insomnia in this case. This allows you to make HTTP requests and see the JSON-formatted responses.

-To build an online application that allows people to plan software developer conferences

-To book a conference, a person needs to have a physical location, like a hotel or convention center. Once they have that, they can create a conference that people can sign up for. Attendees will have badges w-ith QR codes that allow them to connect with other attendees, but the QR code thing is not needed for the MVP.

-Conferences are nothing without really great presentations. Your software will also allow people to propose different presentations. A future feature will allow someone to review the presentation proposal to approve or reject it.

-Eventually, you're going to want to allow vendors and sponsors to have places to set up their booths to show off their wares. However, that's a future feature that does not have to be in the MVP.

**e.g ![Design] ![Reference image](/Picture/Conference_Design.png)**

**Set up** 💻

1.Fork the repo at <https://gitlab.com/sjp19-public-resources/conference-go/>

2.Clone your fork to your projects directory.

3.Change directory into the repository directory.

4.Create a virtual environment.

```python
python -m venv ./.venv

source ./.venv/bin/activate
```

5.Upgrade pip.

```python
python -m pip install --upgrade pip

pip install django
```


6.Install the requirements from the requirements.txt file.

```python
pip freeze > requirements.txt
```

7.Run the migrations.

```python
python manage.py makemigrations

python manage.py migrate
```
8.This project includes a data dump so that you can test out your APIs.

Run this command to import data

```python
python manage.py loaddata conference_go/data.json
```

Loading that data will create a superuser for you with the username **admin** and the password **admin**. (Not particularly secure. Don't do that in real life.) It also contains all of the U.S. states, presentation statuses, some convention center locations, some conferences, and 1000 attendees.

####Code Walk-Through

The Django apps have already been installed in the settings.py file. Also, the URLs are already configured for you in the urls.py file.

There are four Django apps in this Django application:

1. accounts, which contains a custom User object that's not yet used. There are no URLs for that Django app.

2. attendees, which contains the Attendee and Badge models for the application. It has two URL configurations:
-one to list the attendees for a conference
-one to get the details for a specific attendee

3. events, which contains the Conference, Location, and State models. It has four URL configurations:
-one to list the conferences
-one to get the details of a conference
-one to list the locations
-one to show the details of a location

4. presentations, which contains the Presentation and Status models. It has two URL configurations:
-one to get a list of presentations for a conference
-one to get the details for a presentation




###RESTfulize It
#####Set up
comment out the CSRF middleware in the settings.py file.
Open settings.py. Search for "Csrf" and delete below line 

```python
"django.middleware.csrf.CsrfViewMiddleware",
```
With it gone, you'll not be bothered by the Yellow Page of Sadness about missing CSRF tokens.

This project has four main parts:

It shows you how to create, update, and delete Location Entities.
It shows you how to create a Conference, which is slightly different because it has a reference to a Location.
It shows you how to create an Attendee, which is slightly different because it's a dependent resource.
It asks you to take what you've seen and apply it to the rest of the application.




#### Summary :smile:
You can find the link of the project here <>