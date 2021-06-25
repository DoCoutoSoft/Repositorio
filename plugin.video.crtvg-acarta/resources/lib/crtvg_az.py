
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
import crtvg_server as servermodule

from crtvg_const import ADDON, SETTINGS, LANGUAGE, IMAGES_PATH, DATE, VERSION
from core import scrapertools
from core import jsontools
from crtvg_utils import *


#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__(self):
        # Get the command line arguments
        # Get the plugin url in plugin:// notation
        self.plugin_url = sys.argv[0]
        # Get the plugin handle as an integer number
        self.plugin_handle = int(sys.argv[1])

       #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Iniciando : -> ", str(__file__)),#xbmc.logDEBUG)

        # Parse parametros
        #elf.plugin_category = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['plugin_category'][0]
        self.video_list_page_url = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['url'][0]
        #elf.next_page_possible = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['next_page_possible'][0]

        

        datos1 = scrapertools.cache_page(self.video_list_page_url)
        datos2 = scrapertools.get_match(datos1,"<!-- LISTADO DE LA A A LA Z -->(.*?)<!-- LISTADO POR CAT")

        """
        <div class="item-a-carta">
            <a href="/tvg/a-carta/programa/15-zona-cerco-aos-matalobos"
                title="15 Zona: cerco aos Matalobos">
                15 Zona: cerco aos Matalobos
            </a>
        </div>
        """

        patron  = '<div class="item-a-carta"[^<]+'
        patron += '<a href="([^"]+)"[^>]+>([^<]+)<'


        encontrados = re.compile(patron,re.DOTALL).findall(datos2)

        for url_encontrada, titulo_encontrado in encontrados:
            titulo = titulo_encontrado.strip()
            enlace = urlparse.urljoin(self.video_list_page_url,url_encontrada)
            miniatura = MINIATURA_GENERAL
            plot = ""
            liStyle = xbmcgui.ListItem(label=titulo, thumbnailImage=miniatura)
            liStyle.setInfo("video", {"title": titulo, "studio": ADDON})
            liStyle.setArt({'icon': '', 'fanart': ''})
            liStyle.setArt({'thumb': os.path.join(IMAGES_PATH, 'chapter.png'), 'icon': os.path.join(IMAGES_PATH, 'chapter.png'), 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
            addDirectoryItem({"action": "episodios","url": enlace}, liStyle)            
       
        xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

