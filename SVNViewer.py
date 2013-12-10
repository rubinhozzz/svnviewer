# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - SVNViewer

    Shows a specific revision of a file 

    @license: GNU GPL, see COPYING for details.
"""
from MoinMoin import wikiutil
from pysvn import wc_status_kind, opt_revision_kind, wc_notify_action, depth
import pysvn
from cStringIO import StringIO
from MoinMoin.parser.highlight import Parser, PygmentsFormatter

def macro_SVNViewer(macro, url, file_type='text', revision_number='HEAD', start=None, end=None):
    result = ''
    client = pysvn.Client()
    if revision_number is None or 'HEAD' in revision_number.upper():
        revision = pysvn.Revision(pysvn.opt_revision_kind.head)
    else:
        revision = pysvn.Revision(pysvn.opt_revision_kind.number, int(revision_number))
    output = client.cat(url, revision)
    out = StringIO(output)
    lines = out.readlines()
    x, y = clean_range(start, end, len(lines))
    chosen_lines = lines[x-1:y]
    for line in chosen_lines:
        result += line
    parser = Parser("<?print 'eeeeeeeeeeeeee';\necho 'dddd';", macro.request, format_args=file_type)
    parser.num_start = x
    parser.format(macro.request.formatter)
    del out
    return ''

def clean_range(start, end, limit):
    default_range = (1, limit)
    if start is None and end is None:
        return default_range
    if start is not None and end is None:
        start = int(start)
        if start >= limit:
            return default_range
        else:
            return (start, limit)
    if start is not None and end is not None:
        start = int(start)
        end = int(end)
        if start > end or start >= limit:
            return default_range
        else:
            return (start, end)
