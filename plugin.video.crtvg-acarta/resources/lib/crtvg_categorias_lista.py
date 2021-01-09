
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
from crtvg_const import * #ADDON, SETTINGS, LANGUAGE, IMAGES_PATH, DATE, VERSION

#urlACartaAlfabetico = "http://www.crtvg.es/api/?key=apffh343444-dddkk9913833-aoijer0333-34poaskflas033-00AAAddd002233&idseccion=297&limite=0&idioma=glg&metadatos=true&filtros=Metadatodata.disponible_na_app:EQ:1&orden=Entrada.titulo&orden_direccion=ASC"
#urlACartaAlfabetico = "http://www.crtvg.es/api/?key=apffh343444-dddkk9913833-aoijer0333-34poaskflas033-00AAAddd002233&idseccion=294&idioma=glg&metadatos=true&limite=0&orden=fecha_publicacion&orden_direccion=DESC&nivel=1&filtros=Metadatodata.programa_tvg:EQ:"

#
# Main class
#

class Programa(object):
    def __init__ (self, uID, uTitulo, uMiniatura, uContenido, uResumen, uEnlace, uCategorias):
        self.ID = uID
        self.Titulo = uTitulo
        self.Miniatura = uMiniatura
        self.Contenido = uContenido
        self.Resumen = uResumen
        self.Enlace = uEnlace
        self.Categorias = uCategorias
    
    def __str__(self):
        return "%s - %s - %s - %s - %s - %s -%s" % (self.ID, self.Titulo, self.Miniatura, self.Contenido, self.Resumen, self.Enlace, self.Categorias)
    
    def __getitem__(self, item):
        return (self.ID, self.Titulo, self.Miniatura, self.Contenido, self.Resumen, self.Enlace, self.Categorias)[item]

class Categoria(object):
    def __init__ (self, uID, uTitulo):
        self.ID = uID
        self.Titulo = uTitulo
    def __str__(self):
        return "%s - %s" % (self.ID, self.Titulo)
    def __getitem__(self, item):
        return (self.ID, self.Titulo)[item]



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

       #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Iniciando : -> ", str(__file__) + " Beta..."),#xbmc.logDEBUG)
        self.video_list_page_url = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['url'][0]
        
        Programas = []
        Categorias = []
        datos1 = scrapertools.cache_page(urlACartaAlfabetico)
        #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "json_data : -> Data...", str(datos1)),#xbmc.logDEBUG)

        if datos1 == '':
            msgError('Error obteniendo datos', 'Se ha producido un error obteniendo los datos del servidor.\nIntentelo de nuevo mas tarde.\n')
            #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Error desacargando datos [datos1] = ", "[sin datos]"),#xbmc.logDEBUG)
            sys.exit('\nERROR: Se ha producido un error obteniendo los datos del servidor.\nIntentelo de nuevo mas tarde.\n')

        #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "json_data : -> Data...", str(datos1)),#xbmc.logDEBUG)
        
        json_data = jsontools.load_json(datos1)
        #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "json_data : -> Data...", str(json_data)),#xbmc.logDEBUG)
        
        for i in range (0, len (json_data['Entradas'])):
            if json_data['Entradas'][i]['titulo']: # ID 
                ID = json_data['Entradas'][i]['id'] # ID 
                sTitulo = json_data['Entradas'][i]['titulo'] # Titulo
                sTitulo = scrapertools.htmlclean(sTitulo)
                sMiniatura = urlparse.urljoin(urlThumbs, json_data['Entradas'][i]['archivo']) # Thumbnail
                sContenido = scrapertools.htmlclean(json_data['Entradas'][i]['contenido']) # Contenido
                sResumen = scrapertools.htmlclean(json_data['Entradas'][i]['resumen']) # Resumen
                sEnlace = json_data['Entradas'][i]['Extra']['url'] # Pagina

                Categorias = []
                for cat in json_data['Entradas'][i]['Categorias']:
                    if cat == '':
                        cat_id = '999'
                        cat_titulo = 'Non definido'
                    else:
                        cat_id = json_data['Entradas'][i]['Categorias'][cat]['id']
                        cat_titulo = json_data['Entradas'][i]['Categorias'][cat]['titulo']
                    uCategoria = Categoria(cat_id, cat_titulo)
                    Categorias.append(uCategoria)
                #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Categorias : -> " + sTitulo, cat_titulo),#xbmc.logDEBUG)
                uProg = Programa(ID, sTitulo, sMiniatura, sContenido, sResumen, sEnlace, Categorias)
                Programas.append(uProg)
        
        iCat = 'Musicais'
        programas_filtrados = []
        for nProg in Programas:
            nCategorias = nProg.Categorias
            for pCategorias in nCategorias:
                cat_id = pCategorias.ID
                Cat_Titulo = pCategorias.Titulo
                #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Categorias : -> "+ nProg.Titulo, str(Cat_Titulo)),#xbmc.logDEBUG)
                if  (iCat == Cat_Titulo): #and (nProg not in programas_filtrados):
                    programas_filtrados.append(nProg)
       
        #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Programas : -> ", str(programas_filtrados)),#xbmc.logDEBUG)

        i = -1
        p = len(programas_filtrados) -1
                
        for sPrograma in programas_filtrados:
            ID = sPrograma.ID
            Titulo = sPrograma.Titulo.strip()
            Enlace = urlparse.urljoin(urlACarta, sPrograma.Enlace)
            
            if sPrograma.Miniatura == '':
                Miniatura = MINIATURA_GENERAL
            else:
                Miniatura = urlparse.urljoin(urlThumbs, sPrograma.Miniatura)

            Resumen = acentos(sPrograma.Resumen)
            Contenido = acentos(sPrograma.Contenido)
            
            i += 1
            ultimo = False
            if i == p:
                ultimo = True

            inserta_programa(Titulo, "episodios", Enlace, "", Miniatura, resumen=Resumen, num_pagina="1", es_directorio=True, es_ultimo=ultimo)
    

        """
        file = open(os.path.join('d:', '_testfile_.txt'),'a') 
        #file.write('.... pag ....' + pag + ' ......\n') 
        file.write('--------------------------------------------------------------------------------------\n\n')
        file.write(datos+'\n\n')
        file.write('--------------------------------------------------------------------------------------\n\n') 
        """
