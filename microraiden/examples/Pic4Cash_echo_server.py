import logging
import os

from flask import request, send_file
from flask_restful import Resource

from microraiden.make_helpers import make_paywalled_proxy
from microraiden.proxy.resources import Expensive
from microraiden.utils import get_private_key

private_key = "/home/oliver/.local/share/io.parity.ethereum/keys/test/UTC--2018-07-30T14-28-43Z--781e3a75-ed6b-b801-a939-591bc8a9938f"
private_key = get_private_key(private_key)
state_file_path = "/home/oliver/.config/microraiden/state_file_name"

log = logging.getLogger(__name__)

FIX_PRICE_URL = "/echofix"


class Pic4Cash(Expensive):
    def get(self, url: str, param: str):
        # return request.files.get("/home/oliver/Schreibtisch/loredana.jpg", '')
        return send_file("/home/oliver/Schreibtisch/" + param, mimetype='image/jpg')


def run(join_thread: bool = True):
    dirname = os.path.dirname(state_file_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    app = make_paywalled_proxy(private_key, state_file_path)

    # log.info(app)
    app.add_paywalled_resource(
        cls=Pic4Cash,
        url=FIX_PRICE_URL + "/<string:param>",
        price=5
    )

    # Start the app. proxy is a WSGI greenlet, so you must join it properly.
    app.run(debug=True)

    if join_thread:
        app.join()
    else:
        return app
    # Now use echo_client to get the resources.


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
