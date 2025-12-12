SecureVault - Secure file storage using Flask, Jinja, and MongoDB

Prerequisites:
- Python 3.10+ and pip
- MongoDB running locally or accessible remotely
- Optional Ubuntu/WSL setup helper script

Ubuntu/WSL setup (optional):
- From an Ubuntu or WSL terminal at the project root, run: bash scripts/setup_ubuntu.sh
- The script installs system build tools, creates .venv, and installs Python dependencies.
- When complete: copy .env.example to .env and adjust values.

Quick start:
1) Create a virtualenv and install dependencies
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
2) Configure environment
   Copy .env.example to .env and edit values (Windows: copy manually; Linux/WSL: cp .env.example .env)
   Set: SECRET_KEY, JWT_SECRET_KEY, MONGO_URI, HOST, PORT, FLASK_DEBUG
3) Run the app
   python app.py
   The server binds to HOST (default 0.0.0.0) and uses PORT (default 5000).
   Open http://localhost:5000

Configuration (.env):
- SECRET_KEY, JWT_SECRET_KEY: required for sessions and JWT.
- MONGO_URI: e.g., mongodb://localhost:27017/securevault?serverSelectionTimeoutMS=2000
- HOST, PORT, FLASK_DEBUG, FLASK_ENV
- UPLOAD_FOLDER: defaults to ./encrypted_files
- MAX_CONTENT_LENGTH: optional upload size limit (bytes)
- ADMIN_USERNAME, ADMIN_PASSWORD: optional bootstrap values if your workflow uses them
Environment variables are loaded automatically via python-dotenv when a .env file is present.

Troubleshooting:
- MongoDB connectivity:
  - Ensure MongoDB is running (e.g., sudo systemctl status mongodb) or use Docker.
  - On WSL, localhost typically reaches Windows services; confirm port 27017 is accessible.
  - Use /health to check DB status; it returns JSON and 503 if the DB is unreachable.
  - Add serverSelectionTimeoutMS to MONGO_URI to fail fast on unreachable servers.
- WSL reloader loops:
  - The app starts with use_reloader=false to avoid infinite reload loops on WSL.
  - If you need auto-reload, enable it in app.py knowingly (may re-trigger loops in WSL).
- Port already in use:
  - Change PORT in .env or free the conflicting process.

Project notes:
- Encrypted files are stored in the encrypted_files directory (ignored by git).
- Environment variables are read from .env via python-dotenv.
- Static assets live under static/ and templates under templates/.

Production notes:
- Disable debug (FLASK_DEBUG=0) and use a production WSGI server (gunicorn on Linux, waitress on Windows).
- Set strong SECRET_KEY; secure cookies and sessions.
- Serve behind a reverse proxy with TLS.
- Use CSRF protection for forms (Flask-WTF).