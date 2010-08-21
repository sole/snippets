require 'rubygems'
require 'hpricot'

doc = open("bookmarks.html") {|f| Hpricot(f) }

bookmarks = []

(doc/"dl/dt").each do |term|
	link = (term/"a")
	
	if term.next and term.next.name == 'dd'
		desc = term.next.inner_text
	else
		desc = nil
	end
	
	if link.attr('tags')
		tags = link.attr('tags').split(",")
	else
		tags = nil
	end
	
	bookmarks << {
		:address			=>	link.attr('href'),
		:created_at		=>	link.attr('last_visit'),
		:tags					=>	tags,
		:description	=>	desc,
		:title				=>	link.inner_text
	}
	
end
