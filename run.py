import os
from app import app, db

if __name__ == '__main__':
    # 1. Create upload folder if missing
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 2. Automatically generate SQLite database & tables on first run
    with app.app_context():
        db.create_all()
        
    # 3. Start development server
    app.run(debug=True)