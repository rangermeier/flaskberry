from fabric.api import local, lcd
import os

PROJECT_ROOT = os.path.dirname(__file__)
PROJECT_NAME = "flaskberry"

project_dir = os.path.join(PROJECT_ROOT , PROJECT_NAME)
venv_dir = os.path.join(local("echo $WORKON_HOME", capture=True), 
    PROJECT_NAME, "bin", "activate")

def venv_local(command, capture=False):
    return local('source %s && %s' % (venv_dir, command),
        capture=capture)

def msg_update():
    with lcd(project_dir):
        venv_local('pybabel extract -F babel.cfg -o messages.pot .')
        venv_local('pybabel update -i messages.pot -d translations')

def msg_compile():
    with lcd(project_dir):
        venv_local('pybabel compile -d translations')

def test():
    local('nosetests')

def save_requirements():
    venv_local('pip freeze > requirements.txt')

def prepare_commit():
    test()
    save_requirements()
    msg_compile()
