"""
Basic tool support
"""

from __future__ import annotations

import anyio
import logging  # pylint: disable=wrong-import-position
import sys
from datetime import datetime
from functools import partial
from time import time

import asyncclick as click

from .main import load_subgroup
from .path import P, Path, path_eval
from .times import humandelta, time_until
from .yaml import yprint

log = logging.getLogger()


@load_subgroup(prefix="moat.util")
async def cli():
    """Various utilities"""
    # pylint:disable=unnecessary-pass


@cli.command(name="to")
@click.option("--sleep", "-s", is_flag=True, help="Sleep until that date/time")
@click.option("--human", "-h", is_flag=True, help="Print in numan-readable terms")
@click.option("--now", "-n", is_flag=True, help="Don't advance on match")
@click.option("--inv", "-i", is_flag=True, help="Time until no match")
@click.option("--back", "-b", is_flag=True, help="Time since the last (non)-match")
@click.argument("args", nargs=-1)
async def to_(args, sleep, human, now, inv, back):
    """\
Calculate the time until the start of the next given partial time
specification.

For instance, "moat util to 9 h": shows in how many seconds it's 9 o'clock
(possibly on the next day). Arbitrarily many units can be combined.

Negative numbers count from the end, i.e. "-2 hr" == 10 pm. Don't
forget to use the "--" option-to-argument separator if the time
specification starts with a negative number.

Days are numbered 1…7, Monday…Sunday. "3 dy" is synonymous to "wed",
while "3 wed" means "the third wednesday in a month".

"--human" prints a human-understandable version of the given
time. "--sleep" then delays until the specified moment arrives. If none
of these options is given, the number of seconds is printed.

By default, if the given time spec matches the current time, the
duration to the *next* moment the spec matches is calculated. Use
"--now" to print 0 / "now" / not sleep instead.

"--inv" inverts the time specification, i.e. "9 h" prints the time
until the next moment it is not / again no longer 9:** o'clock,
depending on whether "--now" is used / not used.

"--back" calculates the time *since the end* of the last match /
non-match instead. (If you want the start, use "--inv" and add a
second.)

\b
Known units:
s, sec  Second (0…59)
m, min  Minute (0…59)
h, hr   Hour (0…23)
d, dy   Day-of-week (1…7)
mon…sun Day-in-month (1…5)
w, wk   Week-of-year (0…53)
m, mo   Month (1…12)
y, yr   Year (2023–)
"""
    if not args:
        raise click.UsageError("Up to when please?")
    if back and sleep:
        raise click.UsageError("We don't have time machines.")

    t = datetime.now().astimezone()
    if not now:
        t = time_until(args, t, invert=not inv, back=back)
    t = time_until(args, t, invert=inv, back=back)

    t = t.timestamp()
    tt = int(t - time() + 0.9)
    if back:
        tt = -tt
    if human:
        print(humandelta(tt))
    if sleep:
        await anyio.sleep(tt)
    elif not human:
        print(tt)


@cli.command
@click.option("-d", "--dec", "--decode", type=str, help="Source format", default="json")
@click.option("-e", "--enc", "--encode", type=str, help="Destination format", default="yaml")
@click.option(
    "-i", "--in", "--input", "pathi", type=click.File("r"), help="Source file", default=sys.stdin
)
@click.option(
    "-o",
    "--out",
    "--output",
    "patho",
    type=click.File("w"),
    help="Destination file",
    default=sys.stdout,
)
@click.option("-s", "--stream", is_flag=True, help="Multiple messages")
def convert(enc, dec, pathi, patho, stream):
    """File conversion utility.

    Supported file formats: json yaml cbor msgpack python
    """

    def get_codec(n):
        if n == "python":
            from pprint import pformat

            return eval, pformat, False, False
        if n == "json":
            import simplejson as json

            if stream:

                def jdump(d):
                    return json.dumps(d, separators=(",", ":")) + "\n"

            else:

                def jdump(d):
                    return json.dumps(d, indent="  ") + "\n"

            return json.loads, jdump, False, False
        if n == "yaml":
            import ruyaml as yaml

            y = yaml.YAML(typ="safe")
            y.default_flow_style = True, False
            from moat.util import yload

            def ypr(d, s):
                yprint(d, s)
                s.write("---\n")

            return (
                partial(yload, multi=True) if stream else yload,
                ypr if stream else yprint,
                False,
                True,
            )
        if n == "cbor":
            from moat.util.cbor import StdCBOR

            c = StdCBOR()
            d = StdCBOR()
            return c.feed if stream else c.decode, d.encode, True, False
        if n == "msgpack":
            from moat.util.msgpack import StdMsgpack

            c = StdMsgpack()
            d = StdMsgpack()
            return c.feed if stream else c.decode, d.encode, True, False
        raise ValueError("unsupported codec")

    dec, _x, bd, csd = get_codec(dec)
    _y, enc, be, cse = get_codec(enc)
    if bd:
        pathi = pathi.buffer
    if be:
        patho = patho.buffer

    if stream:
        if csd:

            def in_d():
                return [pathi.read()]

        else:

            def in_d():
                while data := pathi.read(4096):
                    yield data

        for d in in_d():
            for data in dec(d):
                if cse:
                    enc(data, patho)
                else:
                    dat = enc(data)
                    patho.write(dat)
    else:
        if csd:
            data = dec(pathi)
        else:
            data = pathi.read()
            data = dec(data)
        if cse:
            enc(data, patho)
        else:
            data = enc(data)
            patho.write(data)
    pathi.close()
    patho.close()


@cli.command("path", help=Path.__doc__, no_args_is_help=True)
@click.option(
    "-e",
    "--encode",
    is_flag=True,
    help="evaluate a Python expr and encode to a pathstr",
)
@click.option("-d", "--decode", is_flag=True, help="decode a path to a list")
@click.argument("path", nargs=-1)
async def path_(encode, decode, path):
    """Explain/test MoaT paths"""
    if not encode and not decode:
        raise click.UsageError("Need -e or -d option.")
    elif not decode:
        try:
            path = path_eval(" ".join(path))
        except Exception as exc:  # pylint:disable=broad-exception-caught
            print(repr(exc), file=sys.stderr)
        if not isinstance(path, (list, tuple)):
            path = path[0]
        print(Path(*path))
    elif encode:
        raise click.UsageError("encode and decode at the same time??")
    else:
        for p in path:
            print(repr(list(P(p))))


@cli.command("cfg", help="Retrieve+show a config value", no_args_is_help=True)
@click.pass_obj
@click.option("-y", "--yaml", is_flag=True, help="print as YAML")
@click.option("-e", "--empty", is_flag=True, help="empty string if the key doesn't exist")
@click.argument("path", nargs=-1, type=P)
async def cfg_(obj, path, yaml, empty):
    """Emit the current configuration as a YAML file.

    You can limit the output by path elements.
    E.g., "cfg kv.connect.host" will print "localhost".

    Single values are printed with a trailing line feed.

    Dump the whole config with "moat util cfg :".
    """
    from .exc import ungroup

    delim = False
    for p in path:
        if delim and yaml:
            print("---", file=obj.stdout)
        with ungroup():
            try:
                v = obj.cfg._get(p)  # noqa:SLF001
            except KeyError:
                if not empty:
                    print("Unknown:", p, file=sys.stderr)
                    sys.exit(1)
            else:
                if yaml:
                    yprint(v, obj.stdout)
                else:
                    print(v, file=obj.stdout)
        delim = True
