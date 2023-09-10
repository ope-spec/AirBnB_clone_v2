#!/usr/bin/env python3
"""
Distributes an archive to web servers using the function do_deploy.
"""
from fabric.api import run, put, env
from os.path import exists

env.hosts = ['3.85.136.193', '107.22.144.21']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/ssh_key'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.
    """
    if not exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")

        archive_filename = archive_path.split('/')[-1]
        release_folder = "/data/web_static/releases/{}".format(
            archive_filename[:-4])
        run("mkdir -p {}".format(release_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_folder))

        run("rm /tmp/{}".format(archive_filename))
        run("mv {}/web_static/* {}".format(release_folder, release_folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_folder))

        print("New version deployed!")
        return True
    except Exception:
        return False
