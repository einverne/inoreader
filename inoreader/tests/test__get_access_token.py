import os
import nose
import shutil
import yaml
from inoreader import _get_access_token
from inoreader.utKit import utKit

# load settings
stream = file("/Users/Dave/git_repos/inoreader/example_settings.yaml", 'r')
settings = yaml.load(stream)
stream.close()


# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

# xnose-class-to-test-main-command-line-function-of-module


class test__get_access_token():

    def test__get_access_token_function(self):
        kwargs = {}
        kwargs["log"] = log
        kwargs["settings"] = settings
        kwargs[
            "settingsFilePath"] = "/Users/Dave/git_repos/inoreader/example_settings.yaml"
        testObject = _get_access_token(**kwargs)
        testObject.get()

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
