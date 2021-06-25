
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
import crtvg_utils
from crtvg_const import *
from resources.lib import core

#
# Main class
#
class Main:

    def __init__(self):
        self.plugin_url = sys.argv[0]
        self.plugin_handle = int(sys.argv[1])
        #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Iniciando : -> ", str(__file__)), xbmc.LOGDEBUG)

        self.video_list_page_url = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['url'][0]
        
        listitem = xbmcgui.ListItem()
        listitem.setPath(self.video_list_page_url)
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        
        try:
            
            #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Reproducir Track : -> ", '->'+playlist+'<--'), xbmc.LOGDEBUG)        
            #xbmcplugin.setResolvedUrl(self.plugin_handle, succeeded = True, listitem = listitem)
            xbmc.PlayListItem(listitem)
        except:
            pass
            crtvg_utils.msgError("Reproducir radio","Erro ao reproducir o canle seleccionado")
           
