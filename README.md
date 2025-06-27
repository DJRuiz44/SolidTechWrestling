# SolidTechWrestling

This repository contains a simple Flask website for the Fort Wayne Wrestling Club.

## Features

- Account registration and login
- About Us page
- Donations page
- Schedule page with the ability to add events (requires login to add events; viewing is public)
- Modern responsive styling
- Contact page that emails messages and stores them

## Requirements

See `requirements.txt` for Python package dependencies.

### Environment Variables

The application uses several environment variables for configuration:

- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD` and `MAIL_DEFAULT_SENDER` for the contact form email.
- `DEBUG` – set to `true` to enable Flask debug mode.
- `PORT` – port the app will listen on (defaults to `5000`).

Without the mail variables configured, messages will still be saved in the database but email notifications may fail.

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

## Local Setup Tutorial

1. **Clone this repository** and change into the project directory.
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set any desired environment variables** (for example your mail settings).
5. **Run the application**:
   ```bash
   python app.py
   ```
6. Open a browser to `http://localhost:5000` to see the site.

## Hosting Your Site

To make the club website publicly accessible you can deploy it to a platform like Heroku, Render or any server capable of running Python applications.

1. Create an account on your chosen hosting provider.
2. Add the environment variables described above to the hosted environment.
3. Deploy this repository and run the app using a production server such as `gunicorn`:
   ```bash
   gunicorn app:app
   ```
4. Configure your provider to expose the port used by `gunicorn` (usually 8000).

Refer to your provider's documentation for specific deployment steps.
