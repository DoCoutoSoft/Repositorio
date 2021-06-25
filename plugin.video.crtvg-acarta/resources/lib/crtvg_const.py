
# -*- coding: UTF-8 -*-
# By FISAT
import os
import xbmcaddon

#
# Constants
# 
ADDON = "plugin.video.crtvg-acarta"
VERSION = "2.2.4"
DATE = "05/08/2018"
SETTINGS = xbmcaddon.Addon(id=ADDON)
LANGUAGE = SETTINGS.getLocalizedString
cachePeriod = SETTINGS.getSetting("cache")
PLUGIN_PATH = SETTINGS.getAddonInfo('path')
IMAGES_PATH = os.path.join(xbmcaddon.Addon(id=ADDON).getAddonInfo('path'), 'resources', 'media')
urlBase = 'http://www.crtvg.es/'
urlACarta ='http://www.crtvg.es/tvg/a-carta'
urlDirectos ='http://www.crtvg.es/tvg/tvg-en-directo'
urlThumbs = 'http://www.crtvg.es/files/thumbs/'
MINIATURA_GENERAL = os.path.join(IMAGES_PATH, 'miniatura_general.jpg')
USERAGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
DEBUG = SETTINGS.getSetting("DEBUG") == "true"
CANAL = 'CRTVG'
urlACartaAlfabetico = "http://www.crtvg.es/api/?key=apffh343444-dddkk9913833-aoijer0333-34poaskflas033-00AAAddd002233&idseccion=297&limite=0&idioma=glg&metadatos=true&filtros=Metadatodata.disponible_na_app:EQ1:&orden=Entrada.titulo&orden_direccion=ASC"
urlACartaProgramas = "http://www.crtvg.es/api/?key=apffh343444-dddkk9913833-aoijer0333-34poaskflas033-00AAAddd002233&idseccion=297&limite=0&idioma=glg&metadatos=true&filtros=Metadatodata.disponible_na_app:EQ:&orden=Entrada.titulo&orden_direccion=ASC"
urlRadioGalega = "http://www.crtvg.es/rg/rg-en-directo"



