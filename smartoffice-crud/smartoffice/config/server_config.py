#!/usr/bin/env python3

import configparser

config = configparser.ConfigParser()
config_file_path = '/home/pi/A2/smartoffice-crud/smartoffice/config/config.ini'


def get_user():
    config.read(config_file_path)
    return config.get('setting','user')

def get_pass():
    config.read(config_file_path)
    return config.get('setting','pass')

def get_host():
    config.read(config_file_path)
    return config.get('setting','host')

def get_dbname():
    config.read(config_file_path)
    return config.get('setting','dbname')
