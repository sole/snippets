#!/bin/bash

# Thanks to Martin Los for his guide: http://www.martinlos.com/?p=41

URLS=("http://downloads.sourceforge.net/project/lame/lame/3.99/lame-3.99.3.tar.gz" "http://downloads.sourceforge.net/project/faac/faac-src/faac-1.28/faac-1.28.tar.gz" "http://downloads.sourceforge.net/project/faac/faad2-src/faad2-2.7/faad2-2.7.tar.gz")

for i in "${URLS[@]}"
do
	echo $i
	curl -O -L $i
done

for i in $( ls *.tar.gz ); do
	tar -xzvf $i
done

for i in $( ls -d */); do
	cd $i
	./configure
	make
	sudo make install
	cd ..
done

svn checkout svn://svn.ffmpeg.org/ffmpeg/trunk ffmpeg
cd ffmpeg
./configure --enable-libmp3lame --enable-libfaac --enable-gpl --enable-nonfree --enable-shared --disable-mmx --arch=x86_64 --cpu=core2
make
sudo make install
