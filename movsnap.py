#/usr/bin/env python
import re
import sys
#convert z.jpeg -pointsize 70 -gravity south -stroke '#000C' -strokewidth 2 -annotate 0 'Hello Red\nMist' -stroke  none -fill white -annotate 0 'Hello Red\nMist' 

# snap video to png from subtitle time
if len(sys.argv) != 3:
    print "usage: %s sub_file video_file" % sys.argv[0]
    sys.exit(1)


# subtitle file
sub_file = sys.argv[1]

# video file
video_file = sys.argv[2]

"""
11
00:01:29,530 --> 00:01:32,124
<i>Every weekday, for 12 years...</i>
"""
# grab time offset from subtitle file
with open(sub_file, "r") as f:
    sub_content = f.read()
    #re_sub = re.findall("([\d]+)[\r]*$\n([\d:,]+)\s+-->\s+[\d:,]+[\r]*$\n(.*?)^[\r\n]*$",sub_content,re.S|re.M)
    #re_sub = re.findall("([\d]+)[\r]*$\n([\d]+):([\d]+):([\d]+),\d+\s+-->\s+[\d:,]+[\r]*$\n(.*?)^[\r\n]*$",sub_content,re.S|re.M)
    subs_raw = re.findall("[\d]+[\r]*$\n([\d]+):([\d]+):([\d]+),\d+\s+-->\s+[\d:,]+[\r]*$\n(.*?)^[\r\n]*$",sub_content,re.S|re.M)



subs = []
for h, m, s, sub in subs_raw:
    subs.append((int(h)*3600+int(m)*60+int(s), sub))

print subs


# video to png
# avconv -ss 4000 -i Kick\ Ass\ 2\ \(2013\)/Kick.Ass.2.1080p.5.1.2013.BluRay.mp4  -vframes 1 out.jpeg
# 


