import os
import sys

import socket
from contextlib import closing
import webbrowser

import logging
from pathlib import Path

from dash import Input, Dash

from vizer.gui import create_webapp
from vizer.ids import CHARTS_STORE_ID, PLOT_LAYOUT_STORE_ID, SELECTED_CHART_STORE_ID, GENERAL_STORE_ID
from vizer import workspace

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def register_auto_save(app: Dash):
    @app.callback(
        Input(CHARTS_STORE_ID, "data"), Input(SELECTED_CHART_STORE_ID, "data"), Input(GENERAL_STORE_ID, "data"),
        Input(PLOT_LAYOUT_STORE_ID, "data")
    )
    def save_workspace(charts, selected, general, plot):
        workspace.cws.plot = plot
        workspace.cws.general = general
        workspace.cws.selected = selected
        workspace.cws.charts = charts
        if workspace.cws.path:
            workspace.cws.save()


def run():

    if len(sys.argv) > 1:

        if sys.argv[1].endswith(".vws"):
            workspace.load_workspace(sys.argv[1])
            print("Loaded workspace")
        else:
            try:
                workspace.load_workspace(workspace.workspace_from_filename(sys.argv[1]))
                print("Found workspace - loading")
            except FileNotFoundError:
                workspace.cws.file = os.path.abspath(sys.argv[1])
                print("Loaded file in empty workspace")

    app = create_webapp()
    app.title = Path(workspace.cws.file).name if workspace.cws.file else "Vizu"
    register_auto_save(app)

    p = find_free_port()
    webbrowser.open(f"http://localhost:{p}")
    app.run_server(port=p, host="0.0.0.0", debug=False)


if __name__ == "__main__":
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    run()
