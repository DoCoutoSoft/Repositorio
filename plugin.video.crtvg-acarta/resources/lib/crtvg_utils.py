# -*- coding: UTF-8 -*-

import gzip
import httplib
import urllib, urlparse, urllib2, sys
import re,xbmc, xbmcplugin, xbmcgui, xbmcaddon, os, sys, time
from crtvg_const import *
from core import scrapertools

#
handle = int(sys.argv[1])
#
def existe_archivo(url):
    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request)
        return True
    except:
        return False

def msgError(titulo, mensaje):
    dialog = xbmcgui.Dialog()
    i = dialog.ok(titulo, mensaje)
    return i


def msg(mensaje):
    dialog = xbmcgui.Dialog()
    i = dialog.ok('Información', mensaje)
    return i

def getParams(arg):
        param=[]
        paramstring=arg
        if len(paramstring)>=2:
            params=arg
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:    
                    param[splitparams[0]]=splitparams[1]
                                
        return param

def traduce(arg):
        return LANGUAGE(arg)
        
def inserta_menu_prinicpal(parameters, li):
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li, isFolder=True)

def inserta_programa(titulo=None, accion=None, enlace=None, categoria="", miniatura="", resumen="", num_pagina=None, es_directorio=True, es_ultimo=False):
    if categoria == "":
        try:
            categoria = unicode( CANAL, "utf-8" ).encode("iso-8859-1")
        except:
            pass
    
    import xbmc

   
    if miniatura.startswith("http://") or miniatura.startswith("https://"):
        thumbnail = miniatura
    else:
        thumbnail = os.path.join(IMAGES_PATH, miniatura)

    import xbmcgui
    import xbmcplugin
    
    liStyle = xbmcgui.ListItem(label=titulo, thumbnailImage=thumbnail)
    liStyle.setInfo("video", {"title": titulo, "studio": ADDON, "Plot" : resumen})
    liStyle.setArt({'thumb': thumbnail, 'icon': thumbnail, 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
    liStyle.setProperty('IsPlayable', 'false')
        
    parametros = '%s?channel=%s&url=%s&action=%s&category=%s&pagina=%s&resumen=%s' % ( sys.argv[ 0 ], titulo, enlace, accion, categoria, num_pagina, resumen)
    xbmcplugin.addDirectoryItem(handle = int(sys.argv[ 1 ]), url =parametros, listitem=liStyle, isFolder=es_directorio)
    if es_ultimo:
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))


def inserta_capitulo(titulo=None, enlace=None, categoria="", miniatura="", resumen="", num_pagina=None, es_directorio=True, es_ultimo=False):
    if categoria == "":
        try:
            categoria = unicode( CANAL, "utf-8" ).encode("iso-8859-1")
        except:
            pass
    
    import xbmc

   
    if miniatura.startswith("http://") or miniatura.startswith("https://"):
        thumbnail = miniatura
        if not existe_archivo(miniatura):
            thumbnail = os.path.join(IMAGES_PATH, MINIATURA_GENERAL)

    else:
        thumbnail = os.path.join(IMAGES_PATH, miniatura)


    import xbmcgui
    import xbmcplugin
    
    liStyle = xbmcgui.ListItem(label=titulo, thumbnailImage=thumbnail)
    liStyle.setInfo( type="Video", infoLabels={ "Title": titulo, "Plot": resumen} )
    liStyle.setArt({'thumb': thumbnail, 'icon': thumbnail, 'fanart': os.path.join(IMAGES_PATH, 'fanart.jpg')})
    liStyle.setProperty('IsPlayable', 'true')
    #listitem = xbmcgui.ListItem( titulo , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    accion = 'play'
    itemurl = '%s?channel=%s&url=%s&action=%s&category=%s&pagina=%s&resumen=%s' % ( sys.argv[ 0 ], titulo, enlace, accion, categoria, num_pagina, resumen)
    xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url =itemurl , listitem=liStyle, isFolder=es_directorio)
    if es_ultimo:
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))

