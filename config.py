import configparser


class Config:
    def __init__(self):
        self.__file_dir = 'config.ini'
        self.__get_data = lambda section, key: self.__read_file()[section][key]
        # settings
        self.__speed = float(self.__get_data('Settings', 'speed'))
        self.__difficulty = float(self.__get_data('Settings', 'difficulty'))
        self.__high_score = int(self.__get_data('Achievements', 'high_score'))

    def __read_file(self):
        config_file = configparser.ConfigParser()
        config_file.read(self.__file_dir)
        return config_file

    def write_config_file(self, section, key, value, ):
        file = self.__read_file()
        file.set(section, key, value)
        with open(self.__file_dir, 'w') as f:
            file.write(f)

    # Window Setup

    @property
    def WINDOW_WIDTH(self):
        return int(self.__get_data('Setup', 'Width'))

    @property
    def WINDOW_HEIGHT(self):
        return int(self.__get_data('Setup', 'Height'))

    # Game Setup

    @property
    def GAME_WIDTH(self):
        return self.WINDOW_WIDTH  # same width as the window

    @property
    def GAME_HEIGHT(self):
        return (9 / 10) * self.WINDOW_HEIGHT  # 75% of the height of the whole window

    @property
    def WIDGET_SIZE(self):
        return self.WINDOW_WIDTH // 25  # size of fruit and snake segments

    # Controls

    @property
    def move_up(self):
        return self.__get_data('Controls', 'move_up').lower()

    @property
    def move_down(self):
        return self.__get_data('Controls', 'move_down').lower()

    @property
    def move_left(self):
        return self.__get_data('Controls', 'move_left').lower()

    @property
    def move_right(self):
        return self.__get_data('Controls', 'move_right').lower()

    @property
    def restart_game(self):
        return self.__get_data('Controls', 'Restart').lower()

    # Settings

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        self.__speed = value

    @property
    def difficulty(self):
        return self.__difficulty

    @difficulty.setter
    def difficulty(self, value):
        self.__difficulty = value

    # Achievements

    @property
    def high_score(self):
        return self.__high_score

    @high_score.setter
    def high_score(self, value):
        self.__high_score = value
