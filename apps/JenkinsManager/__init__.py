from apps.JenkinsManager.jenkinsApi import view

def register_blueprint(app):
    app.register_blueprint(view.jenkinsUrl, url_prefix='/jenkins')

