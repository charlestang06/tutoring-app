# Iridium Tutoring Dashboard

[Iridium Tutoring](https://www.iridiumtutoring.org) is a nationwide 501(c)(3) nonprofit tutoring organization serving K-12 students with free, personalized educational support in all subjects. Our mission is to provide high-quality, accessible, and equitable tutoring to students in need, regardless of their background or financial status. We are committed to helping students reach their full potential and achieve academic success.

This dashboard streamlines the tutoring session registration process and tutor sign-up process to a non-Google-Sheets/Forms-hosted platform. Developed by the 2024 Iridium Tutoring's founder, Charles Tang. Utilizes Model-View-Template (MVT) architecture for models `Tutors`, `Students`, and `Tutoring-Sessions`; views `studentView`, `tutorView`, `index`, `etc`; and Bootstrapped templates for each view.

## Tech Stack
- **Frontend**: HTML, CSS (Bootstrap 5.0), JavaScript
- **Backend**: Django, MySQL, Web Mail (SMTP)
- **Deployment**: CPanel, Apache, Python 3.11

## Features
Italicized features are prioritized for implementation. These are ordered in terms of priority.
- [x] (MVP #1) Admin dashboard (manage tutor, student, and session registrations)
- [x] (MVP #2) Student session registration (sign up for tutoring sessions, email confirmation, automatic account generation)
- [x] (MVP #3) Student dashboard (custom auth login/logout, see past/upcoming sessions, register session, see session details, see tutor details, cancel session)
- [x] (MVP #4) Tutor session dashboard (custom auth login/logout, see available sessions, see historical sessions,  sign up for sessions, past taken sessions, *add session / recurring sessions utility*, calendar view)
- [x] Deployed onto CPanel, configured DNS for a subdomain (portal.iridiumtutoring.org), 90-day SSL from Let's Encrypt Provider (HTTPS)
- [x] Tutor profile dashboard (volunteering hours)
- [ ] Admin improved dashboard (sort by model, create new tutor form, create new session form)
- [ ] CI/CD pipeline for automatic deployment from GitHub to CPanel, pre-prod server for staging
- [ ] TDD (Test-Driven Development) for all views, forms, models, and URLs

## Notes

Since we are deploying with a MySQL remote database, we will prototype on the local SQLite database. This is not ideal, but it is the best we can do with our current resources. 

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
