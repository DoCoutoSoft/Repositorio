
# -*- coding: UTF-8 -*-

#
# Imports
#
import os
import re
import sys
import urllib
import urlparse
import xbmc
import xbmcgui
import xbmcplugin


from crtvg_const import ADDON, SETTINGS, LANGUAGE, IMAGES_PATH, DATE, VERSION, MINIATURA_GENERAL
from core import scrapertools
from core import jsontools
from resources.lib.core.item import Item
from crtvg_utils import *


#
# Main class
#
class Main():
    #
    # Init
    #
    
    def __init__(self):

        self.plugin_url = sys.argv[0]
        self.plugin_handle = int(sys.argv[1])

       #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Iniciando : -> ", str(__file__)),#xbmc.logDEBUG)

        self.video_list_page_url = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['url'][0]
        

        datos1 = scrapertools.cache_page(self.video_list_page_url)
        datos2 = scrapertools.find_single_match(datos1,"LTIMAS ENTRADAS -->(.*?)<!--")
        patron  = '<a href="([^"]+)" title="([^"]+)"[^<]+'
        patron += '<div id="imagen-programa[^<]+'
        patron += '<img src="([^"]+)".*?'
        patron += '<div id="data-programa[^>]+>([^<]+)<'

        encontrados = re.compile(patron,re.DOTALL).findall(datos2)

        for url_encontrada,titulo_encontrado,miniatura_encontrada, fecha_encontrada in encontrados:
            titulo = titulo_encontrado.strip()
            titulo = scrapertools.htmlclean(titulo)+" - "+fecha_encontrada.strip()
            enlace = urlparse.urljoin(self.video_list_page_url, url_encontrada)
            miniatura = urlparse.urljoin(self.video_list_page_url, miniatura_encontrada)
            if miniatura == "":
                miniatura = MINIATURA_GENERAL

            import crtvg_server as servermodule
           #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Enlace video : -> ", enlace),#xbmc.logDEBUG)
            video_urls = servermodule.obten_enlace_video(enlace)
            media_url = str(video_urls)
            if media_url == "":
                crtvg_utils.msgerror("Erro obtendo programas","Non se atoparon programas. Ténteo mais tarde")
                return
            else:
                inserta_capitulo(titulo, enlace=media_url, categoria="play", miniatura=miniatura, resumen="", num_pagina="1", es_directorio=False, es_ultimo=False)

            """
            list_item = xbmcgui.ListItem(label=titulo, thumbnailImage=miniatura)
            list_item.setInfo("video", {"title": titulo, "studio": ADDON})
            list_item.setArt({'thumb': miniatura, 'icon': "", 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
            list_item.setProperty('IsPlayable', 'true')
            is_folder = False
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=media_url,listitem=list_item,isFolder=False)
            """

        xbmcplugin.addSortMethod(handle=self.plugin_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(self.plugin_handle)
