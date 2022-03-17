import os

from environs import Env

env = Env()
env.read_env()

LOGIN = int(os.environ['LOGIN'])
PASSWORD = os.environ['PASSWORD']
SERVER = os.environ['SERVER']
