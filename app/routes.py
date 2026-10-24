import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.models import User, Complaint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_evidence(form_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    evidence_fn = random_hex + f_ext
    evidence_path = os.path.join(app.config['UPLOAD_FOLDER'], evidence_fn)
    form_file.save(evidence_path)
    return evidence_fn

@app.route("/")
def home():
    return render_template('login.html', title='Home')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        # Check if user exists
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('register'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, phone=phone, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    complaints = Complaint.query.filter_by(author=current_user).order_by(Complaint.date_posted.desc()).all()
    return render_template('dashboard.html', complaints=complaints)

@app.route("/report/new", methods=['GET', 'POST'])
@login_required
def new_report():
    if request.method == 'POST':
        category = request.form.get('category')
        description = request.form.get('description')
        suspect = request.form.get('suspect')
        file = request.files.get('evidence_file')
        
        evidence_file = None
        if file and file.filename != '':
            if allowed_file(file.filename):
                evidence_file = save_evidence(file)
            else:
                flash('Invalid file type. Only JPG, PNG, and PDF allowed.', 'danger')
                return redirect(url_for('new_report'))
                
        complaint = Complaint(category=category, description=description, suspect_info=suspect, evidence_file=evidence_file, author=current_user)
        db.session.add(complaint)
        db.session.commit()
        flash('Complaint has been registered successfully.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('report.html', title='File Report')

@app.route("/admin")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    complaints = Complaint.query.order_by(Complaint.date_posted.desc()).all()
    return render_template('admin.html', complaints=complaints)

@app.route("/admin/update_status/<int:complaint_id>", methods=['POST'])
@login_required
def update_status(complaint_id):
    if not current_user.is_admin:
        abort(403)
    complaint = Complaint.query.get_or_404(complaint_id)
    new_status = request.form.get('status')
    complaint.status = new_status
    db.session.commit()
    flash(f'Status updated for Case #{complaint.id}', 'success')
    return redirect(url_for('admin_dashboard'))