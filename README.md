# Cybercrime Reporting System

A web-based portal developed with Flask that enables citizens to report cyber offenses, upload supporting evidence, and track complaint statuses, while allowing administrative review.

---

## Tech Stack
- **Backend:** Python 3, Flask
- **Database / ORM:** SQLite, Flask-SQLAlchemy
- **Authentication:** Flask-Login, Flask-Bcrypt
- **Frontend:** HTML5, CSS3, Jinja2 Templates

---

## How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/ksav1705/cybercrime_reporting_system.git
cd cybercrime_reporting_system
```

### 2. Set up a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python run.py
```

The database (`instance/site.db`) will be created automatically on first startup.

### 5. Access the app
Open your browser and navigate to:
```
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
```