.PHONY: all place table
.SUFFIXES: .tex .dat .pdf .png
.PRECIOUS: %.tex %.dat %.pdf %.png plots/%_v4-0.pdf

scripts  = maketable.py pylib/*.py
variable = theta13
version  = v4-0
data     = data/*.yaml
table    = $(variable).dat
sources  = $(variable).tex $(variable)_dayabay.tex
tex      = $(variable)_common.tex comparison_body.tex styles*.tex meta.tex macro_pgf.tex header.tex
targets  = $(sources:%.tex=plots/%_$(version).png)

all: $(targets)

plots/%.png: plots/%.pdf
	convert -density 300 $< $@

plots/%_v4-0.pdf: %.pdf
	cp -v $< $@

%.pdf: %.tex $(table) $(tex)
	latexmk $<

$(table): $(data)
	./maketable.py -o $@ $^

debug: $(data)
	ipython --pdb -- ./maketable.py -o $@ $^

clean:
	latexmk -C $(sources)

clean_all: clean
	rm plots/*.pdf plots/*.png
