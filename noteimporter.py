import os
import codecs
import sys
import datetime
import time
import pytz
import yaml
import subprocess

notes = yaml.load(file(sys.argv[1],'r'))

translate = dict(((ord(a), None) for a in u'''\/:;?*<>|[]=+"',*.?(){}^$!&'''))
local = pytz.tzfile.build_tzinfo("/etc/localtime", file("/etc/localtime"))
utc = pytz.utc

for note in notes:
    for guid, data in note.items():
        content = data['content']
        tags = data['tags']
        title = content.split('\n',1)[0]

        # Get the modification and create dates, note, they're UTC
        modifydate = data['modifydate'].replace(tzinfo=utc)
        createdate = data['createdate'].replace(tzinfo=utc)

        sanitized_title = title.translate(translate)
        print repr(sanitized_title)

        if 'DL' in tags:
            fn=os.path.join('notes', 'DL', sanitized_title + '.txt')
        else:
            fn=os.path.join('notes', sanitized_title + '.txt')

        with codecs.open(fn, 'w', 'utf-8') as file:
            file.write(content)
            if tags:
                print >> file, '\n\nTags: #' + ' #'.join(tags)

        mtime = time.mktime(modifydate.astimezone(local).timetuple())
        os.utime(fn, (mtime, mtime))

        # Creation date is a bit more difficult
        creation_time = createdate.astimezone(local).strftime("%m/%d/%Y %I:%M:%S %p")

        subprocess.check_call(['/usr/bin/SetFile', '-d', creation_time, fn])
