# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - SVNViewer

    Shows a specific revision of a file 

    @copyright: 2013 Ruben Sanchez <ruben.flex@gmail.com>,
    @license: GNU GPL, see COPYING for details.
"""
import StringIO
from pysvn import wc_status_kind, opt_revision_kind, wc_notify_action, depth
import pysvn
from MoinMoin import wikiutil
from MoinMoin.parser.highlight import Parser

def macro_SVNViewer(macro, url, file_type='text', revision_number='HEAD', start=None, end=None):
    client = pysvn.Client()
    try:
        if revision_number.strip().upper() == 'HEAD':
            revno = client.info2(url)[0][1].rev.number
        else:
            revno = int(revision_number)
    except:
        revision = pysvn.Revision(pysvn.opt_revision_kind.head)
    else:
        revision = pysvn.Revision(pysvn.opt_revision_kind.number, revno)
    output = client.cat(url, revision)
    out = StringIO.StringIO(output)
    lines = out.readlines()
    x, y = clean_range(start, end, len(lines))
    result = u''.join(lines[x-1:y])
    parser = Parser(result, macro.request, format_args=file_type)
    parser.num_start = x
    parser.format(macro.request.formatter)
    del out
    return u''

def clean_range(start, end, limit):
    try:
        start = int(start)
    except:
        start = 1
    else:
        if start > limit:
            start = 1

    try:
        end = int(end)
    except:
        end = limit
    else:
        if end > limit or end < start:
            end = limit

    return start, end