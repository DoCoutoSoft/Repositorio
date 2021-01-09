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
from crtvg_az_beta import Programa
from crtvg_az_beta import Categoria


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

        self.video_list_page_url = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['url'][0]

        Programas = []
        Categorias = []
        tmp = scrapertools.cache_page(urlACartaAlfabetico)
        json_data = jsontools.load_json(tmp)

        for i in range (0, len (json_data['Entradas'])):

            ID = json_data['Entradas'][i]['id'] # ID 
            sTitulo = json_data['Entradas'][i]['titulo'] # Titulo
            sTitulo = scrapertools.htmlclean(sTitulo)
            sMiniatura = urlparse.urljoin(urlThumbs, json_data['Entradas'][i]['archivo']) # Thumbnail
            sContenido = scrapertools.htmlclean(json_data['Entradas'][i]['contenido']) # Contenido
            sResumen = scrapertools.htmlclean(json_data['Entradas'][i]['resumen']) # Resumen
            sEnlace = json_data['Entradas'][i]['Extra']['url'] # Pagina

            for cat in json_data['Entradas'][i]['Categorias']:
                cat_titulo = json_data['Entradas'][i]['Categorias'][cat]['titulo']
                cat_id = json_data['Entradas'][i]['Categorias'][cat]['titulo']
                
                uCategoria = Categoria(cat_id, cat_titulo)
                Categorias.append(uCategoria)

            uProg = Programa(ID, sTitulo, sMiniatura, sContenido, sResumen, sEnlace, Categorias[0].Titulo)
            Programas.append(uProg)



        datos1 = scrapertools.cache_page(self.video_list_page_url)
        datos2 = scrapertools.get_match(datos1,"<!-- LISTADO POR CAT(.*?)</ul>")
        patron = '<div class="item-a-carta(.*?)</div>'
        
        matches = re.compile(patron,re.DOTALL).findall(datos2)

        accion = ""
        for bloque in matches:
            if "<h3>" in bloque:
                scrapedtitle = "[COLOR springgreen]"+scrapertools.get_match(bloque,"<h3>([^<]+)</h3>").strip().upper()+"[/COLOR]"
                scrapedurl=""
                folder=False
                accion = "nada"
                scrapedthumbnail = MINIATURA_GENERAL
            else:
                scrapedtitle = "  "+scrapertools.get_match(bloque,'<a href="[^"]+"[^>]+>([^<]+)<').strip()
                scrapedurl = urlparse.urljoin(self.video_list_page_url,scrapertools.get_match(bloque,'<a href="([^"]+)"[^>]+>[^<]+<').strip())
                folder=True
                accion = "episodios"
                scrapedthumbnail = MINIATURA_GENERAL
                for i in range (0, len (Programas)):
                    programa = Programas[i]
                    if programa.Titulo == scrapedtitle.strip():
                       #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "tit: -> ", "["+str(programa.Titulo)+"] ["+scrapedtitle.strip()+"]"),#xbmc.logDEBUG)
                        scrapedthumbnail = programa.Miniatura
                        break
                
            scrapedplot = ""

            inserta_programa(scrapedtitle, accion, scrapedurl, "", miniatura=scrapedthumbnail, resumen="", num_pagina="1", es_directorio=folder, es_ultimo=False)
       
        xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

