# SolidTechWrestling

This repository contains a simple Flask website for the Fort Wayne Wrestling Club.

## Features

- Account registration and login
- About Us page
- Donations page
- Forms include CSRF protection via Flask-WTF
- `SECRET_KEY` – secret key used for session and CSRF protection.
- Schedule page with the ability to add events (requires login)
- Modern responsive styling

## Requirements

See `requirements.txt` for Python package dependencies.

## Running

1. Install dependencies (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
2. Start the application:
   ```bash
   python app.py
   ```
3. Visit `http://localhost:5000` in your browser.
