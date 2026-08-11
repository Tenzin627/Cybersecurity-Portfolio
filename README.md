# Cybersecurity Portfolio

A personal portfolio website built for cybersecurity, GRC, cloud security, and
AI/security roles. Single-page front end backed by a small Flask application,
built with secure development practices throughout.

## Features

- Responsive single-page layout: hero, about, skills, experience, projects,
  certifications, resume, and contact sections
- Dark theme by default with a light theme toggle, persisted in `localStorage`
- Project filtering by category (Cloud, AppSec, GRC, AI)
- Mobile navigation menu with smooth in-page scrolling
- Contact form with client-side and server-side validation
- CSRF-protected form submission backed by a SQLite database
- Security headers, parameterized SQL queries, and no debug mode in production

## Technologies

- **Front end:** HTML5, CSS3 (custom properties, no frameworks), vanilla JavaScript
- **Back end:** Python, Flask, Jinja2
- **Database:** SQLite
- **Config:** python-dotenv
- **Production server:** Gunicorn

## Project Structure

```text
cybersecurity-portfolio/
│
├── app.py                 # Flask routes, config, security headers, CSRF check
├── database.py             # SQLite connection + parameterized queries
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html          # Single-page portfolio template
│
├── static/
│   ├── style.css
│   └── script.js
│
└── database/
    └── portfolio.db         # Created automatically, not committed
```

## Installation (Windows PowerShell)

Clone or download the project, then from the project folder:

```powershell
cd path\to\cybersecurity-portfolio
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Create your `.env` file

```powershell
copy .env.example .env
```

Then open `.env` and set a real `SECRET_KEY`. You can generate one with:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Paste the output into `.env`:

```text
SECRET_KEY=<paste-generated-value-here>
FLASK_ENV=development
```

### Add your resume (optional)

Place a `resume.pdf` file in the `static/` folder so the **Download Resume**
button works, or update the link in `templates/index.html` to point elsewhere.

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

## License

This portfolio template is free to use and adapt for your own personal site.
