# # -*- coding: UTF-8 -*-

#
# Imports
#
import os
import re
import sys
import urllib
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from resources.lib import core
from resources.lib import crtvg_utils





LIB_DIR = xbmc.translatePath( os.path.join( xbmcaddon.Addon(id='plugin.video.crtvg-acarta').getAddonInfo('path'), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

from crtvg_const import ADDON, SETTINGS, LANGUAGE, IMAGES_PATH, DATE, VERSION


if len(sys.argv[2]) == 0:
    # Menu Principal
   #xbmc.log("[ADDON] %s, Python Version %s" % (ADDON, str(sys.version)), xbmc.LOGDEBUG)
    #xbmc.log( "[ADDON] %s v%s (%s) is starting, ARGV = %s" % ( ADDON, VERSION, DATE, repr(sys.argv) ), xbmc.LOGDEBUG )
    import crtvg_main as plugin
    
else:
    action = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['action'][0]
    #crtvg_utils.msg(action)
    # Novedades
    #
    if action:
        if action == 'novedades':
            import crtvg_novedades as plugin
        elif action == 'programas':
            import crtvg_az_beta as plugin
    # Episodios
        elif action == 'episodios':
            import crtvg_episodios as plugin
    # Categorias
        elif action == 'categorias':
            import crtvg_categorias as plugin
   # Directos
        elif action == 'directos':
            import crtvg_directos as plugin
   # Destacados
        elif action == 'destacados':
            import crtvg_destacados as plugin
   # Alfabetico
        elif action == 'alfabetico':
            import crtvg_alfabetico as plugin
    # Reproducir
        elif action == 'play':
            import crtvg_reproducir as plugin
    # Reproducir Radio
        elif action == 'play_radio':
            import crtvg_reproducir_radio as plugin

    # ... Pruebas ...
        elif action == 'pruebas':
            import crtvg_pruebas as plugin
    # Radio Galega
        elif action == 'radio':
            import crtvg_radio as plugin

    # ... No tiene ...
        elif action == 'nada':
          exit()  
        
        elif action == 'main':
        	import crtvg_main as plugin  


plugin.Main()