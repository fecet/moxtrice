# from tqdm.rich import tqdm_rich
from tqdm import tqdm
from absl import logging
import inspect
from contextlib import contextmanager
from pathlib import Path


class _TqdmLoggingHandler(logging.PythonHandler):
    def __init__(self, tqdm_class=tqdm):
        super(_TqdmLoggingHandler, self).__init__()
        self.tqdm_class = tqdm_class
        # self.stream = logging.logging.getLoggerClass().stream

    def emit(self, record):
        try:
            msg = self.format(record)
            # if self.tqdm_class == tqdm_rich:
            #     self.tqdm_class.write(msg)
            # else:

            self.tqdm_class.write(msg, file=self.stream)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:  # noqa pylint: disable=bare-except
            self.handleError(record)


@contextmanager
def logging_redirect_tqdm(
    tqdm_class=tqdm,
):
    try:
        handlers = [h for h in logging.logging.root.handlers]
        for h in handlers:
            logging.logging.root.removeHandler(h)
        tqdm_handler = _TqdmLoggingHandler(tqdm_class)
        orig_handler = logging.get_absl_handler()
        if orig_handler is not None:
            tqdm_handler.setFormatter(orig_handler._current_handler.formatter)
            tqdm_handler.stream = orig_handler._current_handler.stream

        logging.logging.root.addHandler(tqdm_handler)
        yield
    finally:
        logging.logging.root.removeHandler(tqdm_handler)
        for h in handlers:
            logging.logging.root.addHandler(h)


@contextmanager
def print_redirect_tqdm(tqdm_class=tqdm):
    # Store builtin print
    old_print = print

    def new_print(*args, **kwargs):
        try:
            tqdm_class.write(*args, **kwargs)
        except:
            old_print(*args, **kwargs)

    try:
        inspect.builtins.print = new_print
        yield
    finally:
        inspect.builtins.print = old_print


@contextmanager
def redirect_to_tqdm(tqdm_class=tqdm):
    with logging_redirect_tqdm(tqdm_class) as a, print_redirect_tqdm(tqdm_class) as b:
        yield (a, b)


def _pretty_print(current, parent=None, index=-1, depth=0):
    for i, node in enumerate(current):
        _pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = "\n" + ("\t" * depth)
        else:
            parent[index - 1].tail = "\n" + ("\t" * depth)
        if index == len(parent) - 1:
            current.tail = "\n" + ("\t" * (depth - 1))


def relpath(path_to, path_from):
    path_to = Path(path_to).resolve()
    path_from = Path(path_from).resolve()
    try:
        for p in (*reversed(path_from.parents), path_from):
            head, tail = p, path_to.relative_to(p)
        logging.warn(f"head: {head}, tail: {tail}")
    except Exception as e:  # Stop when the paths diverge.
        logging.exception(e)

    return Path("../" * (len(path_from.parents) - len(head.parents))).joinpath(tail)
