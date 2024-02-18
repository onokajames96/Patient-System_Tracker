from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import config
from models import Admin, MedicalRecord, MedicalRecordEntry, Patient, User
from flask import session, redirect, url_for, render_template, request, jsonify, Flask


app = Flask(__name__)

# Configure SQLAlchemy database connection
DB_URI = f'sqlite:///{config.DB_NAME}'
engine = create_engine(DB_URI)

# Check if the database exists, if not, create it
if not database_exists(engine.url):
    create_database(engine.url)

# Create tables if they do not exist
User.metadata.create_all(engine)
Patient.metadata.create_all(engine)
MedicalRecord.metadata.create_all(engine)
MedicalRecordEntry.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
# Routes

from flask import session, redirect, url_for, render_template, request

@app.route('/user_form', methods=['GET'])
def user_form():
    return render_template('user_form.html')

@app.route('/submit_user_form', methods=['POST'])
def submit_user_form():
    username =request.form.get('username')
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    date_of_birth = request.form.get('date_of_birth')
    address = request.form.get('address')
    phone_number = request.form.get('phone_number')
    return redirect(url_for('show_users'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if admin exists and the password matches
        admin = db_session.query(Admin).filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):  # Assuming you're using Flask-Bcrypt
            # Store admin ID in session
            session['admin_id'] = admin.id
            return redirect(url_for('admin_login_success'))
        else:
            return render_template('admin_login_failure.html')

    return render_template('admin_login.html')

@app.route('/admin/login/success')
def admin_login_success():
    admin_id = session.get('admin_id')
    if admin_id:
        return render_template('admin_login_success.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if the username or email already exists
        if session.query(Admin).filter_by(username=username).first() or session.query(Admin).filter_by(email=email).first():
            return render_template('admin_signup.html', error='Username or email already exists')

        # Create a new admin
        new_admin = Admin(username=username, password=password, email=email)
        session.add(new_admin)
        session.commit()

        return redirect(url_for('admin_signup_success'))

    return render_template('admin_signup.html')

@app.route('/admin/signup/success')
def admin_signup_success():
    return render_template('admin_signup_success.html')


@app.route('/admin/register', methods=['GET'])
def show_admin_registration_form():
    return render_template('register_admin.html')



@app.route('/admin/register', methods=['POST'])
def register_admin():
    data = request.form
    new_user = User(
        username=data['username'],
        password=data['password'],  # Hash the password before storing in the database
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=data['date_of_birth'],
        address=data['address'],
        phone_number=data['phone_number'],
        is_admin=True
    )
    session.add(new_user)
    session.commit()
    return jsonify({'message': 'Admin registered successfully'})

@app.route('/register', methods=['GET'])
def show_registration_form():
    return render_template('register_user.html')

@app.route('/register', methods=['POST'])
def register_user():
    data = request.form
    new_user = User(
        username=data['username'],
        password=data['password'],  # Hash the password before storing in the database
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=data['date_of_birth'],
        address=data['address'],
        phone_number=data['phone_number']
    )
    session.add(new_user)
    session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    if request.method == 'GET':
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            return render_template('update_user.html', user=user)
        else:
            return jsonify({'error': 'User not found'}), 404
    elif request.method == 'POST':
        data = request.form
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.username = data.get('username', user.username)
            user.password = data.get('password', user.password)  # Hash the password before updating
            user.email = data.get('email', user.email)
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
            user.address = data.get('address', user.address)
            user.phone_number = data.get('phone_number', user.phone_number)
            session.commit()
            return jsonify({'message': 'User information updated successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/users', methods=['GET'])
def show_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return render_template('users.html', users=users)

@app.route('/patients', methods=['GET'])
def show_patients():
    session = Session()
    patients = session.query(Patient).all()
    session.close()
    return render_template('patients.html', patients=patients)

@app.route('/medical_records', methods=['GET'])
def show_medical_records():
    session = Session()
    medical_records = session.query(MedicalRecord).all()
    session.close()
    return render_template('medical_records.html', medical_records=medical_records)

@app.route('/medical_record_entry', methods=['GET'])
def show_medical_record_entry():
    session =Session()
    entries = session.query(MedicalRecordEntry).all()
    return render_template('/medical_record_entry.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
