.PHONY: all place table
.SUFFIXES: .tex .dat .pdf .png
.PRECIOUS: %.tex %.dat %.pdf %.png plots/%_v4-0.pdf

scripts  = maketable.py pylib/*.py
variable = dm32
version  = v4-0
data     = data/*.yaml
table    = $(variable)_NO.dat $(variable)_IO.dat
sources  = $(variable)_NO.tex $(variable)_IO.tex $(variable)_NO_dayabay.tex $(variable)_IO_dayabay.tex
tex      = $(variable)_NO_common.tex $(variable)_IO_common.tex comparison_body.tex styles*.tex meta.tex macro_pgf.tex header.tex
targets  = $(sources:%.tex=plots/%_$(version).png)

all: $(targets)

plots/%.png: plots/%.pdf
	convert -density 300 $< $@

plots/%_v4-0.pdf: %.pdf
	cp -v $< $@

%.pdf: %.tex $(table) $(tex)
	latexmk $<

%_NO.dat: $(data)
	./maketable.py -v splitting_large \
	               -o dm32_NO.dat \
		           --nmo NO \
				   $^

%_IO.dat: $(data)
	./maketable.py -v splitting_large \
		           -o dm32_IO.dat \
		           --nmo IO \
				   $^

debug: $(data)
	ipython --pdb -- \
		./maketable.py -v splitting_large \
					   -o dm32_NO.dat \
					   --nmo NO \
					   $^

print-%:
	@echo '$*=$($*)'

clean:
	latexmk -C $(sources)

clean-all: clean
	rm plots/*.pdf plots/*.png
