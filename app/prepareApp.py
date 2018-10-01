#from Models.User import User
#from Models.Client import Client
from Models.AuthorizationCode import AuthorizationCode
from Models.Token import Token
#from Models.Grant import Grant
from app import app, db
from pymysql import Error
from datetime import datetime


class prepareApp():
    def populateData(self,app):
        db.init_app(app)
        db.app = app
        db.create_all()

        '''user1 = User(username='Lexi', password='test1234')
        #user1 = User(username='Lexi')
        user2 = User(username='Champ', password='root1234')
        #user2 = User(username='Champ')
        client1 = Client(client_id='lexi_id', client_secret='lexi_secret',client_name='lexi_client'
                         ,grant_type='authorization_code',response_type='code',
                         redirect_uri=("http://localhost:8000/authorized"))'''

        auth_Code1 = AuthorizationCode(code='idjnienoiwrjc',client_id='lexi_client',redirect_uri=("http://localhost:8000/authorized"),response_type='code')

        token1 = Token(client_id='lexi_client',token_type='bearer',access_token='27429384029380')

        '''client1 = Client(name='lexi_client', client_id='lexi_id', client_secret='lexi_secret',
                         _redirect_uris=("http://localhost:8000/authorized"))
        client2 = Client(name="rocks_client",client_id='rocks_id',client_secret="rocks_secret",
                         _redirect_uris=("http://localhost:8000/authorized"),default_scope="read", client_type="confidential")'''

        '''grant1 = Grant(user_id="1", client_id='lexi_id',code='87648u5t945809', redirect_uri="http://127.0.0.1:5000/authorize",
                       scope="read", expires=datetime.now())'''

        try:
            '''db.session.add(user1)
            db.session.add(user2)
            db.session.add(client1)'''
            #db.session.add(client2)
            #db.session.add(grant1)
            db.session.add(auth_Code1)
            db.session.add(token1)
            db.session.commit()
            db.session.close()
        except Error as error:
            print(error)

        return app

def main():

        prepApp = prepareApp()
        prepApp.populateData(app)

if __name__ == '__main__':
    main()
