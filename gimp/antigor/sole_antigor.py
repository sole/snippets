#!/usr/bin/env python

import math
from gimpfu import *

def sole_antigor(timg, resize, resize_width, resize_height, desaturate):

	if resize:
		image_width = resize_width
		image_height = resize_height
	else:
		image_width = timg.width
		image_height = timg.height
		
	#image = gimp.Image(image_width, image_height, RGB)
	#image.disable_undo()
	
	image = timg.duplicate()
	image.disable_undo()
	
	if resize:
		image.resize(resize_width, resize_height, 0, 0)
	
	disp = gimp.Display(image)
	

register(
	"sole_antigor",
	N_("Make your digital photos look older than they really are"),
	"Make your digital photos look older than they really are",
	"Soledad Penades",
	"Soledad Penades",
	"2011",
	N_("Antigor..."),
	"RGB*",
	[
		(PF_IMAGE, "image", "Input image", None),
		(PF_TOGGLE, "resize", "Resize?", True),
		(PF_SLIDER, "resize_width", "Resize width", 640, (0, 2048, 1)),
		(PF_SLIDER, "resize_height", "Resize height", 480, (0, 2048, 1)),
		(PF_TOGGLE, "desaturate", "Desaturate?", False),
		#(PF_RADIO, "desaturate_method", _("Desaturate by..."), "gif", (("gif", "gif"), ("jpg", "jpg"), ("png", "png"))),
	],
	[],
	sole_antigor,
	menu="<Image>/Filters/Decor/",
	domain=("gimp20-python", gimp.locale_directory)
	)

main()
