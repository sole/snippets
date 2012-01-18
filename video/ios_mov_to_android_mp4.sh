WIDTH="720"
HEIGHT="480"
BITRATE="1500k"
for i in $(ls *.mov); do
	ffmpeg -i $i -r 30 -vcodec mpeg4 -acodec libfaac -ac 1 -ar 44100 -vf scale=$WIDTH:$HEIGHT -b $BITRATE  -y $i.mp4
done
for i in *.mov.mp4; do j=`echo $i | sed 's/.mov.mp4/.mp4/'`; mv "$i" "$j"; done