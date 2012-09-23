Superwrap: The easy way to contribute to python packages
=========================================================

Superwrap in an extension to virtualenvwrapper that makes it easier to contribute to a python package for the first time.

Here is the current workflow for starting to contribute to a new project for people that use virtualenvwrapper: ::

    $ mkvirtualenv requests
    ...
    (requests)$ ~/Development
    (requests)$ git clone git@github.com:kennethreitz/requests.git
    ...
    (requests)$ cd requests
    (requests)$ python setup.py develop

And then start working. After setting up Superwrap, it becomes this: ::

    $ workon requests
    Setup kennethreitz:requests repo for development
    activated
    (requests)$ echo "There is no step 2!"

Anytime you use workon with a repo that you don't already have setup, it will create a new virtualenv, find and clone the repo from github into a new directory, change to that directory, and run ``python setup.py develop``. If you use workon with a virtualenv that has been previously setup, it will work the exact same.

Installation
------------

    * First, have `virtualenvwrapper configured <http://virtualenvwrapper.readthedocs.org/en/latest/install.html>`_.
    * Configure where you want new repos to go by setting the SUPERWRAP_DIR evnrionment variable. It will default to ~/Development.
    * (Optional) Configure GITHUB_OAUTH_TOKEN if you want to create a fork of every repo to clone instead of cloning the repo itself.
    * $ pip install superwrap
    * Add the following to $WORKON_HOME/postactivate

::

    #!/bin/bash
    proj_name=$(echo $VIRTUAL_ENV|awk -F'/' '{print $NF}')
    cd $SUPERWRAP_DIR/$proj_name

Note that this will create issues if your current setup does not consist of virtualenvs and directories with matching names.