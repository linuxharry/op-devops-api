from apps.ansibleManage import view

def register_blueprint(app):
    app.register_blueprint(view.ansibleUrl, url_prefix='/ansible')

