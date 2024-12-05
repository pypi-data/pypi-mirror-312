"""
Gitlab-Docs entrypoint to auto generate gitlab-ci documentation from yml configuration files
Author: Charlie Smith
"""

## Import Thirdparty Libraries
import logging
import os

# from datetime import datetime
# from datetime import timedelta
# from distutils.util import strtobool
# import time
import gitlab_docs.includes as includes
import gitlab_docs.jobs as jobs
import gitlab_docs.reset_docs as md_writer
import gitlab_docs.variables as variables
import gitlab_docs.workflows as workflows

# flake8: noqa: E501
# Logging Setup
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GITLAB DOCS")
logger.setLevel(LOG_LEVEL)
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "GITLAB-DOCS.md")
ENABLE_WORKFLOW_DOCUMENTATION = os.getenv("ENABLE_WORKFLOW_DOCUMENTATION", False)
def main():
    print("Welcome to Gitlab Docs")
    # resets markdown output file and adds GITLAB DOCS opening marker
    GLDOCS_CONFIG_FILE = os.getenv("GLDOCS_CONFIG_FILE", ".gitlab-ci.yml")
    try:
        sudoku = open(GLDOCS_CONFIG_FILE, 'r').readlines()
    except FileNotFoundError:
        print("Gitlab Configuration " + GLDOCS_CONFIG_FILE + " doesn't exist")
        return 0
    else:
        # md_writer.gitlab_docs_reset_writer(OUTPUT_FILE=OUTPUT_FILE, MODE="STARTING")
        variables.document_variables(GLDOCS_CONFIG_FILE=GLDOCS_CONFIG_FILE, WRITE_MODE="w",DISABLE_TITLE=False,OUTPUT_FILE=OUTPUT_FILE)
        includes.document_includes(GLDOCS_CONFIG_FILE=GLDOCS_CONFIG_FILE, WRITE_MODE="w",DISABLE_TITLE=False, DISABLE_TYPE_HEADING=False,OUTPUT_FILE=OUTPUT_FILE)
        if ENABLE_WORKFLOW_DOCUMENTATION != False:
            workflows.document_workflows(GLDOCS_CONFIG_FILE=GLDOCS_CONFIG_FILE, WRITE_MODE="w",DISABLE_TITLE=True,OUTPUT_FILE=OUTPUT_FILE)
        jobs.get_jobs(GLDOCS_CONFIG_FILE=GLDOCS_CONFIG_FILE, WRITE_MODE="w", DISABLE_TITLE=False, DISABLE_TYPE_HEADING=False,OUTPUT_FILE=OUTPUT_FILE)

        # resets markdown output file and adds GITLAB DOCS closing marker
        md_writer.gitlab_docs_reset_writer(OUTPUT_FILE=OUTPUT_FILE, MODE="CLOSING")
