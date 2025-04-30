from config import config
from src.init_app import init_app

configuration = config['development']
app = init_app(configuration)

if __name__ == '__main__':
    app.run()