from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users = [
        {"id": 1,"username": "doctor111","password": "hospital1234","first_name": "John","last_name": "Doe","profile_picture": "path_to_picture","email": "john.doe@example.com","address_line1": "123 Street","city": "china","state": "Hong kong","pincode": "12345"},
        {"id": 2,"username": "doctor110","password": "hospital1234","first_name": "chan","last_name": "lee","profile_picture": "path_to_picture","email": "chan123lee@example.com","address_line1": "123 Street","city": "hong kong","state": "china","pincode": "12345" }
        ]

class User:
    def __init__(self, user_dict):
        self.id = user_dict.get('id')
        self.username = user_dict.get('username')
        self.password = user_dict.get('password')
        self.first_name = user_dict.get('first_name')
        self.last_name = user_dict.get('last_name')
        self.profile_picture = user_dict.get('profile_picture')
        self.email = user_dict.get('email')
        self.address_line1 = user_dict.get('address_line1')
        self.city = user_dict.get('city')
        self.state = user_dict.get('state')
        self.pincode = user_dict.get('pincode')

def find_user(username):
    for user in users:
        if user['username'] == username:
            return User(user)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/redirect', methods=['POST'])
def redirect_user():
    option = request.form['option']
    if option == 'login':
        return redirect('/login')
    elif option == 'signup':
        return redirect('/signup')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    new_patient = {
        "id": len(users) + 1,
        "username": request.form.get('username'),
        "password": request.form.get('password'),
        "first_name": request.form.get('first_name'),
        "last_name": request.form.get('last_name'),
        "email": request.form.get('email'),
        "address_line1": request.form.get('address_line1'),
        "city": request.form.get('city'),
        "state": request.form.get('state'),
        "pincode": request.form.get('pincode')
    }
    users.append(new_patient)
    return redirect('/patient_dashboard')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = find_user(username)
    if user and user.password == password:
        return redirect('/dashboard?username=' + username)
    else:
        return 'Invalid username or password'

@app.route('/dashboard')
def dashboard():
    username = request.args.get('username')
    user = find_user(username)
    if user:
        return render_template('dashboard.html', user=user)
    else:
        return "User not found"

@app.route('/patient_dashboard')
def patient_dashboard():
    user=users[-1]
    return render_template('patient_dash.html', user=user)

    
@app.route('/logout', methods=['get'])
def logout():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
