all: \
	out/static \
	out/favicon.ico \
	out/static/gen \
	out/atom.xml{% for page in pages %} \
	out/{{ page }}{% endfor %} \
	out/blog/index.html{% for post in posts %} \
	out/blog/{{ post.pubdate.__format__('%Y/%m/%d') }}/{{ post.slug}}.html{% endfor %}

out:
	mkdir -p $@

out/static: static out
	cp -a $< $@

out/favicon.ico: out/static
	cp $</images/favicon.ico $@

out/atom.xml:{%for post in posts %} \
	content/blog/{{ post.pubdate.__format__('%Y%m%d') }}_{{ post.slug}}.html{% endfor %}
	python -m yassg renderatomfeed -o $@ $^

out/static/gen: out/static
	npm run build

out/blog/index.html:{%for post in posts %} \
	content/blog/{{ post.pubdate.__format__('%Y%m%d') }}_{{ post.slug}}.html{% endfor %}
	python -m yassg renderblogindex -o $@ $^
{% for post in posts %}
out/blog/{{ post.pubdate.__format__('%Y/%m/%d') }}/{{ post.slug }}.html: content/blog/{{ post.pubdate.__format__('%Y%m%d') }}_{{ post.slug}}.html
	python -m yassg renderpost -o $@ $<
{% endfor %}{% for page in pages %}
out/{{ page }}: content/{{ page }}
	python -m yassg renderpage -o $@ $^
{% endfor %}
clean:
	$(RM) -rf out

.PHONY: all clean