OpenRCV
=======

[![Build Status](https://travis-ci.org/cjerdonek/open-rcv.svg?branch=master)](https://travis-ci.org/cjerdonek/open-rcv)

OpenRCV is an open source software project for tallying ranked-choice
voting elections like instant runoff voting and the single transferable vote.

It is distributed on [PyPI][openrcv-pypi] and licensed under a permissive
open source license.  See the [License](#license) section for details
on the license.

**Note: this software is not yet usable.**


Requirements
------------

OpenRCV requires Python 3.4.  If you do not already have Python 3.4
installed, you can download it [from here][python-download].


Installing
----------

    $ pip install openrcv


Running It
----------

    $ rcvcount ELECTION.blt


Testing It
----------

    $ rcvtest


Contributing
------------

To contribute to the project, see the [Contributing][openrcv-contribute]
page.


License
-------

This project is licensed under the permissive MIT license.
See the [`LICENSE`](LICENSE) file for the actual license wording.


Author
------

Chris Jerdonek (<chris.jerdonek@gmail.com>)


[openrcv-contribute]: docs/contributing.md
[openrcv-pypi]: https://pypi.python.org/pypi/OpenRCV
[python-download]: https://www.python.org/downloads/
