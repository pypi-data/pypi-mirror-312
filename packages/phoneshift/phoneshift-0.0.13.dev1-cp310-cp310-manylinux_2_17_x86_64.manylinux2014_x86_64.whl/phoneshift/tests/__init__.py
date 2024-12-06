import unittest

import sys
import os

sys.path.append(os.path.dirname(__file__)+'/../..') # Ensure this package is being tested
import phoneshift.tests.test_nolicense as test_nolicense
import phoneshift.tests.test_license as test_license

def run():
    testSuite = unittest.TestSuite()
    testLoader = unittest.TestLoader()
    testSuite.addTest(testLoader.loadTestsFromModule(test_nolicense))
    testSuite.addTest(testLoader.loadTestsFromModule(test_license))

    testRunner = unittest.runner.TextTestRunner(verbosity=3)
    ret = testRunner.run(testSuite)
    if len(ret.failures)>0:
        exit(1)
