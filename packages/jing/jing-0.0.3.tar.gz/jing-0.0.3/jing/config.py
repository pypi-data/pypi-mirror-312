#!/usr/bin/env python
# -*- encoding: utf8 -*-

import os
import json
import log

class Config:
    def __init__(self) -> None:
        logger = log.initLogger("config.log")
        # logger.debug("Config object init")
        self.config = self.load()

    def get(self, _section, _key):
        logger = log.getLogger()
        if _section in self.config:
            if _key in self.config[_section]:
                val = self.config[_section][_key]
                # logger.debug("[%s][%s] => [%s]", _section, _key, val)
                return val
            else:
                logger.error("error: key[%s] in [%s] not found", _key, _section)
        else:
            logger.error("error: section[%s] not found", _section)

        return ""

    def load(self):
        logger = log.getLogger()
        path = "%s/.local/sai.json" % os.getenv('HOME')
        if os.path.isfile(path):
            fd = open(path)
            return json.load(fd)
        else:
            self.logger.error("error: invalid path[%s]!", path)
            raise NameError('error: path')

config = Config()

def GetMysqlHost():
    return config.get("mysql", "host")

if __name__=="__main__":
    print(GetMysqlHost())
