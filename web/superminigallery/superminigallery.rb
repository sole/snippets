# MIT LICENSE
# 
# Copyright (c) 2007 Soledad Penades www.soledadpenades.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

require 'FileUtils'
require 'rubygems'
require 'RMagick'
require 'builder'

output_path = 'output'

versions = {
  'thumbnail' =>  [300,150],
  'big'       =>  [1024,768]
}

exif_fields = {
  'Taken'     =>  'DateTimeOriginal',
  'Camera'    =>  'Model',
  'Exposure'  =>  'ExposureTime',  
  'Shutter Speed' =>  'ShutterSpeedValue'
}

xhtml = ''

x = Builder::XmlMarkup.new(:target=>xhtml, :indent=>1)

x.instruct!
x.declare! :DOCTYPE, :html, :PUBLIC, "-//W3C//DTD XHTML 1.0 Strict//EN", "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
x.html( "xmlns" => "http://www.w3.org/1999/xhtml" ) { 
  x.head { 
    x.title "superminigallery"
    x.style( "type"=>"text/css" ) { x.text! "
      body{
        font-family:georgia,serif
      }
      
      h1,h2 {
        margin-top: 0;
      }
      
      a {
        border-bottom: 3px solid #EC008C;
      }
      
      img {
        border: 0;
      }
      
      .picture {
        border-bottom: 2px solid #aaa;
        float: left;
        margin: 10px;
        padding: 10px 0;
        width: 310px;
      }
      " } 
  }


  begin
    FileUtils.mkdir output_path
  rescue
  end

  x.body {
    x.h1('superminigallery')

		draw = Magick::Draw.new
		draw.gravity = Magick::CenterGravity
		draw.pointsize = 64
		draw.font_family = "Helvetica"
		draw.font_weight = Magick::BoldWeight
		draw.stroke = 'none'
		draw.fill = "#ffffff99"
		

		Dir['*.jpg','*.JPG'].sort.each do |f|
			img = Magick::Image.read(f).first
			versions.each do |k,v|
				version_file =  k + '_' + f
				output_img_path = File.join(output_path, version_file)
				puts "converting #{f} into #{output_img_path}"
				
				begin      
					if(k=='thumbnail')
						x.div('class'=>'picture') {
							x.h2(f)
							x.a('href'=> version_file.sub('thumbnail_', 'big_')) {
								x.img('src'=>version_file)
							}
							x.dl {
								x.dt('Dimensions')
								x.dd(img.columns.to_s + ' x ' + img.rows.to_s)

								exif_fields.each do |title, field|
									key = "Exif:#{field}"
									if img[key]!=nil
										x.dt(title)
										x.dd(img[key])
									end
								end
							}
						}
					end

					version = img.crop_resized(v[0], v[1])
					if(k=='big')
						draw.annotate(version, 0, 0, 0, 0, "(c) soledadpenades.com")
					end
					version.write output_img_path
				rescue => exception
					print exception.backtrace.join("\n")
					exit
				end
				GC.start
			end
		end
	}
}

File.open(File.join(output_path, 'index.html'), 'w+') do |file|
  file.puts xhtml
end