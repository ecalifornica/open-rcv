
"""
The rcv command for counting ballots.

"""

import logging
import os
from textwrap import dedent
import sys

import yaml

from openrcv import counting
from openrcv.datagen import (random_contest, BallotGenerator,
                             UniqueBallotGenerator)
from openrcv.formats.blt import BLTOutputFormat
from openrcv.jsmodels import JsonTestCaseOutput
from openrcv.models import BallotStreamResource, ContestInput
from openrcv.parsing import parse_internal_ballot
from openrcv.utils import logged_open, PathInfo, PermanentFileInfo, StringInfo


log = logging.getLogger(__name__)


# TODO: unit-test this.
def count(ns, stdout=None):
    input_path = ns.input_path
    with logged_open(input_path) as f:
        config = yaml.load(f)
    # TODO: use a common pattern for accessing config values.
    base_dir = os.path.dirname(input_path)
    config = config['openrcv']
    contests = config['contests']
    contest = contests[0]
    blt_path = os.path.join(base_dir, contest['file'])
    results = counting.count_irv(blt_path)
    json_results = JsonTestCaseOutput.from_contest_results(results)
    print(json_results.to_json())


def rand_contest(ns, stdout=None):
    if stdout is None:
        stdout = sys.stdout
    output_dir = ns.output_dir
    writer_class = ns.output_format

    contest = ContestInput()
    contest.candidates = ['A', 'B', 'C']
    contest.seat_count = 1
    ballot_stream_info = StringInfo(dedent("""\
    2 1 1
    3 5 1
    """))
    ballots_resource = BallotStreamResource(ballot_stream_info, parse=parse_internal_ballot)
    # with ballots_resource() as ballots:
    #     print(repr(list(ballots)))
    # return
    contest.ballots_resource = ballots_resource
    print(repr(contest))

    writer = writer_class(output_dir=output_dir, stdout=stdout)
    output_paths = writer.write_contest(contest)
    return "\n".join(output_paths) + "\n" if output_paths else None

    choices = list(range(ns.candidates))
    generator = NonUniqueBallotGenerator()
    print(repr(generator.generate(choices)))
    generator = UniqueBallotGenerator()
    print(repr(generator.generate(choices)))
    #print(contest)
