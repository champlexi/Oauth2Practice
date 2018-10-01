from app import db
from .User import User
from authlib.flask.oauth2.sqla import  OAuth2TokenMixin
import time

class Token(db.Model, OAuth2TokenMixin):

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship(User)

    def is_refresh_token_expired(self):
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at < time.time()
