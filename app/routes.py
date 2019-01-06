from flask import render_template, flash, redirect, url_for, request
from app import app, db
from .forms import LoginForm, clientRegisterForm, userSignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from .Models.User import User
from .Models.Client import Client
from werkzeug.urls import url_parse
from werkzeug.security import gen_salt
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
@login_required
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
    #print(request.headers)
    #print(request.data)
    return authorization.create_token_response()
    #return "Oauth token route"

@app.route('/client_register', methods=['GET','POST'])
@login_required
def client_register():
  user = current_user
  if not user:
      return redirect('/')

  registerForm = clientRegisterForm()

  print('Function reached')
  if registerForm.validate_on_submit():
      request_content=request.form.to_dict(flat=True)
      print(*request_content)
      del(request_content['csrf_token'])
      del(request_content['submit'])
      print(*request_content)

      #client = Client(**request.form.to_dict(flat=True))
      client = Client(**request_content)
      client.user_id = user.id
      client.client_id = gen_salt(24)
      if client.token_endpoint_auth_method == 'none':
        client.client_secret = ''
      else:
        client.client_secret = gen_salt(48)

      if 'grant_type' in request_content and request_content['grant_type'] == "authorization_code":
          client.response_type = "code"
      elif 'grant_type' in request_content and request_content['grant_type'] == "token":
          client.response_type = "token"
      print(client.grant_type)
      db.session.add(client)
      db.session.commit()
      flash("Client Registered Successfully")
      #return redirect('/')
  else:
      print(registerForm.errors)


  return render_template('createClient.html', title='Client Registeration', form=registerForm)


@app.route('/sign-up',methods=['GET','POST'])
def userSignUp():

    signUpForm = userSignUpForm()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username=username, password=password)

        db.session.add(user)
        db.session.commit()
        flash("User Registered Successfully")
      #return redirect('/')
    else:
       print(signUpForm.errors)


    return render_template('userSignUp.html',title='Sign Up',form=signUpForm)
