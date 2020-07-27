.PHONY: all table debug clean clean-all
.SUFFIXES: .tex .dat .pdf .png .yaml
.PRECIOUS: %.tex %.dat %.pdf %.png plots/%_v1-0.pdf

scripts  = maketable.py pylib/*.py
variable = deltaCP
version  = v1-0
data     = $(shell realpath --relative-to . $(wildcard data/*.yaml))
table    = $(variable)_NO.dat $(variable)_IO.dat
targets  = $(table:%.dat=plots/%_$(version).png)

all: $(targets) | plots

plots:
	test -d plots || mkdir plots

plots/%.png: plots/%.pdf | plots
	convert -density 300 $< $@

plots/%_$(version).pdf: %.pdf | plots
	cp -v $< $@

$(variable)_NO.pdf: $(variable)_NO.dat
	./plot_deltacp.py $< --ordering NO -o $@

$(variable)_IO.pdf: $(variable)_IO.dat
	./plot_deltacp.py $< --ordering IO -o $@

table: $(table)

%_NO.dat: $(scripts) $(data)
	./maketable.py -v $(variable) \
	               -o $@ \
		           --nmo NO \
				   $(filter %.yaml,$^)

%_IO.dat: $(scripts) $(data)
	./maketable.py -v $(variable) \
		           -o $@ \
		           --nmo IO \
				   $(filter %.yaml,$^)

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
