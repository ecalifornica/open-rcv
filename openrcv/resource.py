
"""
Helper functions to support using iterator resources.

An "iterator resource" is a callable that returns a with-statement context
manager [1], which in turn yields an iterator object for the target `as`
expression.  Here is an example of using an iterator resource `resource`:

    with resource() as items:
        for item in items:
            # Do stuff.
            ...

Unsurprisingly, the above resembles the pattern of opening a file and
reading its lines.

Iterator resources are a central concept in this package.  For example,
for many of our APIs, we pass ballots around as an iterator resource
rather than as a plain iterable.  This lets us access large sets of
ballots as a file rather having to store them in memory.  By using an
iterator resource, we can open and close a ballot file in our
implementations when needed (e.g. using the convenient with statement),
as opposed to having to open a file much earlier than needed, and passing
open file objects into our APIs.

This module provides helper functions for using iterator resources
and for building new iterator resources from existing ones.


[1]: https://docs.python.org/3/library/contextlib.html

"""

# TODO: add a helper class/function for "post-composing".
# TODO: convert StreamInfos to the iterator resource pattern?

from contextlib import contextmanager


@contextmanager
def tracking(iterable, label=None):
    """
    Return a with-statement context manager for an iterable that provides
    item-level information when an exception occurs.

    The context manager yields an iterator object for the target `as`
    expression that we call a "tracked iterator."
    """
    if label is None:
        label = 'item'
    tracker = _IteratorTracker()
    try:
        iterator = tracker.make_iterator(iterable)
        yield iterator
    except Exception as exc:
        # TODO: find a way of including additional information in the stack
        # trace that doesn't involve raising a new exception (and unnecessarily
        # lengthening the stack trace display).
        raise type(exc)("during %s number %d: %r" % (label, tracker.item_number, tracker.item))


class _IteratorTracker(object):

    """
    Records progress of an iterator.
    """

    def __init__(self):
        self.item_number = 0
        self.item = None

    def make_iterator(self, iterable):
        """
        Return a new iterator object yielding the same items.

        We call the return value a "tracked iterator."
        """
        for item_number, item in enumerate(iterable, start=1):
            self.item = item
            self.item_number = item_number
            yield item


def iter_resource(iterable):
    """Wrap an iterable in an iterator resource."""
    return _IterableResource(iterable)


class _IterableResource(object):

    """A class for exposing an iterable as an iterator resource."""

    def __init__(self, iterable):
        self.iterable = iterable

    @contextmanager
    def __call__(self):
        yield self.iterable


def pipe_resource(resource, pipe_func):
    """
    Pipe a resource's iterator object through a function.

    Create an iterator resource that passes the iterator object from the
    given iterator resource through the given pipe function.

    Arguments:
      pip_func: a function that accepts an iterable and returns an
        iterator object.
      resource: an iterator resource.
    """
    return _PipedResource(resource, pipe_func)


class _PipedResource(object):

    """
    An iterator resource in which the target iterable is passed to a pipe
    function (i.e. as a post-process).
    """

    def __init__(self, resource, pipe_func):
        """
        Arguments:
          pip_func: a function that accepts an iterable and returns an
            iterator object.
          resource: an iterator resource.
        """
        self.pipe_func = pipe_func
        self.resource = resource

    @contextmanager
    def __call__(self):
        with self.resource() as items:
            yield self.pipe_func(items)
