# Iridium Tutoring Dashboard

[Iridium Tutoring](https://www.iridiumtutoring.org) is a nationwide 501(c)(3) nonprofit tutoring organization serving K-12 students with free, personalized educational support in all subjects. Our mission is to provide high-quality, accessible, and equitable tutoring to students in need, regardless of their background or financial status. We are committed to helping students reach their full potential and achieve academic success. 

This dashboard streamlines the tutoring session registration process and tutor sign-up process to a non-Google-Sheets/Forms hosted platform. Developed by the 2024 Iridium Tutoring director team (Charles Tang).

## Tech Stack
- **Frontend**: Django, HTML, CSS, JavaScript
- **Backend**: Django, SQLite
- **Deployment**: *To be determined*

## Features
- Admin dashboard (manage tutor, student, session registrations)
- Tutor dashboard
- Student session registration
- Model-View-Template (MVT) architecture for Tutors, Students, and TutoringSessions

## Future Features
[] Student dashboard + auth
[] Tutor auth 
[] Director auth
[] Full site ported from Google Sites

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