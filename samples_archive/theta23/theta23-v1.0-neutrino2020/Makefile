variable = theta23
version  = v1-0
suffix   = neutrino2020

.PHONY: all table debug clean clean-all publish
.SUFFIXES: .tex .dat .pdf .png .yaml

publishdir = ../../../plots/$(variable)/$(subst -,.,$(version))-$(suffix)
scripts    = maketable.py pylib/*.py
script     = ./$(variable).py
data       = $(shell realpath $(wildcard data/*.yaml))
table_NO   = $(variable)_NO_$(version).dat
table_IO   = $(variable)_IO_$(version).dat
tables     = $(table_NO) $(table_IO)
targets_NO = $(table_NO:%.dat=plots/%.png) $(table_NO:%.dat=plots/%.pdf)
targets_IO = $(table_IO:%.dat=plots/%.png) $(table_IO:%.dat=plots/%.pdf)
targets    = $(targets_NO) $(targets_IO)

.PRECIOUS: %.tex %.dat %.pdf %.png $(tables) $(targets)

all: $(targets) | plots

plots:
	test -d plots || mkdir plots

#define plot = 
	#$(script) $< -o $@
	#cp -v $< plots/
#endef

plots/$(variable)_%_$(version).png: $(variable)_%_$(version).dat $(script) | plots
	$(script) $< -o $@
	cp -v $< plots/

plots/$(variable)_%_$(version).pdf: $(variable)_%_$(version).dat $(script) | plots
	$(script) $< -o $@
	cp -v $< plots/

table: $(tables)

$(tables): $(scripts) $(data)
	./maketable.py -v $(variable) \
	               -o $@ \
				   $(filter %.yaml,$^)

debug-plot:
	ipython --pdb -- $(script) -s $(table_NO) --nmo NO

print-%:
	@echo '$*=$($*)'

clean-all:
	rm plots/*.pdf plots/*.png

publish: all
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp -v plots/* $(publishdir)/
	cp -v $(table_IO) $(table_NO) $(publishdir)/
