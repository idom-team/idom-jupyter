from urllib.parse import urljoin

from notebook.notebookapp import NotebookApp
from idom.client.manage import web_modules_dir
from tornado.web import StaticFileHandler
from tornado.web import Application


def _load_jupyter_server_extension(notebook_app: NotebookApp):
    web_app: Application = notebook_app.web_app
    route_pattern = urljoin(web_app.settings["base_url"], "_idom_web_modules/(.*)")
    web_app.add_handlers(
        host_pattern=".*$",
        host_handlers=[
            (
                route_pattern,
                StaticFileHandler,
                {"path": str(web_modules_dir().absolute())},
            ),
        ],
    )


# compat for older versions of Jupyter
load_jupyter_server_extension = _load_jupyter_server_extension
