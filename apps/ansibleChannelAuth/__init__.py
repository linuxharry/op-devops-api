from apps.ansibleChannelAuth import view

def register_blueprint(app):
    app.register_blueprint(view.channelUrl, url_prefix='/channel')
