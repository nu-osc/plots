.PHONY: all table debug clean clean-all
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

all: $(targets) | plots

plots:
	mkdir plots

plots/%.png: plots/%.pdf | plots
	convert -density 300 $< $@

plots/%_$(version).pdf: %.pdf | plots
	cp -v $< $@

%.pdf: %.tex $(table) $(tex)
	latexmk -g $<

$(table): $(scripts) | $(data)
	./maketable.py -o $@ $|

debug:
	ipython --pdb -- \
		./maketable.py -o $(variable).dat $(data)
print-%:
	@echo '$*=$($*)'

clean:
	latexmk -C $(sources)

clean-all: clean
	rm plots/*.pdf plots/*.png
