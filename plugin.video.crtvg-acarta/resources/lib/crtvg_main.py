# -*- coding: UTF-8 -*-

#
# Imports
#
import sys
import urllib,urllib2
import urlparse
import xbmc, xbmcaddon
import xbmcgui
import xbmcplugin
import os
from crtvg_const import *
from resources.lib import core
from resources.lib.core import scrapertools
from resources.lib import crtvg_utils
from crtvg_utils import *

nombre_canal = "tvg"

#
# Main class
#if len(sys.argv[2]) == 0:
    #
    # Main menu
    #


class Main:
    def __init__(self):

        # Menu Principal
        liStyle = []
        
        liStyle = xbmcgui.ListItem("Programas Destacados")
        liStyle.setArt({'icon': os.path.join(IMAGES_PATH, 'destacados.png'), 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
        inserta_menu_prinicpal({"action": "destacados","url": urlACarta}, liStyle)
        
        liStyle = xbmcgui.ListItem("Últimos programas engadidos".decode('string_escape'))
        liStyle.setArt({'icon': os.path.join(IMAGES_PATH, 'novedades.png'), 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
        inserta_menu_prinicpal({"action": "novedades","url": urlACarta}, liStyle)
        
        liStyle = xbmcgui.ListItem("Listaxe Do A ao Z")
        liStyle.setArt({'icon': os.path.join(IMAGES_PATH, 'az.png'), 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
        inserta_menu_prinicpal({"action": "programas","url": urlACarta}, liStyle)
        
        #liStyle = xbmcgui.ListItem("Listaxe de programas por orde alfabetico".decode('string_escape'))
        #liStyle.setArt({'icon': os.path.join(IMAGES_PATH, ''), 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
        #inserta_menu_prinicpal({"action": "alfabetico","url": urlACarta}, liStyle)
        
        liStyle = xbmcgui.ListItem("Listaxe de programas por Categorías".decode('string_escape'))
        liStyle.setArt({'icon': os.path.join(IMAGES_PATH, 'categorias.png'), 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
        inserta_menu_prinicpal({"action": "categorias","url": urlACarta}, liStyle)
        
        liStyle = xbmcgui.ListItem("Canles que emiten en Directo")
        liStyle.setArt({'icon': os.path.join(IMAGES_PATH, 'tvdirectos.png'), 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
        inserta_menu_prinicpal({"action": "directos","url": urlDirectos}, liStyle)
        
        liStyle = xbmcgui.ListItem("Radio Galega")
        liStyle.setArt({'icon': os.path.join(IMAGES_PATH, 'radiogalega.png'), 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
        inserta_menu_prinicpal({"action": "radio","url": urlACarta}, liStyle)

        #liStyle = xbmcgui.ListItem(".... Probas varias....")
        #liStyle.setArt({'icon': os.path.join(IMAGES_PATH, 'pruebas.png'), 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
        #inserta_menu_prinicpal({"action": "pruebas","url": urlACarta}, liStyle)
        
        xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
    

