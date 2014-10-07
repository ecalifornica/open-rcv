
"""
The rcv command for counting ballots.

"""

import json
import logging
import sys

from openrcv.datagen import create_json_tests
from openrcv import models
from openrcv.models import TestInputFile
from openrcv.scripts.main import main
from openrcv import utils
from openrcv.utils import FileInfo


log = logging.getLogger(__name__)

TEST_INPUT_PATH = "sub/open-rcv-tests/contests.json"


def run_main():
    main(do_rcvgen)

def do_rcvgen(argv):
    count_test_file(argv)


def count_test_file(argv):
    stream_info = utils.JsonFileInfo(TEST_INPUT_PATH)
    with stream_info.open() as f:
        jsobj = json.load(f)
    test_file = TestInputFile.from_jsobj(jsobj)
    log.info("printing TestInputFile")
    print(test_file.to_json())


def make_input_test_file(argv):
    # target_path="sub/open-rcv-tests/contests.json"

    test_file = create_json_tests()
    stream_info = FileInfo("temp.json")
    models.write_json(test_file.to_jsobj(), stream_info)

    with stream_info.open() as f:
        json = f.read()
    print(json)