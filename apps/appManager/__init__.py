from apps.appManager import view

def register_blueprint(app):
    app.register_blueprint(view.appMgUrl, url_prefix='/app')

