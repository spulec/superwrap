import logging
import os
import requests
import subprocess

# Suppress most requests logging
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)


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
    res = requests.get("https://api.github.com/legacy/repos/search/{}?language=python".format(virtualenv_name))
    repo_name = virtualenv_name
    repos = [repo for repo in res.json['repositories'] if repo['name'] == repo_name]
    repos = sorted(repos, key=lambda repo: repo['followers'], reverse=True)
    if not repos:
        print u"Could not find a github repo with name {}".format(repo_name)
        return
    repo = repos[0]
    owner = repo['username']
    github_url = u"git@github.com:{}/{}.git".format(owner, virtualenv_name)

    user_fork_url = None
    github_oauth_token = os.environ.get('GITHUB_OAUTH_TOKEN')
    if github_oauth_token:
        # Create a fork
        headers = {"Authorization": u"token {}".format(github_oauth_token)}
        fork_url = "https://api.github.com/repos/{}/{}/forks".format(owner, repo_name)
        res = requests.post(fork_url, headers=headers)
        if res.ok:
            user_fork_url = res.json['ssh_url']
        else:
            print "GITHUB_OAUTH_TOKEN did not have the right oauth scope"

    call_virtualenv_command("mkvirtualenv {}".format(virtualenv_name))
    dev_path = os.path.expanduser(os.environ.get("SUPERWRAP_DIR", "~/Development"))
    os.chdir(dev_path)
    call_virtualenv_command(u"git clone {}".format(github_url))
    os.chdir(virtualenv_name)
    call_virtualenv_command(u"git remote rm origin")
    call_virtualenv_command(u"git remote add origin {}".format(user_fork_url))

    call_virtualenv_command("python setup.py develop")
    print u"Setup {}:{} repo for development".format(owner, virtualenv_name)
