#!/usr/bin/env python3
"""
Distributes an archive to web servers using the function do_deploy.
"""
from fabric.api import run, put, env
from fabric.api import local, task
from datetime import datetime
import os
from os.path import exists

env.hosts = ['3.85.136.193', '107.22.144.21']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/ssh_key'


@task
def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = local("tar -cvzf {} web_static".format(archived_f_path))

    if t_gzip_archive.succeeded:
        return archived_f_path
    else:
        return None

@task
def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.
    """
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        run("sudo rm -rf {}/web_static".format(newest_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    return False
