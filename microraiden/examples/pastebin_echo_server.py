import click
from flask import request

from microraiden.click_helpers import main, pass_app
from microraiden.proxy.resources import PaywalledProxyUrl

private_key_path = "~/.local/share/io.parity.ethereum/keys/test/UTC--2018-07-30T14-28-43Z--781e3a75-ed6b-b801-a939-591bc8a9938f"
private_key_password_path = "~/.local/share/io.parity.ethereum/keys/test/password.txt"
state_file_path = "~/.config/microraiden/state_file_name"


class PaywalledPastebin(PaywalledProxyUrl):
    def __init__(self, *args, **kwargs):
        super().__init__(domain='https://pastebin.com', *args, **kwargs)

    def price(self):
        if '/pastebin/' in request.path:
            return self._price
        else:
            return 0


@main.command()
@click.option(
    '--host',
    default='localhost',
    help='Address of the proxy'
)
@click.option(
    '--port',
    default=5000,
    help='Port of the proxy'
)
@pass_app
def start(app, host, port):
    app.add_paywalled_resource(
        PaywalledPastebin,
        "/<path:x>",
        price=5
    )
    app.run(host=host, port=port, debug=True)
    app.join()


if __name__ == '__main__':
    import logging
    from gevent import monkey

    monkey.patch_all()
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("blockchain").setLevel(logging.DEBUG)
    logging.getLogger("channel_manager").setLevel(logging.DEBUG)
    main()
