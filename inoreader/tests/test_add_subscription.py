import os
import nose
import shutil
import yaml
from inoreader import add_subscription
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


class test_add_subscription():

    def test_add_subscription_function(self):
        kwargs = {}
        kwargs["log"] = log
        kwargs["settings"] = settings
        kwargs[
            "settingsFilePath"] = "/Users/Dave/git_repos/inoreader/example_settings.yaml"
        kwargs[
            "rssUrl"] = "https://github.com/esheldon/esutil/commits/master.atom"
        kwargs["folder"] = "github-updates"
        # xt-kwarg_key_and_value

        testObject = add_subscription(**kwargs)
        testObject.get()

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
