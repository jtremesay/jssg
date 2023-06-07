all: \
	out/static \
	out/static/gen \
	out/index.html \
	out/cgi.html \
	out/cv.html \
	out/blog/index.html \
	out/blog/2023/05/31/helloworld.html \
	out/blog/2023/06/06/chaines_youtube.html

out:
	mkdir -p $@

out/static: static out
	cp -a $< $@

out/static/gen:
	npm run build

out/blog/index.html: \
	content/blog/20230531_helloworld.html \
	content/blog/20230606_chaines_youtube.html
	python -m yassg renderblogindex -o $@ $^

out/blog/2023/05/31/helloworld.html: content/blog/20230531_helloworld.html
	python -m yassg renderpost -o $@ $<

out/blog/2023/06/06/chaines_youtube.html: content/blog/20230606_chaines_youtube.html
	python -m yassg renderpost -o $@ $<

out/%.html: content/%.html
	python -m yassg renderpage -o $@ $^

clean:
	$(RM) -rf \
		out

.PHONY: all clean