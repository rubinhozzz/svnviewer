# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - SVNViewer

    Shows a specific revision of a file 

    @copyright: 2013 Ruben Sanchez <ruben.flex@gmail.com>,
    @license: GNU GPL, see COPYING for details.
"""
from cStringIO import StringIO
from pysvn import wc_status_kind, opt_revision_kind, wc_notify_action, depth
import pysvn
from MoinMoin import wikiutil
from MoinMoin.parser.highlight import Parser

def macro_SVNViewer(macro, url, file_type='text', revision_number='HEAD', start=None, end=None):
    result = ''
    client = pysvn.Client()
    if is_number(revision_number):
        revision = pysvn.Revision(pysvn.opt_revision_kind.number, int(revision_number))
    else: 
        revision = pysvn.Revision(pysvn.opt_revision_kind.head)
    output = client.cat(url, revision)
    out = StringIO(output)
    lines = out.readlines()
    x, y = clean_range(start, end, len(lines))
    result += u''.join(lines[x-1:y])
    parser = Parser(result, macro.request, format_args=file_type)
    parser.num_start = x
    parser.format(macro.request.formatter)
    del out
    return ''

def clean_range(start, end, limit):
    #cleaning start
    if start is None or is_number(start) == False or int(start) > limit:
        start = 1
    else:
        start = int(start)
    #cleaning end
    if end is None or is_number(end) == False or int(end) > limit or int(end) < start:
        end = limit
    else:
        end = int(end)
    return start, end

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False