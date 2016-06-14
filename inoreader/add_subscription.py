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
from _get_access_token import _get_access_token


###################################################################


class add_subscription():

    """
    *The worker class for the add_subscription module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``settingsFilePath`` -- path to the settings file
        - ``rssUrl`` -- rssUrl
        - ``folder`` -- folder to add the rss feed to


    .. todo::

        - @review: when complete, clean add_subscription class
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
            rssUrl="",
            folder=False
    ):
        self.log = log
        log.debug("instansiating a new 'add_subscription' object")
        self.settings = settings
        self.rssUrl = rssUrl
        self.settingsFilePath = settingsFilePath
        if folder:
            self.folder = "user/-/label/%(folder)s" % locals()
        else:
            self.folder = folder
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
        self.quickaddUrl = "https://www.inoreader.com/reader/api/0/subscription/quickadd"
        self.subscribeUrl = "https://www.inoreader.com/reader/api/0/subscription/edit"

        return None

    def close(self):
        del self
        return None

    # 4. @flagged: what actions does each object have to be able to perform? Add them here
    # Method Attributes
    def get(self):
        """
        *get the add_subscription object*

        **Return:**
            - ``add_subscription``

        .. todo::

            - @review: when complete, clean get method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get`` method')

        params = {}
        params["s"] = self.rssUrl
        params["ac"] = "subscribe"
        if self.folder:
            params["a"] = self.folder

        try:
            r = requests.get(
                url=self.subscribeUrl,
                params=params,
                headers=self.header,
            )
            print('Response HTTP Status Code   : {status_code}'.format(
                status_code=r.status_code))
            print(
                'Response HTTP Response Body : {content}'.format(content=r.content))
        except requests.exceptions.RequestException as e:
            print('HTTP Request failed')

        self.log.info('completed the ``get`` method')
        return add_subscription
    # xt-class-method


if __name__ == '__main__':
    main()
