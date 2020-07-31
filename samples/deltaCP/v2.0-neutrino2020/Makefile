variable = deltaCP
version  = v2-0
suffix   = neutrino2020

.PHONY: all table debug clean clean-all publish
.SUFFIXES: .tex .dat .pdf .png .yaml
.PRECIOUS: %.tex %.dat %.pdf %.png plots/%_$(version).pdf plots/%_$(version).png

publishdir = ../../../plots/$(variable)/$(subst -,.,$(version))-$(suffix)
scripts  = maketable.py pylib/*.py
data     = $(shell realpath $(wildcard data/*.yaml))
table_NO   = $(variable)_NO_$(version).dat
table_IO   = $(variable)_IO_$(version).dat
tables     = $(table_NO) $(table_IO)
targets_NO = $(table_NO:%.dat=plots/%.png) $(table_NO:%.dat=plots/%.pdf)
targets_IO = $(table_IO:%.dat=plots/%.png) $(table_IO:%.dat=plots/%.pdf)
targets    = $(targets_NO) $(targets_IO)

all: $(targets) | plots

plots:
	test -d plots || mkdir plots

plots/$(variable)_%_$(version).png plots/$(variable)_%_$(version).pdf: $(variable)_%_$(version).dat plot_deltacp.py | plots
	./plot_deltacp.py $< --ordering $(findstring NO,$@)$(findstring IO,$@) -o $@
	cp $< plots/

table: $(tables)

$(tables): $(scripts) $(data)
	./maketable.py -v $(variable) \
	               -o $@ \
		           --nmo $(findstring NO,$@)$(findstring IO,$@) \
				   $(filter %.yaml,$^)

debug:
	ipython --pdb -- \
		./maketable.py -v $(variable) \
					   -o $(variable)_NO.dat \
					   --nmo NO \
					   $(data)
	ipython --pdb -- \
		./maketable.py -v $(variable) \
					   -o $(variable)_IO.dat \
					   --nmo IO \
					   $(data)

print-%:
	@echo '$*=$($*)'

clean-all:
	rm plots/*.pdf plots/*.png

publish: all
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp plots/* $(publishdir)/
	cp $(table_IO) $(table_NO) $(publishdir)/
