from apps.configuration import environment
def register_blueprint(app):
    app.register_blueprint(environment.blueprint, url_prefix='/configuration/environments')
