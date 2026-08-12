## Personal Cybersecurity Portfolio

A personal cybersecurity portfolio built with Python, Flask, HTML, CSS, JavaScript, and SQLite.

The site showcases cybersecurity projects, certifications, education, professional experience, and technical skills.

## Features
- Responsive portfolio website
- Dark/light theme
- Mobile navigation
- Project filtering
- Certifications page
- Resume download
- Contact form
- CSRF protection
- Secure session cookies
- Security headers
- SQLite database for contact messages
- Client-side and server-side form validation
- Tech Stack
- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- Security: CSRF protection, security headers, input validation
- Fonts: IBM Plex Sans / IBM Plex Mono

## Setup
Clone the repository
   
```git clone YOUR_REPOSITORY_URL```

```cd portfolio```

Create a virtual environment

```python -m venv venv```

Activate it

```.\venv\Scripts\Activate.ps1```

If PowerShell blocks activation:

```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```

Then activate again:

```.\venv\Scripts\Activate.ps1```

Install dependencies

```pip install -r requirements.txt```

Create .env

Create a file named:

```.env```

Add:

```SECRET_KEY=your-secret-key```

```FLASK_ENV=development```

Generate a stronger secret key with:

```python -c "import secrets; print(secrets.token_hex(32))"```

Copy the generated value into .env.

Run the application

```python app.py```

Open:

```http://127.0.0.1:5000```

## Contact Form

Contact submissions are:

Validated in JavaScript.
Sent to the Flask /contact endpoint.
Validated again on the server.
Protected with a CSRF token.
Stored in SQLite.
## Security
This project demonstrates several basic web security practices:

- CSRF protection
- Secure session cookies
- Input validation
- Parameterized SQL queries
- Security HTTP headers
- Content Security Policy
- HttpOnly cookies
- SameSite cookies
- Error handling without exposing database details

## Tenzin Melongkharpa

Cybersecurity professional focused on:

Cybersecurity
GRC
Cloud Security
IAM
Secure Software Development
AI & Security
License

This project is for personal portfolio and educational purposes.
