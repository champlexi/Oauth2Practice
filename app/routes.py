from flask import render_template, flash, redirect, url_for, request
from app import app
from .forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from .Models.User import User
from werkzeug.urls import url_parse
import flask_login
from .oauth2 import authorization, config_oauth
from authlib.specs.rfc6749 import OAuth2Error

@app.route('/')
@app.route('/index')
def index():
    return "Welcome to Learnnacts.in"

@app.route('/home')
@login_required
def home():
    user = {'username':'Lexi'}
    return render_template('home.html',title='Home',user=user)


@app.route('/login', methods=['GET','POST'])
def login():
    '''Error Details : int does not have attribute is_authenticated
       Solution : There was issue in load_user method defined in User Model class. I had defined parameter in decorator. That was wrong.
       I need to provide parameter in method instead of decorator '''
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    #print(flask_login.current_user)
    form = LoginForm()
    if form.validate_on_submit():
        #flash('Login requested for user {}, remember_me={}'.format(form.username.data,form.remember_me.data))
        #print(flask_login.current_user.is_authenticated())
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.username.data, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/oauth/authorize', methods=['GET','POST'])
def authorize():
    config_oauth(app)
    user = current_user

    if request.method =='GET':
        try:
            print(user)
            grant = authorization.validate_consent_request(end_user=user.id)
        except OAuth2Error as error:
            print(error)
            return error.error
        return render_template('authorize.html', user=user, grant=grant)

    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = User.query.filter_by(username=username)
    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None
    return authorization.create_authorization_response(grant_user=grant_user)

@app.route('/oauth/token', methods=['POST'])
def issue_token():

    '''if request.method == 'GET':
        code = request.args.get('code')
        state = request.args.get('state')
        print(code)
        print(state)
        grant_type = "authorization_code"
        redirect_uri = "http://127.0.0.1:5000/home"'''
    return authorization.create_token_response()
    #return "Oauth token route"
