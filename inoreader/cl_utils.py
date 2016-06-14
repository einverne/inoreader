#!/usr/local/bin/python
# encoding: utf-8
"""
*CL-Utils for inoreader*

:Author:
    David Young

:Date Created:
    August 26, 2015

.. todo::
    
    @review: when complete pull all general functions and classes into dryxPython

Usage:
    inoreader sub <feedUrl> [<folder>] [-s <pathToSettingsFile>]
    inoreader [-u|-f] articles <stream> [<maxArticles>] [-s <pathToSettingsFile>]
    inoreader tag add <tagToAdd> <articleId>...
    inoreader tag remove <tagToRemove> <articleId>...

    -h, --help            show this help message
    -v, --version         show version
    -s, --settings        the settings file
    -u, --unread          include unread articles
    -f, --favourite       include starred articles
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
from docopt import docopt
from dryxPython import logs as dl
from dryxPython import commonutils as dcu
from fundamentals import tools, times
from inoreader.add_subscription import add_subscription
from inoreader.get_articles import get_articles
from inoreader.edit_tags import edit_tags

# from ..__init__ import *


def tab_complete(text, state):
    return (glob.glob(text + '*') + [None])[state]


def main(arguments=None):
    """
    *The main function used when ``cl_utils.py`` is run as a single script from the cl, or when installed as a cl command*
    """
    # setup the command-line util settings
    su = tools(
        arguments=arguments,
        docString=__doc__,
        logLevel="WARNING",
        options_first=True,
        projectName="inoreader"
    )
    arguments, settings, log, dbConn = su.setup()

    # tab completion for raw_input
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(tab_complete)

    # unpack remaining cl arguments using `exec` to setup the variable names
    # automatically
    for arg, val in arguments.iteritems():
        if arg[0] == "-":
            varname = arg.replace("-", "") + "Flag"
        else:
            varname = arg.replace("<", "").replace(">", "")
        if isinstance(val, str) or isinstance(val, unicode):
            exec(varname + " = '%s'" % (val,))
        else:
            exec(varname + " = %s" % (val,))
        if arg == "--dbConn":
            dbConn = val
        log.debug('%s = %s' % (varname, val,))

    ## START LOGGING ##
    startTime = times.get_now_sql_datetime()
    log.info(
        '--- STARTING TO RUN THE cl_utils.py AT %s' %
        (startTime,))

    # set options interactively if user requests
    if "interactiveFlag" in locals() and interactiveFlag:

        # load previous settings
        moduleDirectory = os.path.dirname(__file__) + "/resources"
        pathToPickleFile = "%(moduleDirectory)s/previousSettings.p" % locals()
        try:
            with open(pathToPickleFile):
                pass
            previousSettingsExist = True
        except:
            previousSettingsExist = False
        previousSettings = {}
        if previousSettingsExist:
            previousSettings = pickle.load(open(pathToPickleFile, "rb"))

        # x-raw-input
        # x-boolean-raw-input
        # x-raw-input-with-default-value-from-previous-settings

        # save the most recently used requests
        pickleMeObjects = []
        pickleMe = {}
        theseLocals = locals()
        for k in pickleMeObjects:
            pickleMe[k] = theseLocals[k]
        pickle.dump(pickleMe, open(pathToPickleFile, "wb"))

    # call the worker function
    # x-if-settings-or-database-credientials
    if sub:
        rss = add_subscription(
            log,
            settings=settings,
            settingsFilePath=settingsFile,
            rssUrl=feedUrl,
            folder=folder
        )
        rss.get()
    if articles:
        if favouriteFlag:
            unreadOrStarred = "starred"
        elif unreadFlag:
            unreadOrStarred = "unread"
        articles = get_articles(
            log,
            settings=settings,
            settingsFilePath=settingsFile,
            stream=stream,
            maxArticles=maxArticles,
            unreadOrStarred=unreadOrStarred
        )
        articles = articles.get()

        if len(articles) == 0:
            print "No articles found"
        else:
            for article in articles:
                title = article["title"]
                thisId = article["id"]
                print "%(title)s (%(thisId)s)" % locals()

    if tag:
        tag = edit_tags(
            log,
            settings=settings,
            settingsFilePath=settingsFile,
            removeTag=tagToRemove,
            addTag=tagToAdd,
            articleIdList=articleId
        )
        tag.get()

    if "dbConn" in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    ## FINISH LOGGING ##
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' %
             (endTime, runningTime, ))

    return


###################################################################
# CLASSES                                                         #
###################################################################
# xt-class-module-worker-tmpx
# xt-class-tmpx


###################################################################
# PUBLIC FUNCTIONS                                                #
###################################################################
# xt-worker-def

# use the tab-trigger below for new function
# xt-def-with-logger

###################################################################
# PRIVATE (HELPER) FUNCTIONS                                      #
###################################################################

if __name__ == '__main__':
    main()
