
# -*- coding: UTF-8 -*-

#
# Imports
#
import os
import re
import sys
import urllib
import urllib2
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
import os
import sys


from crtvg_const import *
from core import scrapertools
from core import config
from crtvg_utils import HTTPCommunicator

#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__(self):

        self.plugin_url = sys.argv[0]
        # Get the plugin handle as an integer number
        self.plugin_handle = int(sys.argv[1])




        dialog = xbmcgui.Dialog()
        i = dialog.yesno("Are you sane", "At least some of the time")

       #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "Play->", ' PlayVideo',#xbmc.logDEBUG)
        # Parse parameters
        self.plugin_category = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['plugin_category'][0]
        self.video_list_page_url = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['url'][0]
        self.next_page_possible = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['next_page_possible'][0]

       #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s" % (ADDON, VERSION, DATE, "self.video_list_page_url", str(self.video_list_page_url)),#xbmc.logDEBUG)

        data = scrapertools.cache_page(self.video_list_page_url)
        datos = scrapertools.find_single_match(data,'<div class="destacado-info-resumen">(.*?)</div>')
        datos = scrapertools.htmlclean(datos).strip()
        try:
           #xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s" % (ADDON, VERSION, DATE, "Iniciando reproducción de media_url", str(media_url)),#xbmc.logDEBUG)
            import crtvg_server as servermodule
            video_urls = servermodule.get_video_url(self.video_list_page_url,page_data=data)
            media_url = video_urls[0][1]

            playVideo('',media_url)
            
        except:
            import traceback
            print traceback.format_exc()
            media_url = ""


    def playVideo(self, name, url, liz=None):
        log('playVideo')
        info = getVideoInfo(url,QUALITY,True)
        if info is None: return
        info = info.streams()
        url  = info[0]['xbmc_url']
        liz  = xbmcgui.ListItem(name, path=url)
        if 'subtitles' in info[0]['ytdl_format']: liz.setSubtitles([x['url'] for x in info[0]['ytdl_format']['subtitles'].get('en','') if 'url' in x])
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)



        xbmcplugin.addSortMethod(handle=self.plugin_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE)
        # Finish creating a virtual folder.
        xbmcplugin.endOfDirectory(self.plugin_handle)
        
        


        #listitem.setInfo( "video", { "Title" : title, "FileName" : title, "Plot" : plot } )



