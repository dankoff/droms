import os

from flask import Flask

def make_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='KEM??Q^{0|{c??',
        DATABASE=os.path.join(app.instance_path, 'droms.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initiate app
    from . import db
    db.init_app(app)

    # register menu blueprint
    from . import menu
    app.register_blueprint(menu.bp)
    app.add_url_rule('/', endpoint='index')

    # register auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # register cart Blueprint
    from . import cart
    app.register_blueprint(cart.bp)

    return app
