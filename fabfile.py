"""REMOTE SERVER CONTROLS
file has to be named fabfile, functions are accessed from console
using "fab <functionname>" """

from fabric import task
from fabric import Connection

AWS = "ec2-18-197-132-108.eu-central-1.compute.amazonaws.com"
PEM = "../../sshmatt3000.pem"

###############################################################################
# DEFINE CONNECTION TO AWS
c = Connection(
        user = 'ec2-user',
        host = AWS,
        connect_kwargs = {'key_filename': PEM}
    )
###############################################################################
# REMOTE FUNCTIONS

@task
def basics(context):
    '''installs basic python and git on server'''
    c.run('sudo yum -y install python3')
    c.run('sudo yum -y install git')

@task
def requirements(context):
    '''installs python modules from requirements.txt'''
    with c.cd('product-api'):
        c.run('sudo pip3 install -r requirements.txt')
        c.run('mkdir templates')
    
@task
def clone(context):
    c.run('git clone https://github.com/mheerens/product-api.git')
    
@task
def credentials(context):
    '''sends credentials.py to server'''
    c.put("credentials.py")
    c.run('mv credentials.py product-api/credentials.py')

@task
def pull(context):
    '''pulls updates from github'''
    with c.cd('product-api'):
        c.run("pwd")
        c.run('git pull')
        
@task
def run(context):
    '''runs flask server, used to start the api'''
    with c.cd('product-api'):
        c.run("FLASK_APP=api.py flask run --host=0.0.0.0 --port=8080")

@task
def reset(context):
    '''erases project file and re-clones'''
    c.run('rm product-api -rf')
    c.run('git clone https://github.com/mheerens/product-api.git')

