variable = theta12
version  = v1-0
suffix   = neutrino2020

.PHONY: all table debug clean clean-all publish
.SUFFIXES: .tex .dat .pdf .png .yaml

publishdir = ../../../plots/$(variable)/$(subst -,.,$(version))-$(suffix)
scripts    = maketable.py pylib/*.py
script     = ./theta12.py
data       = $(shell realpath $(wildcard data/*.yaml))
tables     = $(variable)_$(version).dat
targets    = $(tables:%.dat=plots/%.png) $(tables:%.dat=plots/%.pdf)

.PRECIOUS: %.tex %.dat %.pdf %.png $(tables) $(targets)

all: $(targets) | plots

plots:
	test -d plots || mkdir plots

#define plot = 
	#$(script) $< -o $@
	#cp -v $< plots/
#endef

plots/$(variable)_$(version).png: $(variable)_$(version).dat $(script) | plots
	$(script) $< -o $@
	cp -v $< plots/

plots/$(variable)_$(version).pdf: $(variable)_$(version).dat $(script) | plots
	$(script) $< -o $@
	cp -v $< plots/

table: $(tables)

$(tables): $(scripts) $(data)
	./maketable.py -v $(variable) \
	               -o $@ \
				   $(filter %.yaml,$^)

debug:
	ipython --pdb -- \
		./maketable.py -v $(variable) \
					   -o $(variable)_NO.dat \
					   $(data)
	ipython --pdb -- \
		./maketable.py -v $(variable) \
					   -o $(variable)_IO.dat \
					   $(data)

print-%:
	@echo '$*=$($*)'

clean-all:
	rm plots/*.pdf plots/*.png

publish: all
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp plots/* $(publishdir)/
	cp $(table_IO) $(table_NO) $(publishdir)/
