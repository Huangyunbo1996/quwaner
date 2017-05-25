from app import create_app
from flask_script import Manager
from app.models import User,Travel
from app import db

app = create_app('default')
manager = Manager(app)

@manager.shell
def make_shell_context():
    return dict(app=app,db=db,User=User,Travel=Travel)

if __name__ == '__main__':
    manager.run()