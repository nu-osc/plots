variable = deltaCP
version  = v1-0

.PHONY: all table debug clean clean-all
.SUFFIXES: .tex .dat .pdf .png .yaml
.PRECIOUS: %.tex %.dat %.pdf %.png plots/%_$(version).pdf

scripts  = maketable.py pylib/*.py
data     = $(shell realpath --relative-to . $(wildcard data/*.yaml))
table_NO   = $(variable)_NO.dat
table_IO   = $(variable)_IO.dat
targets_NO = $(table_NO:%.dat=plots/%_$(version).png) $(table_NO:%.dat=plots/%_$(version).pdf)
targets_IO = $(table_IO:%.dat=plots/%_$(version).png) $(table_IO:%.dat=plots/%_$(version).pdf)
targets    = $(targets_NO) $(targets_IO)

all: $(targets) | plots

plots:
	test -d plots || mkdir plots

$(targets_NO): $(table_NO) plot_deltacp.py
	./plot_deltacp.py $< --ordering NO -o $@

$(targets_IO): $(table_IO) plot_deltacp.py
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

clean-all:
	rm plots/*.pdf plots/*.png
