#!/bin/bash
#
# A script for screencasting in Ubuntu - capturing both the X11 display and PulseAudio output
# based on the script found here http://www.ja-sig.org/wiki/display/JSG/Screencasting+In+Ubuntu
# (hence the '2' in the filename)
#
# This version encodes using theora/libvorbis for video and audio. We get an .ogv as output.
#

# list of programs we depend on
progs="xdpyinfo grep head sed ffmpeg pacat parec sox"

# check for programs we depend on
result=0
for prog in $progs
do
  type -p $prog > /dev/null
  if (( $? != 0 )); then
    echo "Error: Cannot find required program '$prog'"
    result=1
  fi
done
if (( $result != 0 )); then
  exit 1
fi

screenSize="640x480" # default if we cant detect it
screenOffset="0,0" # default to top-left corner
frameRate="24" # default frame rate
baseName="capture" # default base filename for capture

# attempt to detect the dimension of the screen for the default
dimensions=`xdpyinfo | grep 'dimensions:' | head -1 | \
  sed -e 's/^.* \([0-9]\+x[0-9]\+\) pixels.*$/\1/'`
if [[ "$dimensions" =~ [0-9]+x[0-9]+ ]]; then
  screenSize=$dimensions
fi

# collect command line settings
while getopts 'hs:o:t:p' param ; do
  case $param in
    s)
      screenSize="$OPTARG"
      ;;
    o)
      screenOffset="$OPTARG"
      ;;
    t)
      timeToRecord="$OPTARG"
      ;;
    *)
      echo ""
      echo "$0 - records screencast"
      echo ""
      echo "$0 [options] [base-filename]"
      echo ""
      echo "options:"
      echo "	-h            show brief help"
      echo "	-s <size>     screensize to record as <width>x<height>"
      echo "	-o <offset>   offset off recording area as <xoffset>,<yoffset>"
      echo "	-t <time>     time to record (in seconds)"
      echo ""
      exit 0
      ;;
  esac
done

shift $(( $OPTIND - 1 ))

# determine basename of files
if [ -n "$1" ] ; then
  baseName="$1"
fi

echo ""
echo "Size = $screenSize"
echo "Offset = $screenOffset"
echo "Rate = $frameRate"
echo "Filename = $baseName"

# get ready to start recording
echo ""
if [ -n "$timeToRecord" ]; then
  echo "Preparing to capture for $timeToRecord seconds."
else
  echo "Preparing to capture."
  echo "Press ENTER when finished capturing."
fi
sleep 3
echo ""

# start playing silence to make sure there is always audio flowing
pacat /dev/zero &
pidSilence=$!

# starts recording video using x11grab to make an ogv video
ffmpeg -y -an  \
  -s "$screenSize" -r "$frameRate" -f x11grab -i :0.0+"$screenOffset" \
  -s "$screenSize" -r "$frameRate" -vcodec libtheora -qscale 25 \
  "$baseName.temp.ogv" &
pidVideo=$!

# starts recording raw audio
parec --format=s16le --rate=44100 --channels=2 $baseName.raw &
pidAudio=$!

echo ""
echo "Video recording started with process ID $pidVideo"
echo "Audio recording started with process ID $pidAudio"
echo ""

# wait for recording to be done, either by timer or user hitting enter
if [ -n "$timeToRecord" ]; then
  sleep "$timeToRecord"
else
  read nothing
fi

# stop recordings
echo ""
echo "Terminating recordings ..."
kill -15 $pidVideo $pidAudio 
kill -15 $pidSilence
wait

# filter and normalize the audio
echo "" 
echo "Filtering and normalizing sound ..." 
sox --norm -s -b 16 -L -r 44100 -c 2 "$baseName.raw" "$baseName.wav"  highpass 65 lowpass 12k

outputFile="$baseName.ogv"

# encode video and audio into final ogv file
echo "" 
echo "Encoding to final ogv ..." 

ffmpeg -i "$baseName.wav" -i "$baseName.temp.ogv" -qscale 25 -acodec libvorbis -ab 128k -ac 2 -ar 44100 -vcodec copy "$outputFile"


echo ""
echo "DONE! Final media written in file $outputFile"

echo ""
exit 0

