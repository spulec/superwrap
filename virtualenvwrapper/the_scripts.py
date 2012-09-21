import os
import requests
import subprocess


def call_virtualenv_command(command):
    base_command = "source /usr/local/share/python/virtualenvwrapper.sh;"
    command = u"{}{}".format(base_command, command)
    subprocess.check_output(command,
        stderr=subprocess.STDOUT,
        shell=True
    )


def pre_activate(args):
    virtualenv_name = args[0]
    command = u"virtualenvwrapper_verify_workon_environment {}".format(virtualenv_name)
    try:
        call_virtualenv_command(command)
    except subprocess.CalledProcessError:
        # virtualenv doesn't already exist. Create it.
        create_virtualenv(virtualenv_name)


def create_virtualenv(virtualenv_name):
    # mkvirtualenv
    call_virtualenv_command("mkvirtualenv {}".format(virtualenv_name))
    # cd to ~Development

    res = requests.get("https://api.github.com/legacy/repos/search/{}?language=python".format(virtualenv_name))
    repos = [repo for repo in res.json['repositories'] if repo['name'] == virtualenv_name]
    repos = sorted(repos, key=lambda repo: repo['followers'], reverse=True)
    repo = repos[0]
    owner = repo['username']

    github_url = "git@github.com:{}/{}.git".format(owner, virtualenv_name)
    dev_path = os.path.expanduser("~/Development")
    os.chdir(dev_path)
    call_virtualenv_command("git clone {}".format(github_url))
    os.chdir(virtualenv_name)
    call_virtualenv_command("python setup.py develop")
    print "Setup {}:{} repo for development".format(owner, virtualenv_name)
