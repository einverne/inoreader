#!/usr/local/bin/python
# encoding: utf-8
"""
*Add subscription to inoread*

:Author:
    David Young

:Date Created:
    August 26, 2015

.. todo::
    
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
import requests
from docopt import docopt
from dryxPython import logs as dl
from dryxPython import commonutils as dcu
from fundamentals import tools, times
from inoreader._get_access_token import _get_access_token
# from ..__init__ import *


###################################################################


class edit_tags():

    """
    *The worker class for the edit_tags module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``settingsFilePath`` -- path to the settings file
        - ``removeTag`` -- tag to remove (can also be star, like, broadcast or read)
        - ``addTag`` -- tag to add (can also be star, like, broadcast or read)
        - ``articleIdList`` -- list of article ids


    .. todo::

        - @review: when complete, clean edit_tags class
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
            removeTag=False,
            addTag=False,
            articleIdList=[]
    ):
        self.log = log
        log.debug("instansiating a new 'edit_tags' object")
        self.settings = settings
        self.settingsFilePath = settingsFilePath
        self.removeTag = removeTag
        self.articleIdList = articleIdList
        self.addTag = addTag
        # xt-self-arg-tmpx

        # 2. @flagged: what are the default attrributes each object could have? Add them to variable attribute set here
        # Variable Data Atrributes

        # 3. @flagged: what variable attrributes need overriden in any baseclass(es) used
        # Override Variable Data Atrributes

        # Initial Actions
        header = _get_access_token(
            log=self.log,
            settings=self.settings,
            settingsFilePath=self.settingsFilePath
        )
        self.header = header.get()
        self.url = "https://www.inoreader.com/reader/api/0/edit-tag"

        return None

    def close(self):
        del self
        return None

    # 4. @flagged: what actions does each object have to be able to perform? Add them here
    # Method Attributes
    def get(self):
        """
        *get the edit_tags object*

        **Return:**
            - ``edit_tags``

        .. todo::

            - @review: when complete, clean get method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get`` method')

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
            else:
                if self.addTag:
                    tag = self.addTag
                    print "tag `%(tag)s` added" % locals()
                if self.removeTag:
                    tag = self.removeTag
                    print "tag `%(tag)s` removed" % locals()

        except requests.exceptions.RequestException as e:
            print('HTTP Request failed')

        self.log.info('completed the ``get`` method')
        return edit_tags

    def setup_parameters(
            self):
        """
        *setup paramms*

        **Key Arguments:**
            # -

        **Return:**
            - None

        .. todo::

            - @review: when complete, clean setup_parameters method
            - @review: when complete add logging
        """
        self.log.info('starting the ``setup_parameters`` method')

        self.params = {}

        if self.addTag:
            if self.addTag in ["starred", "like", "read", "broadcast"]:
                addTag = "user/-/state/com.google/" + self.addTag
            else:
                addTag = "user/-/label/" + self.addTag
            self.params["a"] = addTag

        if self.removeTag:
            if self.removeTag in ["starred", "like", "read", "broadcast"]:
                removeTag = "user/-/state/com.google/" + self.removeTag
            else:
                removeTag = "user/-/label/" + self.removeTag
            self.params["r"] = removeTag

        if isinstance(self.articleIdList, int) or isinstance(self.articleIdList, str) or isinstance(self.articleIdList, unicode):
            self.articleIdList = [self.articleIdList]
        self.params["i"] = self.articleIdList

        self.log.info('completed the ``setup_parameters`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method


if __name__ == '__main__':
    main()
