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
from core import tools

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
        
        html_full = scrapertools.cache_page(self.video_list_page_url)
        html_strip = scrapertools.find_single_match(html_full,"PESTAÑAS -->(.*?)<!--")
        
        #patron  = '<a href="([^"]+)" title="([^"]+)"[^<]+'
        #patron += '<img src="([^"]+)".*?'
        #patron += '<div class="entrada-blog-fecha[^>]+>([^<]+)<'
        #encontrados = re.compile(patron,re.DOTALL).findall(datos)

        patron = '<ul class="categorias" id="tabs-a-carta">(.*?)</ul>'
        html_found = scrapertools.find_single_match(html_strip,patron)
        patrones = 'href="([^"]+)" title="([^"]+)"[^<]+'
        cat = re.compile(patrones,re.DOTALL).findall(html_found)

        
        for html_link, html_label, in cat:
            enlace  = html_link.strip()
           #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Enlace -> ", str('->' + enlace + '<- ')),#xbmc.logDEBUG)
            #enlace = urlparse.urljoin(self.video_list_page_url, enlace)
            accion = 'nada'
            if enlace == '#caja-ultimos':
                accion = 'novedades'
            elif enlace == '#caja-letras':
                accion = 'programas'
            elif enlace == '#caja-categorias':
               accion = 'categorias'
            else:
               accion = 'nada'
            
            titulo = scrapertools.htmlclean(html_label)
            folder=True
            scrapedthumbnail = MINIATURA_GENERAL
            inserta_programa(titulo, accion, urlACarta, "", miniatura=scrapedthumbnail, resumen='', num_pagina="1", es_directorio=folder, es_ultimo=False)

            
        xbmcplugin.addSortMethod(handle=self.plugin_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
