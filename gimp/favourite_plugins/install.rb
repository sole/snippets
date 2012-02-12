# encoding: utf-8
require 'open-uri'
require 'pathname'

=begin

A ruby script for downloading, installing and placing underneath a sane menu entry my favourite gimp scripts for photo manipulation (hence they go under "Filters/Photo"). You can change it by changing the menu_entry variable. See below...

=end

Encoding.default_external = 'UTF-8'

def download_file(src_url, dst_path)
	dst_file = File.join(dst_path, src_url.split('/').last)
	
	open(dst_file, 'wb') do |f|
		f << open(src_url).read
	end if not File.exists?(dst_file) or File.size(dst_file) == 0
	
	return dst_file
end

def patch_menu_entry(script_file, orig_entry, new_entry)
	script_contents = open(script_file, 'rb').read
	open(script_file, 'wb') do |f|
		f << script_contents.gsub(orig_entry, new_entry)
	end
end

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

gimp_dir = File.expand_path('~/.gimp-2.6')
scripts_dir = File.join(gimp_dir, 'scripts')
menu_entry = '<Image>/Filters/Photo'

# Add film grain
patch_menu_entry(download_file('http://registry.gimp.org/files/Eg-AddFilmGrain.scm', scripts_dir), '<Image>/Filters/Eg', menu_entry)

# Black and white film
patch_menu_entry(download_file('http://registry.gimp.org/files/adsr-bw-films.scm', scripts_dir), '<Image>/Colors', menu_entry)

# Diana/holga
patch_menu_entry(download_file('http://www.vide.memoire.free.fr/photo/textes/contrefacons/diana-holga2d.scm', scripts_dir), '<Image>/Filters/jp/diana-holga2d', menu_entry + "/Diana-Holga")

# Film Imitation Lab http://registry.gimp.org/node/24639 TODO (needs uncompressing a zip file)

# gimp-resynthesizer TODO

# Lomo
patch_menu_entry(download_file('http://registry.gimp.org/files/elsamuko-lomo.scm', scripts_dir), '<Image>/Filters/Light and Shadow', menu_entry)

# Movie 300
patch_menu_entry(download_file('http://registry.gimp.org/files/elsamuko-movie-300.scm', scripts_dir), '<Image>/Filters/Artistic', menu_entry)

# National Geographic
patch_menu_entry(download_file('http://registry.gimp.org/files/elsamuko-national-geographic.scm', scripts_dir), '<Image>/Filters/Generic', menu_entry)

# Photochrom
patch_menu_entry(download_file('http://registry.gimp.org/files/elsamuko-photochrom.scm', scripts_dir), '<Image>/Filters/Artistic', menu_entry)

# Technicolor 2
patch_menu_entry(download_file('http://registry.gimp.org/files/elsamuko-technicolor-2-color.scm', scripts_dir), '<Image>/Colors', menu_entry)

# Technicolor 3
patch_menu_entry(download_file('http://registry.gimp.org/files/elsamuko-technicolor-3-color.scm', scripts_dir), '<Image>/Colors', menu_entry)

# Vintage look
patch_menu_entry(download_file('http://registry.gimp.org/files/mm1-vintage-look.0.3_0.scm', scripts_dir), '<Image>/Filters/Artistic', menu_entry)
