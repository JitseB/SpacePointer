from app import app
import json, os

with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as file:
    config = json.load(file)

if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'], debug=config['debug'])
