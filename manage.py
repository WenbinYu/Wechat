# -*- coding:utf-8 -*-
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from wechat import get_app
from wechat import db

app = get_app('development')


#
# manager = Manager(app)
#
#
# Migrate(app, db)
#
# manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    app.run()

    # manager.run()