#!/usr/bin/env python

import math
from gimpfu import *

def sole_generate_bitmap_font(timg, tdrawable, font, font_size, orientation):
	char_begin = 32
	char_end = 127
	num_chars = char_end - char_begin
	
	if orientation == "horizontal":
		height = font_size
		width = font_size * num_chars
	else:
		width = font_size
		height = font_size * num_chars
	
	image = gimp.Image(width, height, RGB)
	image.disable_undo()
	
	gimp.set_foreground(255, 255, 255)
	gimp.set_background(0, 0, 0)
	
	background_layer = gimp.Layer(image, "Background", width, height, RGB_IMAGE, 100, NORMAL_MODE)
	image.add_layer(background_layer, 0)
	pdb.gimp_edit_fill(background_layer, BACKGROUND_FILL)
	
	disp = gimp.Display(image)
	
	for i in range(char_begin, char_end):
		string = '%c' % i
		offset = i - char_begin
		
		if orientation == "vertical":
			x_pos = 0
			y_pos = offset * font_size
		else:
			x_pos = offset * font_size
			y_pos = 0
		
		text_layer = pdb.gimp_text_fontname(image, None, x_pos, y_pos, string, -1, False, font_size, PIXELS, font)
		
		gimp.progress_update(float(offset) / float(num_chars))
	
	pdb.gimp_image_flatten(image)
	
	
	image.enable_undo()

register(
	"sole_generate_bitmap_font",
	"Generate bitmap font",
	"Generate bitmap font",
	"Soledad Penades",
	"Soledad Penades",
	"2009",
	"<Image>/File/Create/_Generate Bitmap Font",
	"",
	[
		(PF_FONT, "Font", "Font", "04b03"),
		(PF_SPINNER, "Font_Size", "Size", 8, (0, 1000, 1)),
		(PF_RADIO, "orientation", "Orientation", "horizontal", 
			(("_horizontal", "horizontal"), ("_vertical", "vertical"))
		)
	],
	[],
	sole_generate_bitmap_font)

main()
