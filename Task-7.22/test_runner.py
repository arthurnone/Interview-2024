"""
Python script for running unit tests with coverage reporting.

This script uses the 'unittest' framework to discover and run all test cases
from the 'tests' directory that match the pattern 'test_*.py'. It utilizes the
'coverage' module to generate coverage reports in both text and HTML formats.

Developer: WangPeifeng
Date: 2024-05-29
"""

import unittest  
import coverage 

cov = coverage.Coverage()  # Create a Coverage object
cov.start()  

# Discover and load all test cases from the 'tests' directory that match the pattern 'test_*.py'
test_suite = unittest.defaultTestLoader.discover('tests', pattern='test_*.py')

# Create a TextTestRunner object for running the test suite and writing the result to 'test_report.log'
runner = unittest.TextTestRunner(stream=open('test_report.log', 'w'), verbosity=2)

# Run the test suite using the runner
result = runner.run(test_suite)

cov.stop()  
cov.report()  # Generate a coverage report
cov.html_report(directory='coverage_report')  # Generate an HTML coverage report in the 'coverage_report' directory
cov.report(show_missing=True)  # Show lines of code that were not covered in the coverage report
