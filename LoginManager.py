from flask import Flask, render_template, url_for, request, redirect
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from models import User
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UMood.db'
app.config['SECRET_KEY'] = 'test'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    Email = StringField(validators=[InputRequired(), Length(min=1, max=120)], render_kw={"placeholder": "Email"})
    Password = PasswordField(validators=[InputRequired(), Length(min=4, max=16)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")
    
    def validate_email(self, username):
        existing_email =  User.query.filter_by(Email=User.Email.data).first()
        if existing_email:
            raise ValidationError("That Email already exists. Please enter a different one.")
        
class LoginForm(FlaskForm):
    Email = StringField(validators=[InputRequired(), Length(min=1, max=120)], render_kw={"placeholder": "Email"})
    Password = PasswordField(validators=[InputRequired(), Length(min=4, max=16)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")   

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.Email.data).first()
        if user:
            if bcrypt.check_password_hash(user.Password, form.Password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)
    
@app.route('/dashboard', methods=('GET', 'POST'))
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.Password.data)
        new_user = User(Email=form.Email.data, Password=hashed_password)
        User.session.add(new_user)
        User.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)