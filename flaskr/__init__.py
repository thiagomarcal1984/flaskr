import os

from flask import Flask

def create_app(test_config=None):
    # Cria e configura o app.
    app = Flask(__name__, instance_relative_config=True) 
    # instance_relative_config=True muda a referência da instância: 
    # False (padrão) é relativo ao arquivo.py; 
    # True se refere à pasta onde o __init__ é declarado.
    app.config.from_mapping(
        SECRET_KEY = b'-6\xe3\\[\xee\xc1\x8cl\x17r\xf2\xf8\xd3\x14\x0b',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    
    if test_config is None:
        # Carrega o arquivo de configuração, se houver, quando não está testando.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Carrega a configuração de teste
        app.config.from_mapping(test_config)
    
    # Garante que a pasta da instância existe, para criar o DB.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    @app.route('/hello')
    def hello():
        return 'Hello, world!'

    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
