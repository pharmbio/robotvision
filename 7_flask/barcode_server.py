import logging
from flask import Flask

PORT = 5001

def handle():
    return "read comment"

if __name__ == '__main__':
    # Init logging
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Before start server")


    server = Flask(__name__)
    server.add_url_rule('/read', 'read', handle)

    server.run(host='0.0.0.0', port=PORT)