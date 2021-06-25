# -*- coding: utf-8 -*-
import inspect
import os

import xbmc
import config

loggeractive = (config.get_setting("debug") == "true")


def log_enable(active):
    global loggeractive
    loggeractive = active


def encode_log(message=""):
    if message:
        # Unicode to utf8
        if type(message) == unicode:
            message = message.encode("utf8")

        # All encodings to utf8
        elif type(message) == str:
            message = unicode(message, "utf8", errors="replace").encode("utf8")

        # Objects to string
        else:
            message = str(message)

    return message


def get_caller(message=None):
    module = inspect.getmodule(inspect.currentframe().f_back.f_back)

    # En boxee en ocasiones no detecta el modulo, de este modo lo hacemos manual
    if module is None:
        module = ".".join(os.path.splitext(inspect.currentframe().f_back.f_back.f_code.co_filename.split("tvalacarta")[1])[0].split(os.path.sep))[1:]
    else:
        module = module.__name__

    function = inspect.currentframe().f_back.f_back.f_code.co_name

    if module == "__main__":
        module = "tvalacarta"
    else:
        module = "tvalacarta." + module
    if message:
        if module not in message:
            if function == "<module>":
                return module + " " + message
            else:
                return module + " [" + function + "] " + message
        else:
            return message
    else:
        if function == "<module>":
            return module
        else:
            return module + "." + function


def info(texto=""):
    if loggeractive:
        xbmc.log(get_caller(encode_log(texto)), xbmc.logNOTICE)


def debug(texto=""):
    if loggeractive:
        texto = "    [" + get_caller() + "] " + encode_log(texto)

        xbmc.log("######## DEBUG #########", xbmc.logNOTICE)
        xbmc.log(texto, xbmc.logNOTICE)


def error(texto=""):
    if loggeractive:
        texto = "    [" + get_caller() + "] " + encode_log(texto)

        xbmc.log("######## ERROR #########", xbmc.logNOTICE)
        xbmc.log(texto, xbmc.logNOTICE)
