#!/usr/local/bin/python
# encoding: utf-8
"""
get_articles.py
===================
:Summary:
    Add subscription to inoread

:Author:
    David Young

:Date Created:
    August 26, 2015

:dryx syntax:
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this script/module please email me: d.r.young@qub.ac.uk

:Tasks:
    @review: when complete pull all general functions and classes into dryxPython

# xdocopt-usage-tempx
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
import re
import requests
from docopt import docopt
from dryxPython import logs as dl
from dryxPython import commonutils as dcu
from dryxPython.projectsetup import setup_main_clutil
from inoreader._get_access_token import _get_access_token
# from ..__init__ import *


###################################################################


class get_articles():

    """
    The worker class for the get_articles module

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``settingsFilePath`` -- path to the settings file
        - ``stream`` -- return article of stream
        - ``maxArticles`` -- maximum number of articles to return (False = All)
        - ``unreadOrStarred`` -- return only unread or starred

    **Todo**
        - @review: when complete, clean get_articles class
        - @review: when complete add logging
        - @review: when complete, decide whether to abstract class to another module
    """
    # Initialisation
    # 1. @flagged: what are the unique attrributes for each object? Add them
    # to __init__

    def __init__(
            self,
            log,
            settings=False,
            settingsFilePath=False,
            stream=False,
            maxArticles=False,
            unreadOrStarred=False
    ):
        self.log = log
        log.debug("instansiating a new 'get_articles' object")
        self.settings = settings
        self.settingsFilePath = settingsFilePath
        self.maxArticles = maxArticles
        self.unreadOrStarred = unreadOrStarred
        self.stream = stream

        if self.maxArticles == False or self.maxArticles == None:
            self.maxArticles = 1000

        # xt-self-arg-tmpx

        # Initial Actions
        header = _get_access_token(
            log=self.log,
            settings=self.settings,
            settingsFilePath=self.settingsFilePath
        )
        self.header = header.get()

        if self.stream in ["read", "broadcast", "like", "starred"]:
            self.stream = "user/-/state/com.google/" + self.stream
        else:
            self.stream = "user/-/label/" + self.stream
        self.url = "https://www.inoreader.com/reader/api/0/stream/contents/" + \
            self.stream

        return None

    # Method Attributes
    def get(self):
        """get the get_articles object

        **Return:**
            - ``get_articles``

        **Todo**
            - @review: when complete, clean get method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get`` method')

        regex = re.compile(r'(user/\d*?/label/|user/\d*?/state/com.google/)')

        import json

        self.setup_parameters()

        try:
            r = requests.get(
                url=self.url,
                params=self.params,
                headers=self.header,
            )
            if r.status_code != 200:
                print('Response HTTP Status Code   : {status_code}'.format(
                    status_code=r.status_code))
            if len(r.content) != 0:
                thisUrl = r.url
                # print """URL: %(thisUrl)s""" % locals()
                articles = r.json()
            else:
                print "No articles found at this URL: " + r.url
                return []
            if len(articles["items"]) == 0:
                print "No articles found at this URL: " + r.url
                return []
            # print articles
        except requests.exceptions.RequestException as e:
            print('HTTP Request failed')

        if articles:
            articleList = []
            for item in articles["items"]:
                thisArticle = {}
                thisArticle["origin-title"] = item["origin"]["title"]
                thisArticle["origin-url"] = item["origin"]["htmlUrl"]
                thisArticle["author"] = item["author"]
                thisArticle["title"] = item["title"]
                try:
                    thisArticle["alternate-url"] = item["alternate"][0]["href"]
                except:
                    thisArticle["alternate-url"] = None
                try:
                    thisArticle["enclosure-url"] = item["enclosure"][0]["href"]
                except:
                    thisArticle["enclosure-url"] = None
                try:
                    thisArticle[
                        "enclosure-type"] = item["enclosure"][0]["type"]
                except:
                    thisArticle["enclosure-type"] = None
                thisArticle["summary"] = item["summary"][
                    "content"].encode("utf-8", "ignore")
                thisArticle["id"] = item["id"].split("/")[-1]
                thisArticle["labels"] = item["categories"]
                thisArticle["url"] = item["canonical"][0]["href"]

                tags = []
                statusTags = []
                for label in thisArticle["labels"]:
                    if "/com.google/" in label:
                        label = regex.sub("", label)
                        statusTags.append(label)
                    else:
                        label = regex.sub("", label)
                        tags.append(label)
                thisArticle["tags"] = tags
                thisArticle["statusTags"] = statusTags
                articleList.append(thisArticle)

        self.log.info('completed the ``get`` method')
        return articleList

    def setup_parameters(
            self):
        """setup parameters

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean setup_parameters method
            - @review: when complete add logging
        """
        self.log.info('starting the ``setup_parameters`` method')

        self.params = {}
        excludes = []
        includes = []

        # SET MAX ARTICLES
        if hasattr(self, 'maxArticles'):
            if int(self.maxArticles) > 1000:
                self.params["n"] = 1000
            else:
                self.params["n"] = self.maxArticles

        else:
            print self.maxArticles

        # STARRED
        if self.unreadOrStarred:
            if self.unreadOrStarred == "starred":
                includes.append("user/-/state/com.google/starred")
            elif self.unreadOrStarred == "unread":
                excludes.append("user/-/state/com.google/read")

        self.params["xt"] = excludes
        self.params["it"] = includes

        self.log.info('completed the ``setup_parameters`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method


if __name__ == '__main__':
    main()
