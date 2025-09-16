import configparser
import os


class ConfigReader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join("Configurations", "config.ini")

        # Set default values
        self.defaults = {
            'Application': {
                'url': 'https://www.google.com',
                'wait_time': '10'
            },
            'Browser': {
                'browser_name': 'chromium'
            },
            'Reporting': {
                'screenshot_on_failure': 'true',
                'trace_on_failure': 'true'
            }
        }

        # Read the config file if it exists
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)
        else:
            # Create default config if file doesn't exist
            print(f"⚠️ Config file not found at {self.config_path}. Using default values.")
            for section, options in self.defaults.items():
                self.config[section] = options

    def get_application_url(self):
        try:
            return self.config.get('Application', 'url')
        except (configparser.NoSectionError, configparser.NoOptionError):
            return self.defaults['Application']['url']

    def get_wait_time(self):
        try:
            return self.config.getint('Application', 'wait_time')
        except (configparser.NoSectionError, configparser.NoOptionError):
            return int(self.defaults['Application']['wait_time'])

    def get_browser(self):
        try:
            return self.config.get('Browser', 'browser_name')
        except (configparser.NoSectionError, configparser.NoOptionError):
            return self.defaults['Browser']['browser_name']

    def get_screenshot_on_failure(self):
        try:
            return self.config.getboolean('Reporting', 'screenshot_on_failure')
        except (configparser.NoSectionError, configparser.NoOptionError):
            return self.defaults['Reporting']['screenshot_on_failure'].lower() == 'true'

    def get_trace_on_failure(self):
        try:
            return self.config.getboolean('Reporting', 'trace_on_failure')
        except (configparser.NoSectionError, configparser.NoOptionError):
            return self.defaults['Reporting']['trace_on_failure'].lower() == 'true'