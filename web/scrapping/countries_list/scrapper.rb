require 'rubygems'
require 'hpricot'
require 'open-uri'
require 'fileutils'

# setup tmp dir & files first
tmp_dir = File.join('.', 'tmp')
spanish_url = 'http://es.wikipedia.org/wiki/ISO_3166-1'
spanish_file = File.join(tmp_dir, 'es')

if not File.exist?(tmp_dir)
	FileUtils.mkdir(tmp_dir)
end

if not File.exist?(spanish_file)
	f = File.new(spanish_file, "w")
	open(spanish_url) {|uf|
		uf.each_line {|line| f << line}
	}
	f.close
end

# Spanish list

doc = open(spanish_file) { |f| Hpricot(f) }

pres = doc/"pre"

countries_spanish = {}

pres.each{|e|
#	p e.children.length
	e.children.each{|c|
		p c
	}
	i = 0
	while i < e.children.length do
		# codes (text node)
		# link to 3166#country
		# space (text node)
		# flag
		# country name in spanish
		codes = e.children[i]
		name = e.children[i+4]
		
		puts codes, name
		
		i = i + 4	
		puts "---"
	end
	puts "======================"
	break
}
