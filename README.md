# Tutoring App

This Django tutoring app was developed as a tutor/student portal for [Iridium Tutoring](https://www.iridiumtutoring.org), a nationwide 501(c)(3) nonprofit tutoring organization serving K-12 students with free, personalized educational support in all subjects. Our mission is to provide high-quality, accessible, and equitable tutoring to students in need, regardless of their background or financial status. We are committed to helping students reach their full potential and achieve academic success.

This dashboard is a B2C tutor + student web application that streamlines the tutoring session registration process and tutor sign-up process and replaces Excel/Google-Sheets/Forms platforms. Utilizes Model-View-Template (MVT) architecture for models `Tutors`, `Students`, and `Tutoring-Sessions`; views `studentView`, `tutorView`, `index`, `etc`; and Bootstrapped configurable templates for each view. Developed by the 2024 Iridium Tutoring's founder, Charles Tang. 

## Tech Stack
- **Frontend**: HTML, CSS (Bootstrap 5.0), JavaScript, FullCalendar
- **Backend**: Django, MySQL, Web Mail (SMTP), Let's Encrypt
- **Deployment**: CPanel, Apache, Python 3.11.5, WSGI

## Features
Italicized features are prioritized for implementation. These are ordered in terms of priority.
- [x] (MVP #1) Admin dashboard (manage tutor, student, and session registrations)
- [x] (MVP #2) Student session registration (sign up for tutoring sessions, email confirmation, automatic account generation)
- [x] (MVP #3) Student dashboard (custom auth login/logout, see past/upcoming sessions, register session, see session details, see tutor details, cancel session)
- [x] (MVP #4) Tutor session dashboard (custom auth login/logout, see available sessions, see historical sessions,  sign up for sessions, past taken sessions, add session / recurring sessions utility, calendar view)
- [x] Deployed onto CPanel, configured DNS for a subdomain (portal.iridiumtutoring.org), 90-day SSL from Let's Encrypt Provider (HTTPS)
- [x] Tutor profile dashboard (volunteering hours)
- [x] CI/CD pipeline for semi-automatic deployment from GitHub to CPanel, pre-prod server for staging

## Contributing
Fork this repository and create a new branch for your feature. Once you are done, create a pull request to merge your branch into the main branch.

## How To Run
We assume you have the latest version of Python installed.

1. Clone the repository
```bash
    git clone https://github.com/charlestang06/iridisite.git
```

2. Install the required packages
```bash
    pip install django
```

3. Make migrations
```bash
    python manage.py makemigrations
    python manage.py migrate
```

4. Run the server.
```bash
    python manage.py runserver
```
## Deploy to CPanel
1. Run the app on your local machine and ensure it works. (see previous steps)
2. Connect to CPanel and create a new MySQL database. Create a new user and assign the user to the database. Ensure the user has all privileges.
3. Under CPanel `Domains` tool, create a new subdomain (i.e. portal.iridiumtutoring.org) on your CPanel. Link it to the directory public_html/portal, or the directory of your choice.
4. Ensure `settings.py` is configured with MySQL database settings, `DEBUG = False`, and `ALLOWED_HOSTS = ['*']`.
5. Run `python manage.py collectstatic` to collect all static files into the static directory.
6. Zip the entire project folder and upload it to the root directory of your CPanel. Extract the contents into the subdomain directory.
7. Under `Create Python App` tool, create a new Python application. Select the subdomain you created in step 2. Make sure you select the highest Python version (3.11.5).
8. Add environment variables for all email settings, database settings, and Django secret key.
9. With an FTP client, configure the `passenger_wsgi.py` file with the following contents.
```python
# passenger_wsgi.py
import os
import sys

from iridisite.wsgi import application
```
9. From the dashboard, install all dependencies through the `pip install` tool with the `requirements.txt` file. If you have any issues, you can install the packages manually through the `python` tool.
10. In the `python` tool, run `manage.py makemigrations` and `manage.py migrate` to create the database tables.
11. Restart the Python application and visit the subdomain to see if it works.