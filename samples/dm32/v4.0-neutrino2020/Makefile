.PHONY: all table debug clean clean-all
.SUFFIXES: .tex .dat .pdf .png
.PRECIOUS: %.tex %.dat %.pdf %.png plots/%_v4-0.pdf

scripts  = maketable.py pylib/*.py
variable = dm32
version  = v4-0
data     = $(realpath $(wildcard data/*.yaml))
table    = $(variable)_NO.dat $(variable)_IO.dat
sources  = $(variable)_NO.tex $(variable)_IO.tex $(variable)_NO_dayabay.tex $(variable)_IO_dayabay.tex
tex      = $(variable)_NO_common.tex $(variable)_IO_common.tex comparison_body.tex styles*.tex meta.tex macro_pgf.tex header.tex
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

%_NO.dat: $(scripts) | $(data)
	./maketable.py -v splitting_large \
	               -o $@ \
		           --nmo NO \
				   $|

%_IO.dat: $(scripts) | $(data)
	./maketable.py -v splitting_large \
		           -o $@ \
		           --nmo IO \
				   $|

debug:
	ipython --pdb -- \
		./maketable.py -v splitting_large \
					   -o $(variable)_NO.dat \
					   --nmo NO \
					   $(data)

print-%:
	@echo '$*=$($*)'

clean:
	latexmk -C $(sources)

clean-all: clean
	rm plots/*.pdf plots/*.png
