# -*- coding: utf-8 -*-

import logger
import xbmcaddon
import re
import urllib2
import xbmcgui
import xbmcplugin
import sys
import urllib
     
def getSetting(settingName):
    setting=xbmcaddon.Addon().getSetting(settingName)
        
    return setting

def getUrl(url):
    #logger.debug(url)

    f=urllib2.urlopen(url)
    data=f.read()
    f.close()

    return data

def findall(pattern, searText, flags):
    #logger.debug("findall - pattern: {0}".format(pattern))

    try:

        return re.findall(pattern, searText,flags)

    except Exception as e:
        logger.debug(str(e))
        return None

def addItemMenu(label, thumbnail, url, IsPlayable = 'false', isFolder= True):

    handle = int(sys.argv[1])

    logger.debug("addItemMenu - label:{0}, thumbnail: {1}, url: {2}, IsPlayable: {3}, isFolder: {4}".format(label,thumbnail,url,IsPlayable,isFolder))

    li= xbmcgui.ListItem(label=label, thumbnailImage=thumbnail)
    li.setProperty('IsPlayable', IsPlayable)

    xbmcplugin.addDirectoryItem(handle, listitem = li, url = url, isFolder = isFolder)

def build_url(query):

    base_url = sys.argv[0]

    return base_url + '?' + urllib.urlencode(query)

