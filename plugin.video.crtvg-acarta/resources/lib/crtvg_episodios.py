
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

from crtvg_const import ADDON, SETTINGS, LANGUAGE, IMAGES_PATH, DATE, VERSION, MINIATURA_GENERAL
from crtvg_utils import *
from core import scrapertools
from core import jsontools


#
# Main class
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
        num_pagina = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['pagina'][0]

        if "/ax/" in self.video_list_page_url:
            headers=[]
            headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:17.0) Gecko/20100101 Firefox/17.0"])
            headers.append(["X-Requested-With","XMLHttpRequest"])
            headers.append(["Referer",self.video_list_page_url])
            data = scrapertools.cache_page(self.video_list_page_url, post="", headers=headers)
            data = data.replace("\\n"," ")
            data = data.replace("\\\"","\"")
            data = data.replace("\\/","/")
        else:
            data = scrapertools.cache_page(self.video_list_page_url)
            try:
                id_programa = scrapertools.get_match(data,"initAlaCartaBuscador.(\d+)")
            except:
                id_programa = ""


            #http://www.crtvg.es/ax/tvgalacartabuscador/programa:33517/pagina:1/seccion:294/titulo:/mes:null/ano:null/temporada:null
            url = "http://www.crtvg.es/ax/tvgalacartabuscador/programa:"+id_programa+"/pagina:"+num_pagina+"/seccion:294/titulo:/mes:null/ano:null/temporada:null"
            headers=[]
            headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:17.0) Gecko/20100101 Firefox/17.0"])
            headers.append(["X-Requested-With","XMLHttpRequest"])
            headers.append(["Referer",self.video_list_page_url])
            datos = scrapertools.cache_page(url, post="", headers=headers)
            datos = datos.replace("\\n"," ")
            datos = datos.replace("\\\"","\"")
            datos = datos.replace("\\/","/")
            #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Datos Episodios : -> ", datos),#xbmc.logDEBUG)


        patron  = '<tr[^<]+'
        patron += '<td class="a-carta-resultado-titulo[^<]+'
        patron += '<a href="([^"]+)"\s+title="([^"]+)".*?'
        patron += '<td class="a-carta-resultado-data">(.*?)</td>'
        matches = re.compile(patron,re.DOTALL).findall(datos)
        
       #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Datos Episodios : -> ", '['+str(matches)+']'),#xbmc.logDEBUG)
        if matches == []:
            titulo = '(Non se atoparon videos)'
            miniatura = os.path.join(IMAGES_PATH, 'no-video.png')
            num_pagina = '1'
            media_url = 'nada'
            inserta_capitulo(titulo, enlace=media_url, categoria='nada', miniatura=miniatura, resumen="", num_pagina=num_pagina, es_directorio=False, es_ultimo=True)
            exit()


        list_item = []
        for url_encontrada,titulo_encontrado, fecha_encontrada in matches:
            titulo = titulo_encontrado.strip()
            json_title = jsontools.load_json('{"title":"'+titulo+'"}')
            titulo = json_title["title"]
            titulo = scrapertools.htmlclean(titulo)+" - "+ fecha_encontrada.strip()

            url = urlparse.urljoin(self.video_list_page_url,url_encontrada)
            
            video_urls = servermodule.obten_enlace_video(url)
            media_url = str(video_urls)

            thumb_url = servermodule.obten_miniatura_capitulo(url)
            
            if thumb_url == "":
                miniatura = os.path.join(IMAGES_PATH, 'movie.png')
            else:
                miniatura = thumb_url

            inserta_capitulo(titulo, enlace=media_url, categoria='episodios', miniatura=miniatura, resumen="", num_pagina=num_pagina, es_directorio=False, es_ultimo=False)


        if datos.find('Seguinte') > -1:
            nueva_pagina = int(num_pagina) +1
            pagina_siguiente = str(nueva_pagina)

            nueva_pagina = str(int(num_pagina ) +1)
            parametros = {"action": "episodios","url": url, "pagina": pagina_siguiente}
            url = self.plugin_url + '?' + urllib.urlencode(parametros)
            inserta_programa('Páxina Seguinte ('+pagina_siguiente+')', "episodios", enlace=url, categoria="episodios", miniatura=miniatura, resumen="Ir á paxina seguinte...", num_pagina=nueva_pagina, es_directorio=True, es_ultimo=False)
      

        xbmcplugin.addSortMethod(handle=self.plugin_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(self.plugin_handle)
