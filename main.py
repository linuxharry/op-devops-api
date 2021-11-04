from public import app
from config import DEBUG
from libs import middleware
from apps import account

from apps import appManager
from apps import instanceManager

from apps import serviceManage
from apps import ldapManager
from apps import JenkinsManager

from apps import ansibleManage
from apps import ansibleChannelAuth
from apps import configuration
from apps import home
# from apps import deploy

# from apps import assets

# from apps import apis
# from apps import schedule

# from apps import common
# from apps import system

middleware.init_app(app)
account.register_blueprint(app)
appManager.register_blueprint(app)
instanceManager.register_blueprint(app)
ldapManager.register_blueprint(app)
serviceManage.register_blueprint(app)
JenkinsManager.register_blueprint(app)
ansibleManage.register_blueprint(app)
ansibleChannelAuth.register_blueprint(app)
configuration.register_blueprint(app)
home.register_blueprint(app)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=DEBUG)
