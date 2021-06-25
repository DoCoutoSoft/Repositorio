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

from core import scrapertools
from core import jsontools
from crtvg_utils import *
from crtvg_const import *

#
# Main class destacados...
#
class Main:
    #
    # Init
    #
    def __init__(self):
        self.plugin_url = sys.argv[0]
        self.plugin_handle = int(sys.argv[1])

       #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Iniciando : -> ", str(__file__)),#xbmc.logDEBUG)

        self.video_list_page_url = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['url'][0]

        datos = scrapertools.cache_page(self.video_list_page_url)
        
        """
        </div>
        <a href="/tvg/a-carta/campana-cierraunicef-al-bano-e-lila-downs" title="Campaña 'cierraUNICEF', Al Bano e Lila Downs">
            <img src="/files/thumbs/002520171124000000.jpg" alt="Campaña 'cierraUNICEF', Al Bano e Lila Downs" width="190" height="106">
            <div class="osmaisvistos-info">
                <h2>Luar</h2>
                <h3>Campaña 'cierraUNICEF', Al Bano e Lila Downs</h3>
                <div class="entrada-blog-fecha">
                    24/11/2017 / 22:00 h
                </div>
            </div>
        </a>
        </div>        
        """

        patron  = '<a href="([^"]+)" title="([^"]+)"[^<]+'
        patron += '<img src="([^"]+)".*?'
        patron += '<div class="entrada-blog-fecha[^>]+>([^<]+)<'

        encontrados = re.compile(patron,re.DOTALL).findall(datos)

        for url_encontrada, titulo_encontrado, miniatura_encontrada, fecha_encontrada in encontrados:
            titulo = titulo_encontrado.strip()
            titulo = scrapertools.htmlclean(titulo) + " - " + fecha_encontrada.strip()
            enlace = urlparse.urljoin(self.video_list_page_url, url_encontrada)
            miniatura = urlparse.urljoin(self.video_list_page_url, miniatura_encontrada)
            if miniatura == "":
                miniatura = MINIATURA_GENERAL

            import crtvg_server as servermodule
            video_urls = servermodule.obten_enlace_video(enlace)
            media_url = str(video_urls)
            if media_url == "":
                crtvg_utils.msgerror("Erro obtendo datos do programa " + titulo,"Non se atoparon videos. Ténteo mais tarde")
                return
            else:
                inserta_capitulo(titulo, enlace=media_url, categoria="play", miniatura=miniatura, resumen="", num_pagina="1", es_directorio=False, es_ultimo=False)

        xbmcplugin.addSortMethod(handle=self.plugin_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(self.plugin_handle)
