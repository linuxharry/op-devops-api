from apps.serviceManage import view

def register_blueprint(app):
    app.register_blueprint(view.serviceUrl, url_prefix='/service')
