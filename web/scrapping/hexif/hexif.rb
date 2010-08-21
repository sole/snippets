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

require 'rubygems'
require 'hpricot'
require 'open-uri'

# doc = Hpricot(open("http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html"))
doc = open("EXIF.html") { |f| Hpricot(f) }

rows = []

(doc/"table.inner//tr").each do |row|
    cells = []
    (row/"td").each do |cell|
       
        if (cell/" span.s").length > 0
              values = (cell/"span.s").inner_html.split('<br />').collect{ |str| 
              pair = str.strip.split('=').collect{|val| val.strip}
              Hash[pair[0], pair[1]]
            }
            
            if(values.length==1)
              cells << cell.inner_text
            else
              cells << values
            end
            
        elsif
            cells << cell.inner_text
        end
    end
    rows << cells
    
end

rows.shift

#p rows.to_yaml

File.open('hexif.yaml', 'w') { |f|
  f << rows.to_yaml
}