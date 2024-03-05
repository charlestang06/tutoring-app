# Iridium Tutoring Dashboard

[Iridium Tutoring](https://www.iridiumtutoring.org) is a nationwide 501(c)(3) nonprofit tutoring organization serving K-12 students with free, personalized educational support in all subjects. Our mission is to provide high-quality, accessible, and equitable tutoring to students in need, regardless of their background or financial status. We are committed to helping students reach their full potential and achieve academic success.

This dashboard streamlines the tutoring session registration process and tutor sign-up process to a non-Google-Sheets/Forms hosted platform. Developed by the 2024 Iridium Tutoring director team (Charles Tang). Utilizes Model-View-Template (MVT) architecture for Tutors, Students, and TutoringSessions.


## Tech Stack
- **Frontend**: Django, HTML, CSS, JavaScript
- **Backend**: Django, SQLite
- **Deployment**: DigitalOcean

## Features
[x] Admin dashboard (manage tutor, student, session registrations)
[x] Student session registration (sign up for tutoring sessions, email confirmation, automatic account generation)
[] Student dashboard (login/logout, see past/upcoming sessions, register session, see tutor details)
[] Tutor dashboard (login/logout, see available sessions, see historical sessions, volunteering hours, sign up for sessions, past taken sessions, add sessions)
[] Admin dashboard (sort by model, create new tutor form, create new session form)
[] Deployed onto DigitalOcean (thanks to nonprofit credits), subdomain of iridiumtutoring.org

## Notes

Since we are deploying with a SQLite single-file database, we will need to download the database from the server every time we deploy. This is not ideal, but it is the best we can do with our current resources.

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

3. Run the server.
```bash
    python manage.py runserver
```
