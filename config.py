import configparser


class Config:
    def __init__(self, **kwargs):
        self.__file_dir = 'config.ini'
        self.__get_data = lambda section, key: self.__read_file()[section][key]

        self.window_width = int(self.__get_data('Setup', 'Width'))
        self.window_height = int(self.__get_data('Setup', 'Height'))

        self.fps = float(self.__get_data('Gameplay', 'Fps'))
        self.snake_speed = int(self.__get_data('Gameplay', 'snake_speed'))

        self.fruit_size = int(self.__get_data('Settings', 'fruit_size'))
        self.snake_size = int(self.__get_data('Settings', 'snake_size'))

        self.move_up = self.__get_data('Controls', 'move_up').lower()
        self.move_down = self.__get_data('Controls', 'move_down').lower()
        self.move_left = self.__get_data('Controls', 'move_left').lower()
        self.move_right = self.__get_data('Controls', 'move_right').lower()
        self.restart_game = self.__get_data('Controls', 'Restart').lower()

    def __read_file(self):
        config_file = configparser.ConfigParser()
        config_file.read(self.__file_dir)
        return config_file

    def write_config_file(self, section, key, value, ):
        file = self.__read_file()
        file.set(section, key, value)
        with open(self.__file_dir, 'w') as f:
            file.write(f)
