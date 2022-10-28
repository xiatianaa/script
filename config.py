# -*- coding: utf-8 -*-
import os

from configparser import RawConfigParser

file_ini = 'config.ini'


class Config(object):
    def __init__(self, config_file=file_ini):
        self._path = os.path.join(os.getcwd(), config_file)
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.ini")
        self._config = RawConfigParser()
        self._config.read(self._path, encoding='gbk')

    def get(self, section, name, strip_blank=True, strip_quote=True):
        s = self._config.get(section, name)
        if strip_blank:
            s = s.strip()
        if strip_quote:
            s = s.strip('"').strip("'")

        return s

    def set(self, section, name, value):
        self._config.set(section, name, value)
        f = open(file_ini, 'w')
        # 重新写入文件
        self._config.write(f)
        f.close()
    def getboolean(self, section, name):
        return self._config.getboolean(section, name)


global_config = Config()
