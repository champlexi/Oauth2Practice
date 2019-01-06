from flask_wtf import FlaskForm,Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class clientRegisterForm(FlaskForm):
    client_name = StringField('ClientName', validators=[DataRequired()])
    client_uri = StringField('ClientURI', validators=[DataRequired()])
    scope = SelectField('Allowed Scopes', choices=[('read','Read'),('write','Write')], validators=[DataRequired()])
    redirect_uri = StringField('RedirectURIs',validators=[DataRequired()])
    grant_type = SelectField('Allowed Grant Types', choices=[('authorization_code','authorization_code'),('token','token'),('password','password'),
                                                         ('client_credentials','client_credentials')], validators=[DataRequired()])
    token_endpoint_auth_method = SelectField('Token Endpoint Auth Method', choices=[('client_secret_basic','client_secret_basic'),
                                                        ('client_secret_post','client_secret_post'),('none','None')])
    submit = SubmitField('Register')


class userSignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
