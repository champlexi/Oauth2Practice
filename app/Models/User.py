from app import db, login
from werkzeug.security import safe_str_cmp
from flask_login import UserMixin


class User(UserMixin, db.Model):
    db.metadata.clear()
    #__table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40),nullable=False)

    '''def __str__(self):
        return self.username'''

    def get_user_id(self):
        return self.id


    def check_password(self,username, password):
        user = User.query.filter_by(username=username).first()
        if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
          return user
        else:
         return False



@login.user_loader
def load_user(user_id):
    print(user_id)
    return User.query.filter_by(id=user_id).first()
