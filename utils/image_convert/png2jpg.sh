#!/bin/bash
# Converts to jpg all png images in the current directory
# requires ImageMagick
mogrify -format jpg *.png
