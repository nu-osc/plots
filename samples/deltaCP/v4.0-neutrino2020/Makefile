.PHONY: all table debug clean clean-all
.SUFFIXES: .tex .dat .pdf .png
.PRECIOUS: %.tex %.dat %.pdf %.png plots/%_v4-0.pdf

scripts  = maketable.py pylib/*.py
variable = deltaCP
version  = v1-0
data     = data/*.yaml
table    = $(variable)_NO.dat $(variable)_IO.dat
#sources  = $(variable)_NO.tex $(variable)_IO.tex
#tex      = $(variable)_NO_common.tex $(variable)_IO_common.tex comparison_body.tex styles*.tex meta.tex macro_pgf.tex header.tex
#targets  = $(sources:%.tex=plots/%_$(version).png)

all: $(targets) | plots

plots:
	mkdir plots

plots/%.png: plots/%.pdf | plots
	convert -density 300 $< $@

plots/%_$(version).pdf: %.pdf | plots
	cp -v $< $@

%.pdf: %.tex table $(tex)
	#latexmk -g $<
	echo Empty target: add a script to provide pdfs

table: $(table)

%_NO.dat: $(scripts) | $(data)
	./maketable.py -v $(variable) \
	               -o $@ \
		           --nmo NO \
				   $|

%_IO.dat: $(scripts) | $(data)
	./maketable.py -v $(variable) \
		           -o $@ \
		           --nmo IO \
				   $|

debug:
	ipython --pdb -- \
		./maketable.py -v $(variable) \
					   -o $(variable)_NO.dat \
					   --nmo NO \
					   $(data)

print-%:
	@echo '$*=$($*)'

clean:
	#latexmk -C $(sources)

clean-all: clean
	rm plots/*.pdf plots/*.png
