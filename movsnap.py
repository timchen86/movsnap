#/usr/bin/env python
import subprocess
import pipes
import os
import re
import sys

if len(sys.argv) != 5:
    print "usage: %s sub_file video_file start end" % sys.argv[0]
    sys.exit(1)

# subtitle file
sub_file = sys.argv[1]

# video file
video_file = sys.argv[2]

# 
start = int(sys.argv[3])
end = int(sys.argv[4])

"""
11
00:01:29,530 --> 00:01:32,124
<i>Every weekday, for 12 years...</i>
"""
# grab time offset and text from subtitle file
with open(sub_file, "r") as f:
    sub_content = f.read()
    subs_raw = re.findall("[\d]+[\r]*$\n([\d]+):([\d]+):([\d]+),(\d+)\s+-->\s+[\d:,]+[\r]*$\n(.*?)^[\r\n]*$",sub_content,re.S|re.M)


subs = []
for h, m, s, ms, sub in subs_raw:
    sub = re.sub("<.*?>","",sub)
    t = "%s:%s:%s.%s" % (h, m, s, ms)
    t_x = "%s-%s-%s.%s" % (h, m, s, ms)
    subs.append((t, t_x, sub))

print subs

base_dir = os.path.dirname(video_file)
tmp_dir = os.path.join(base_dir, "movsnap_tmpdir")

try:
    os.makedirs(tmp_dir)
except:
    pass

video_file = pipes.quote(video_file)
for time, time_x, sub in subs[start:end]:
    out_file = os.path.join(tmp_dir, "%s.png" % time_x) 
    out_file = pipes.quote(out_file)

    ffmpeg_exe = "ffmpeg -y -ss %s -i %s -vframes 1 %s" % (time, (video_file), (out_file))
    print ffmpeg_exe

    try:
        subprocess.check_call(ffmpeg_exe, shell=True)
    except:
        pass

    sub_txt = pipes.quote(sub)
    convert_exe = "convert %s -pointsize 70 -gravity south -stroke black -strokewidth 20 -annotate 0 %s -stroke none -fill white -annotate 0 %s %s" % ((out_file), (sub_txt), (sub_txt), (out_file))

    print convert_exe
    try:
        subprocess.check_call(convert_exe, shell=True)
    except:
        pass
