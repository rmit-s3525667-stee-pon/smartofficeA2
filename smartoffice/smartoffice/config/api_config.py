import configparser

config = configparser.ConfigParser()
config_file_path = '/home/pi/A2/smartoffice/smartoffice/config/config.ini'

def get_api_domain():
    config.read(config_file_path)
    return config.get('setting','api_domain')
