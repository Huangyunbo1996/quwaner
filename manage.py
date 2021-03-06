from app import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from app.models import User,Travel,Comment,Tag
from app import db

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app,db)

@manager.shell
def make_shell_context():
    return dict(app=app,db=db,User=User,Travel=Travel,
                Comment=Comment,Tag=Tag)

manager.add_command('db',MigrateCommand)

@manager.command
def re_create_db():
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    manager.run()