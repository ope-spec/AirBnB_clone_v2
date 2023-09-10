#!/usr/bin/python3
"""This script generates a .tgz archive from the contents of the web_static folder."""
from fabric.api import local
import time


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        local("mkdir -p versions")
        archive_name = "web_static_{}.tgz".format(time.strftime("%Y%m%d%H%M%S"))
        local("tar -cvzf versions/{} web_static/".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception:
        return None
