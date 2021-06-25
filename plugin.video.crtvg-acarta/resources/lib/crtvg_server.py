# -*- coding: utf-8 -*-

import urlparse,urllib2,urllib,re
import os
import sys

import xbmc, xbmcaddon
import xbmcgui
import xbmcplugin

from core import scrapertools
from core import logger
from core import config
from crtvg_const import ADDON, SETTINGS, LANGUAGE, IMAGES_PATH, DATE, VERSION
from crtvg_utils import *


def obten_enlace_video( page_url , premium = False , user="" , password="", video_password="", page_data="" ):
    #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "crtvg_server.obten_enlace_video de: -> ", page_url),#xbmc.logDEBUG)

    if page_data=="":
        data = scrapertools.cache_page(page_url)
    else:
        data = page_data

    video_urls = []

    # media_url = scrapertools.find_single_match(data,"var url = '([^']+)'") + "/playlist.m3u8"
    patron  = 'var url = "([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if not matches:
        media_url = ""
    else:
        media_url = matches[0] + "/playlist.m3u8"
    
    return media_url

def obten_enlace_radio( page_url , premium = False , user="" , password="", video_password="", page_data="" ):
    #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "crtvg_server.obten_enlace_video de: -> ", page_url),#xbmc.logDEBUG)

    if page_data=="":
        data = scrapertools.cache_page(page_url)
    else:
        data = page_data

    video_urls = []

    # media_url = scrapertools.find_single_match(data,"var url = '([^']+)'") + "/playlist.m3u8"
    patron  = 'var url = "([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if not matches:
        media_url = ""
    else:
        media_url = matches[0] #+ "/playlist.m3u8"
    
    return media_url

def obten_miniatura_capitulo( page_url, page_data="" ):
    #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "crtvg_server.obten_enlace_video de: -> ", page_url),#xbmc.logDEBUG)

    if page_data=="":
        data = scrapertools.cache_page(page_url)
    else:
        data = page_data

    """
    playlist: [{
            mediaid: 'Capítulo 93: A culpa - Á carta',
            image: "http://www.crtvg.es/files/web/20171123080912_8.png",
    """

    patron  = 'playlist\: \[{.*?image\: "([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    if not matches:
        thumb_url = ""
    else:
        thumb_url = matches[0]
    
    return thumb_url

def obten_titulo_directos( page_url, page_data="" ):
    #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "crtvg_server.obten_enlace_video de: -> ", page_url),#xbmc.logDEBUG)

    if page_data=="":
        datos = scrapertools.cache_page(page_url)
    else:
        datos = page_data

    """
    <h2 class="destacado-info-titulo-programa">
        <a href="/tvg/programas/ti-veras" title="Ti verás">Ti verás</a>                    
    </h2>
    """

    patron  = '<h2 class="destacado-info-titulo-programa"[^<]+'
    patron += '<a href="([^"]+)"[^>]+>([^<]+)<'

    encontrados = re.compile(patron,re.DOTALL).findall(datos)
    if not encontrados:
        titulo = "(Sen título)"
        return titulo
    
    for url_encontrada, titulo_encontrado in encontrados:
        titulo = titulo_encontrado.strip()
    return titulo

def obten_resumen_directos( page_url, page_data="" ):
    #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "crtvg_server.obten_enlace_video de: -> ", page_url),#xbmc.logDEBUG)

    if page_data=="":
        datos = scrapertools.cache_page(page_url)
    else:
        datos = page_data

    """
    <div class="destacado-info-resumen">
        <p><strong>Ti ver&aacute;s</strong> &eacute; un concurso diario presentado por Rodrigo V&aacute;zquez que combina unha aditiva din&aacute;mica de xogo e o aspecto m&aacute;is humano e interactivo do 'talk show'. As parellas concursantes deben responder correctamente 8 preguntas e abrir 8 das 10 bonecas rusas xigantes para conseguir a maior cantidade de cartos posibles. Dentro de cada boneca pode haber ata cinco m&aacute;is ou pode non haber ningunha. Cantas m&aacute;is bonecas garden as matrioskas no seu interior, maior ser&aacute; a cuant&iacute;a dos cartos en xogo. Se seguen abrindo e non hai boneca, perder&aacute;n todo o ga&ntilde;ado. Para poder xogar cunha boneca e realizar a primeira apertura deben escoller unha categor&iacute;a entre dez posibles temas e seleccionar a opci&oacute;n correcta entre verdadeiro ou falso.</p>
    </div>

    """
   
    patron  = '<meta property="og:description" content="([^"]+)"'
    resumen_encontrado = scrapertools.find_single_match(datos, patron)
    if not resumen_encontrado:
        resumen = "(Sen resumen)"
        return resumen

    resumen = resumen_encontrado.strip()
    return acentos(resumen)

def obten_resumen_radios( page_url, page_data="" ):
    #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "crtvg_server.obten_enlace_video de: -> ", page_url),#xbmc.logDEBUG)

    if page_data=="":
        datos = scrapertools.cache_page(page_url)
    else:
        datos = page_data

    """
    <div class="destacado-info-resumen">
        <p><strong>Ti ver&aacute;s</strong> &eacute; un concurso diario presentado por Rodrigo V&aacute;zquez que combina unha aditiva din&aacute;mica de xogo e o aspecto m&aacute;is humano e interactivo do 'talk show'. As parellas concursantes deben responder correctamente 8 preguntas e abrir 8 das 10 bonecas rusas xigantes para conseguir a maior cantidade de cartos posibles. Dentro de cada boneca pode haber ata cinco m&aacute;is ou pode non haber ningunha. Cantas m&aacute;is bonecas garden as matrioskas no seu interior, maior ser&aacute; a cuant&iacute;a dos cartos en xogo. Se seguen abrindo e non hai boneca, perder&aacute;n todo o ga&ntilde;ado. Para poder xogar cunha boneca e realizar a primeira apertura deben escoller unha categor&iacute;a entre dez posibles temas e seleccionar a opci&oacute;n correcta entre verdadeiro ou falso.</p>
    </div>

    """
   
    patron  = '<div class="destacado-info-resumen">(.*)</div>'
    resumen_encontrado = scrapertools.find_single_match(datos, patron)
    resumen_encontrado = scrapertools.htmlclean(resumen_encontrado)
    #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "crtvg_server.obten_resumen_encontrado_radio de: -> ", resumen_encontrado), xbmc.LOGDEBUG)
    
    if not resumen_encontrado:
        resumen = "(Sen resumen)"
        return resumen

    resumen = resumen_encontrado.strip()
    #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "resumen_encontrado_radio: -> ", resumen), xbmc.LOGDEBUG)
    return acentos(resumen)
