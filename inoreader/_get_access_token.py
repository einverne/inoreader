#!/usr/local/bin/python
# encoding: utf-8
"""
_get_access_token.py
====================
:Summary:
    Get access token for Inoreader and store in settings file

:Author:
    David Young

:Date Created:
    August 24, 2015

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
import yaml
import re
import requests
from docopt import docopt
from dryxPython import logs as dl
from dryxPython import commonutils as dcu
from dryxPython.projectsetup import setup_main_clutil
# from ..__init__ import *


class _get_access_token():

    """
    The worker class for the _get_access_token module

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``settingsFilePath`` -- path to the settings file
    """
    # Initialisation

    def __init__(
            self,
            log,
            settings=False,
            settingsFilePath=False
    ):
        self.log = log
        log.debug("instansiating a new '_get_access_token' object")
        self.settings = settings
        self.settingsFilePath = settingsFilePath
        # xt-self-arg-tmpx

        # Initial Actions

        return None

    # Method Attributes
    def get(self):
        """get the _get_access_token object

        **Return:**
            - ``_get_access_token``
        """
        self.log.info('starting the ``get`` method')

        header = self.check_for_access_token()
        if not header:
            self.request_username_and_password()
            self.request_access_token()
            self.add_access_token_to_settings()
            header = self.check_for_access_token()

        self.log.info('completed the ``get`` method')
        return header

    def request_username_and_password(
            self):
        """request username and password
        """
        self.log.info('starting the ``request_username_and_password`` method')

        self.username = raw_input("Inoreader Username: ")
        import getpass
        self.password = getpass.getpass("Inoreader Password: ")

        self.log.info('completed the ``request_username_and_password`` method')
        return None

    def request_access_token(
            self):
        """request access token
        """
        self.log.info('starting the ``request_access_token`` method')

        # Inoreader Authentication (POST
        # https://www.inoreader.com/accounts/ClientLogin)
        try:
            r = requests.post(
                url="https://www.inoreader.com/accounts/ClientLogin",
                params={
                    "Email": self.username,
                    "Passwd": self.password,
                },
                headers={
                    "AppId": self.settings["inoreader"]["appid"],
                    "AppKey": self.settings["inoreader"]["appkey"],
                    "User-Agent": self.settings["inoreader"]["useragent"],
                },
            )
        except requests.exceptions.RequestException as e:
            print('HTTP Request failed')
            sys.exit(0)

        matchObject = re.search(r"Auth=([a-zA-Z0-9\_]*)", r.content, re.S)
        self.authToken = matchObject.group(1)

        print self.authToken

        self.log.info('completed the ``request_access_token`` method')
        return None

    def add_access_token_to_settings(
            self):
        """add access token to settings
        """
        self.log.info('starting the ``add_access_token_to_settings`` method')

        fileName = self.settingsFilePath
        stream = file(fileName, 'w')
        self.settings["inoreader"]["access_token"] = self.authToken
        yamlContent = self.settings
        yaml.dump(yamlContent, stream,
                  default_flow_style=False, allow_unicode=True)
        stream.close()

        self.log.info('completed the ``add_access_token_to_settings`` method')
        return None

    def check_for_access_token(
            self):
        """check for access token - and that it works
        """
        self.log.info('starting the ``check_for_access_token`` method')

        if "access_token" in self.settings["inoreader"] and self.settings["inoreader"]["access_token"]:

            try:
                r = requests.get(
                    url="https://www.inoreader.com/reader/api/0/stream/contents/user/-/state/com.google/starred",
                    headers={
                        "AppId": self.settings["inoreader"]["appid"],
                        "AppKey": self.settings["inoreader"]["appkey"],
                        "User-Agent": self.settings["inoreader"]["useragent"],
                        "Authorization": "GoogleLogin auth=" + self.settings["inoreader"]["access_token"],
                    },
                )
                if r.status_code != 200:
                    errorCode = r.status_code
                    self.log.error(
                        'cound not connect with this access token (status code %(errorCode)s)' % locals())
                else:
                    headers = {
                        "AppId": self.settings["inoreader"]["appid"],
                        "AppKey": self.settings["inoreader"]["appkey"],
                        "User-Agent": self.settings["inoreader"]["useragent"],
                        "Authorization": "GoogleLogin auth=" + self.settings["inoreader"]["access_token"],
                    }
                    return headers

            except requests.exceptions.RequestException as e:
                print('HTTP Request failed')
                sys.exit(0)

        self.log.info('completed the ``check_for_access_token`` method')
        return None