def inserta_radio(titulo=None, enlace=None, categoria="", miniatura="", resumen="", num_pagina=None, es_directorio=True, es_ultimo=False):
    if categoria == "":
        try:
            categoria = unicode( CANAL, "utf-8" ).encode("iso-8859-1")
        except:
            pass
    
    import xbmc

   
    if miniatura.startswith("http://") or miniatura.startswith("https://"):
        thumbnail = miniatura
        if not existe_archivo(miniatura):
            thumbnail = os.path.join(IMAGES_PATH, MINIATURA_GENERAL)
    else:
        thumbnail = os.path.join(IMAGES_PATH, miniatura)

    import xbmcgui
    import xbmcplugin
    
    liStyle = xbmcgui.ListItem(label=titulo, thumbnailImage=thumbnail)
    liStyle.setInfo( type="Video", infoLabels={ "Title": titulo, "Plot": resumen} )
    liStyle.setArt({'thumb': thumbnail, 'icon': thumbnail, 'fanart': os.path.join(IMAGES_PATH, 'fanart_radio.jpg')})
    liStyle.setProperty('IsPlayable', 'true')
    
    accion = 'play_radio'
    pista = enlace 
    itemurl = enlace #'%s?channel=%s&url=%s&action=%s&category=%s&pagina=%s&resumen=%s' % ( sys.argv[ 0 ], titulo, enlace, accion, categoria, num_pagina, resumen)
    xbmcplugin.addDirectoryItem(handle = int(sys.argv[ 1 ]), url =itemurl ,  listitem=liStyle,  isFolder=es_directorio)
    if es_ultimo:
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))

def acentos(texto=""):
    #Minúsculas:
    if texto=="":
        Restultado = ""
        
    else:
        Resultado = texto.replace("&aacute;","á")
        Resultado = Resultado.replace("&eacute;","é")
        Resultado = Resultado.replace("&iacute;","í")
        Resultado = Resultado.replace("&oacute;","ó")
        Resultado = Resultado.replace("&uacute;","ú")
     
        #Mayúsculas:
        Resultado = Resultado.replace("&Aacute;","Á")
        Resultado = Resultado.replace("&Eacute;","É")
        Resultado = Resultado.replace("&Iacute;","Í")
        Resultado = Resultado.replace("&Oacute;","Ó")
        Resultado = Resultado.replace("&Uacute;","Ú")
        
        #Tildes graves:
        Resultado = Resultado.replace("&agrave;","à")
        Resultado = Resultado.replace("&egrave;","è")
        Resultado = Resultado.replace("&igrave;","ì")
        Resultado = Resultado.replace("&ograve;","ò")
        Resultado = Resultado.replace("&ugrave;","ù")
     
        #Tildes graves mayúsculas:
        Resultado = Resultado.replace("&Agrave;","À")
        Resultado = Resultado.replace("&Egrave;","È")
        Resultado = Resultado.replace("&Igrave;","Ì")
        Resultado = Resultado.replace("&Ograve;","Ò")
        Resultado = Resultado.replace("&Ugrave;","Ù")
        return Resultado


def filtrar_categoria(ilista, ivalor, limit=None):
    nueva_lista = []
    for i in range (0, len(ilista)):
        if ilista[i].Categoria == ivalor:
            nueva_lista.append(ilista[i])
    return nueva_lista


def parse_m3u(infile):

    html_full = scrapertools.cache_page(infile)    
    xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Iniciando Full : -> ", html_full), xbmc.LOGDEBUG)
    pista = ''
    patron = 'http://(.*)'
    lineas = scrapertools.find_single_match(html_full, patron)
    #lineas = re.compile(patron,re.DOTALL).findall(html_full)
    #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Iniciando Full : -> ", lineas), xbmc.LOGDEBUG)

    if lineas == '':
        return
    
    for enlace in lineas:
        pista  = infile #'http://' + enlace.strip()
    
        
    return pista
    