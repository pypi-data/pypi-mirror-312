import os
import configparser
import logging

class ConfigRegistry:
    """
    A global registry to manage and access Config instances by ID.
    """
    _registry = {}

    @classmethod
    def register(cls, config_id, config_instance):
        """
        Register a new Config instance with a unique ID.
        """
        if config_id in cls._registry:
            raise ValueError(f"Config ID '{config_id}' is already registered.")
        cls._registry[config_id] = config_instance

    @classmethod
    def get(cls, config_id):
        """
        Retrieve a Config instance by its ID.
        """
        if config_id not in cls._registry:
            raise ValueError(f"Config ID '{config_id}' is not registered.")
        return cls._registry[config_id]

    @classmethod
    def unregister(cls, config_id):
        """
        Remove a Config instance from the registry.
        """
        if config_id in cls._registry:
            del cls._registry[config_id]
        else:
            raise ValueError(f"Config ID '{config_id}' is not registered.")


class Config:
    """
    Configuration manager with optional integration into a global registry.
    """
    def __init__(self, config_file, log_namespace, enable_logging=True, log_level=logging.DEBUG, comment_prefixes = "#"):
        self.config = configparser.ConfigParser(allow_no_value=True, comment_prefixes=comment_prefixes, inline_comment_prefixes=comment_prefixes)
        self.config_file = config_file or os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
        self.log_dir = os.path.join(os.path.dirname(self.config_file), "logs", log_namespace)
        self.filepath = os.path.join(self.log_dir, f"config_{log_namespace}.log")
        os.makedirs(self.log_dir, exist_ok=True)
        self.enable_logging = enable_logging
        self.log_level = log_level
        if self.enable_logging:
            self._setup_logger()
        self.load_config()

    def _setup_logger(self):
        """
        Set up the logger with the specified logging level.
        """
        logging.basicConfig(
            filename=self.filepath,
            filemode='a',
            level=self.log_level,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(f"ConfigLogger_{id(self)}")

    def load_config(self):
        """
        Load the configuration file.
        """
        if os.path.exists(self.config_file):
            try:
                self.config.read(self.config_file)
                if self.enable_logging:
                    self.logger.info("Configuration loaded successfully.")
            except Exception as e:
                if self.enable_logging:
                    self.logger.error(f"Failed to load configuration: {e}")
        else:
            if self.enable_logging:
                self.logger.error(f"Config file '{self.config_file}' not found.")

    def save_config(self):
        """
        Save the current configuration to the config file.
        """
        try:
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
            if self.enable_logging:
                self.logger.info("Configuration saved successfully.")
        except Exception as e:
            if self.enable_logging:
                self.logger.error(f"Failed to save configuration: {e}")

    def set_value(self, section, option, value):
        """
        Set a configuration value.
        Creates the section if it doesn't exist.
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
            if self.enable_logging:
                self.logger.info(f"Added section: [{section}]")
        self.config.set(section, option, value)
        if self.enable_logging:
            self.logger.info(f"Set value: [{section}] {option} = {value}")
        self.save_config()

    def remove_value(self, section, option):
        """
        Remove a configuration value.
        """
        if self.config.has_section(section) and self.config.has_option(section, option):
            self.config.remove_option(section, option)
            if self.enable_logging:
                self.logger.info(f"Removed value: [{section}] {option}")
            self.save_config()
        else:
            if self.enable_logging:
                self.logger.warning(f"Attempted to remove non-existent value: [{section}] {option}")

    def remove_section(self, section):
        """
        Remove an entire section.
        """
        if self.config.has_section(section):
            self.config.remove_section(section)
            if self.enable_logging:
                self.logger.info(f"Removed section: [{section}]")
            self.save_config()
        else:
            if self.enable_logging:
                self.logger.warning(f"Attempted to remove non-existent section: [{section}]")

    def get_value(self, section, option, fallback=None):
        """
        Get a configuration value, returning a fallback if not found.
        """
        try:
            value = self.config.get(section, option, fallback=fallback)
            if self.enable_logging:
                self.logger.info(f"Retrieved value: [{section}] {option} = {value}")
            return value
        except Exception as e:
            if self.enable_logging:
                self.logger.error(f"Failed to retrieve value: [{section}] {option}. Error: {e}")
            return fallback

    def get_int(self, section, option, fallback=None):
        """
        Get an integer configuration value, returning a fallback if not found or invalid.
        """
        try:
            value = self.config.getint(section, option, fallback=fallback)
            if self.enable_logging:
                self.logger.info(f"Retrieved int value: [{section}] {option} = {value}")
            return value
        except Exception as e:
            if self.enable_logging:
                self.logger.error(f"Failed to retrieve int value: [{section}] {option}. Error: {e}")
            return fallback

    def get_bool(self, section, option, fallback=None):
        """
        Get a boolean configuration value, returning a fallback if not found or invalid.
        """
        try:
            value = self.config.getboolean(section, option, fallback=fallback)
            if self.enable_logging:
                self.logger.info(f"Retrieved bool value: [{section}] {option} = {value}")
            return value
        except Exception as e:
            if self.enable_logging:
                self.logger.error(f"Failed to retrieve bool value: [{section}] {option}. Error: {e}")
            return fallback

    def get_float(self, section, option, fallback=None):
        """
        Get a float configuration value, returning a fallback if not found or invalid.
        """
        try:
            value = self.config.getfloat(section, option, fallback=fallback)
            if self.enable_logging:
                self.logger.info(f"Retrieved float value: [{section}] {option} = {value}")
            return value
        except Exception as e:
            if self.enable_logging:
                self.logger.error(f"Failed to retrieve float value: [{section}] {option}. Error: {e}")
            return fallback

    def get_list(self, section, option, delimiter=',', fallback=None):
        """
        Get a list of values (comma-separated), returning a fallback if not found or invalid.
        """
        value = self.get_value(section, option, fallback="") 
        if value:
            try:
                return [v.strip() for v in value.split(delimiter)]
            except Exception as e:
                if self.enable_logging:
                    self.logger.error(f"Failed to parse list value: [{section}] {option}. Error: {e}")
                return fallback
        return fallback

    def get_dict(self, section, option, delimiter=',', key_value_separator=':', fallback=None):
        """
        Get a dictionary of key-value pairs (comma-separated), returning a fallback if not found or invalid.
        """
        value = self.get_value(section, option, fallback="")
        if value:
            try:
                pairs = [pair.split(key_value_separator) for pair in value.split(delimiter)]
                return {k.strip(): v.strip() for k, v in pairs}
            except Exception as e:
                if self.enable_logging:
                    self.logger.error(f"Failed to parse dict value: [{section}] {option}. Error: {e}")
                return fallback
        return fallback

    def register(self, config_id):
        """
        Register this Config instance in the global registry.
        """
        ConfigRegistry.register(config_id, self)

