import configparser
import os

cur_path = os.path.dirname(__file__)
config_path = os.path.join(cur_path, "cfg.ini")
config = configparser.ConfigParser()
config.read(config_path)

sender = config.get('email', 'sender')
password = config.get('email', 'password')
host = config.get('email', 'host')
receiver = config.get('email', 'receiver')
subject = config.get('email', 'subject')
content = config.get('email', 'content')