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

## Running Locally

```powershell
python app.py
```

The site runs at `http://127.0.0.1:5000/`. The SQLite database and its table
are created automatically on first run.

## Git / GitHub Workflow

```powershell
git init
git add .
git commit -m "Initial commit: cybersecurity portfolio"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

`.env`, the database file, and virtual environment folders are excluded via
`.gitignore` and should never be committed.

## Deployment (Render)

1. Push the project to a GitHub repository.
2. Create a new **Web Service** on Render and connect the repository.
3. Set the build and start commands:

   ```text
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. Add environment variables in the Render dashboard (do not commit them):

   ```text
   SECRET_KEY=<a-different-random-value-for-production>
   FLASK_ENV=production
   ```

5. Deploy. Render provides HTTPS automatically; `FLASK_ENV=production` makes
   the session cookie `Secure` and keeps debug mode off.

## Security Notes

- **No secrets in source code.** `SECRET_KEY` is loaded from environment
  variables via `python-dotenv`; only `.env.example` (with a placeholder) is
  committed.
- **CSRF protection.** Every contact form submission includes a per-session
  token that the server verifies with a constant-time comparison before
  writing to the database.
- **SQL injection prevention.** All database queries use parameterized
  placeholders (`?`) — user input is never concatenated into SQL.
- **Server-side validation.** The `/contact` route re-validates name, email,
  and message length even though the form also validates client-side, since
  client-side checks can be bypassed.
- **Safe DOM handling.** The front end uses `textContent`, not `innerHTML`,
  when displaying form errors or status messages, avoiding DOM-based XSS.
- **Security headers.** Responses include `X-Content-Type-Options`,
  `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, and a
  restrictive `Content-Security-Policy`.
- **Debug mode.** Disabled automatically when `FLASK_ENV=production`.
- **Generic error responses.** Server errors return a generic message to the
  client; details are only written to the server-side log.
- **No plaintext secrets in the database.** The `messages` table stores only
  the contact form's name, email, and message — no passwords are collected
  or stored anywhere in this application.
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
## PostgreSQL Database
Connect to the Database

Open PowerShell and go to the PostgreSQL bin directory:

```cd "C:\Program Files\PostgreSQL\18\bin"```

Connect to the Render PostgreSQL database:

```.\psql.exe "YOUR_DATABASE_URL"```

Security: Do not commit your database URL, username, or password to GitHub. Store the connection string securely.

View Contact Messages

After connecting to PostgreSQL, run:

```SELECT * FROM messages ORDER BY created_at DESC;```

This displays contact form submissions with the newest messages first.

Exit PostgreSQL

```\q```

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
