from apps.ldapManager import view

def register_blueprint(app):
    app.register_blueprint(view.ldapUrl, url_prefix='/ldap')
