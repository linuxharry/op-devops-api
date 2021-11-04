from apps.instanceManager import view

def register_blueprint(app):
    app.register_blueprint(view.instanceMgUrl, url_prefix='/instance')

