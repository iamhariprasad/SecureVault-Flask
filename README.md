SecureVault - Secure file storage using Flask, Jinja, and MongoDB
## Iamhariprasad
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


Website images:
## 🔐 Login Page
<img src="https://github.com/user-attachments/assets/75ac1b35-6a83-4f5b-8b53-4936ecf4f2ae" width="100%" />

## 🧾 Register Page & Admin Login
<img src="https://github.com/user-attachments/assets/1a1fcc8b-47b4-4ed2-bea7-7f562d19317c" width="100%" />

## 🗂️ Dashboard (User & Admin)
<img src="https://github.com/user-attachments/assets/0e52777d-1ed8-49ee-a308-52f17b10c1a0" width="100%" />

## ⬆️ Upload Files (Password Encrypted) — User & Admin
<img src="https://github.com/user-attachments/assets/1d500330-b12f-4f74-b0a8-a3abad218fea" width="100%" />

## 🆕 Updated Dashboard (User & Admin)
<img src="https://github.com/user-attachments/assets/ba3e652a-8f70-4840-a589-7a565ac13b5b" width="100%" />

## 🔓 Download File (Password Decryption) — User & Admin
<img src="https://github.com/user-attachments/assets/6f0388db-bbe7-4e15-935f-1306757476e8" width="100%" />

## 👤 User 2 Uploading Files
<img src="https://github.com/user-attachments/assets/e8135bd3-4e10-4030-bf3f-018960512b31" width="100%" />

## 📁 File Uploaded (User 2)
<img src="https://github.com/user-attachments/assets/cf621ef3-f213-40cd-8b5d-7ab4d94195c6" width="100%" />

## 🛡️ Admin Dashboard (hari is admin + regular user)
<img src="https://github.com/user-attachments/assets/1b72a385-092d-4cbf-8a39-10b04c100d1f" width="100%" />

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