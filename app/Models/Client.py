from app import db
from .User import User
from authlib.flask.oauth2.sqla import  OAuth2ClientMixin



class Client(db.Model,OAuth2ClientMixin):

    __table_args__ = {'extend_existing': True}
    #db.metadata.clear()

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship(User)

    '''name = db.Column(db.String(40))
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              nullable=False)

    # Possible Client_type value will be public and confidential
    client_type = db.Column(db.String(20), default='public')
    _redirect_uris = db.Column(db.Text)

    # Possible scope for my app would be read and write
    default_scope = db.Column(db.Text, default='read')

    @property
    def user(self):
        return User.query.get(1)

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self.default_scope:
            return self.default_scope.split()
        return []

    @property
    def allowed_grant_types(self):
        return ['authorization', 'password', 'client',
                'implicit']

    def getClientByID(client_id):
        clientDetails = Client.query.filter_by(client_id=client_id).first()
        return clientDetails'''
