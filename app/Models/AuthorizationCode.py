from app import db
from .User import User
from authlib.flask.oauth2.sqla import  OAuth2AuthorizationCodeMixin

class AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
  __table_args__ = {'extend_existing': True}
  id = db.Column(db.Integer, primary_key=True,autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
  user = db.relationship(User)
