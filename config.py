import configparser


class Config:
    def __init__(self, **kwargs):
        self.__file_dir = 'config.ini'
        self.__get_data = lambda section, key: self.__read_file()[section][key]

        # get settings from the file
        # setup
        self.window_width = int(self.__get_data('Setup', 'Width'))
        self.window_height = int(self.__get_data('Setup', 'Height'))
        # Settings
        self.speed = float(self.__get_data('Settings', 'speed'))
        self.difficulty = float(self.__get_data('Settings', 'difficulty'))
        # controls
        self.move_up = self.__get_data('Controls', 'move_up').lower()
        self.move_down = self.__get_data('Controls', 'move_down').lower()
        self.move_left = self.__get_data('Controls', 'move_left').lower()
        self.move_right = self.__get_data('Controls', 'move_right').lower()
        self.restart_game = self.__get_data('Controls', 'Restart').lower()
        # Achievements
        self.high_score = int(self.__get_data('Achievements', 'high_score'))

    # same width as the window
    @property
    def game_width(self):
        return self.window_width

    # 75% of the height of the whole window
    @property
    def game_height(self):
        return (9 / 10) * self.window_height

    # size of fruit and snake segments
    @property
    def widget_size(self):
        return self.window_width // 25

    def __read_file(self):
        config_file = configparser.ConfigParser()
        config_file.read(self.__file_dir)
        return config_file

    def write_config_file(self, section, key, value, ):
        file = self.__read_file()
        file.set(section, key, value)
        with open(self.__file_dir, 'w') as f:
            file.write(f)
