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

        #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Iniciando : -> ", str(__file__)), xbmc.LOGDEBUG)

        self.video_list_page_url = urlRadioGalega

        datos1 = scrapertools.cache_page(self.video_list_page_url)
        datos2 = scrapertools.find_single_match(datos1,"VER DESPOIS -->(.*?)<!-- FIN ENTRADA")
        xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Datos Ver Despois : -> ", str(datos2)), xbmc.LOGDEBUG)
        
        patron = '<a class=.*?href="([^"]+)"\s+title="([^"]+)"'

        matches = re.compile(patron,re.DOTALL).findall(datos2)
        list_item = []
        for scrapedurl,scrapedtitle in matches:
            titulo = scrapedtitle.strip()
            titulo = scrapertools.htmlclean(titulo)
            enlace = urlparse.urljoin(self.video_list_page_url,scrapedurl)

            datos_directo = scrapertools.cache_page(enlace)
            import crtvg_server as servermodule
            video_urls = servermodule.obten_enlace_radio(enlace, page_data=datos_directo)
            media_url = str(video_urls)
            miniatura = servermodule.obten_miniatura_capitulo(enlace, page_data=datos_directo)
            url = enlace

            if not miniatura:
                miniatura = MINIATURA_GENERAL

            
            programa_emitido = servermodule.obten_titulo_directos(enlace, page_data=datos_directo)
            #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Directos Titulo : -> ", str(programa_emitido)), xbmc.LOGDEBUG)
            
            resumen_emitido = servermodule.obten_resumen_radios(enlace, page_data=datos_directo)
            plot = "Emitindo actualmente:\n" + programa_emitido + '\n' + resumen_emitido.strip()
            #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Radios Resumen : -> ", str(plot)), xbmc.LOGDEBUG)

            list_item = xbmcgui.ListItem(label=titulo, thumbnailImage=miniatura)
            list_item.setInfo("Video", {"title": titulo, "studio": ADDON})
            list_item.setArt({'thumb': miniatura, 'icon': miniatura, 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
            list_item.setProperty('IsPlayable', 'true')
            parameters = {"action": "play_radio", "url": media_url, "title": titulo}
            url = self.plugin_url + '?' + urllib.urlencode(parameters)
            is_folder = False
            
            inserta_radio(titulo, enlace=media_url, categoria="play_radio", miniatura=miniatura, resumen=plot, num_pagina="1", es_directorio=is_folder, es_ultimo=False)
            #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "media_url : -> ", str(media_url)), xbmc.LOGDEBUG)

        xbmcplugin.addSortMethod(handle=self.plugin_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(self.plugin_handle)

