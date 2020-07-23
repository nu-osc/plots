.PHONY: all place table
.SUFFIXES: .tex .dat .pdf .png
.PRECIOUS: %.tex %.dat %.pdf %.png plots/%_v4-0.pdf

scripts  = maketable.py pylib/*.py
variable = theta13
version = v4-0
data    = data/*.yaml
table   = $(variable).dat
sources = $(variable).tex $(variable)_dayabay.tex
targets = $(sources:%.tex=plots/%_$(version).png)

all: $(targets)

plots/%.png: plots/%.pdf
	convert -density 300 $< $@

plots/%_v4-0.pdf: %.pdf
	cp -v $< $@

%.pdf: %.tex $(data)
	latexmk $<

theta13.dat: $(scripts)
	./maketable.py -o $@ $^

clean:
	latexmk -C $(sources)

clean_all: clean
	rm plots/*.pdf plots/*.png
