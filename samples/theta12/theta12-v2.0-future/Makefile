variable = theta12
version  = v2-0b
suffix   = neutrino2020

.PHONY: all table debug clean clean-all publish
.SUFFIXES: .tex .dat .pdf .png .yaml

publishdir = ../../../plots/$(variable)/$(subst -,.,$(version))-$(suffix)
scripts    = maketable.py pylib/*.py
script     = ./$(variable).py
data       = $(shell realpath $(wildcard data/*.yaml))

#
# Name combinations
#
name               = $(variable)_$(version)
name_global        = $(variable)_global_$(version)
name_global_future = $(variable)_global_future_$(version)
names              = $(name) $(name_global) $(name_global_future)
# Extensions
extensions         = pdf png

#
# Targets
#
tables       = $(name).dat
targets      = $(foreach n,$(names),$(foreach ext,$(extensions),plots/$(n).$(ext)))

.PRECIOUS: $(tables) $(targets)

#
# Recipes
#

all: $(targets) | plots

plots:
	test -d plots || mkdir plots

plots/$(variable)_$(version).pdf plots/$(variable)_$(version).png: $(variable)_$(version).dat $(script) *.py | plots
	$(script) $< -o $@ -e theor estimation
	cp -v $< plots/

plots/$(variable)_global_$(version).pdf plots/$(variable)_global_$(version).png: $(variable)_$(version).dat $(script) *.py | plots
	$(script) $< -o $@ -e estimation
	cp -v $< plots/

plots/$(variable)_global_future_$(version).pdf plots/$(variable)_global_future_$(version).png: $(variable)_$(version).dat $(script) *.py | plots
	$(script) $< -o $@
	cp -v $< plots/

table: $(tables)

$(tables): $(scripts) $(data)
	ipython --pdb -- \
	./maketable.py -v $(variable) \
	               -o $@ \
				   $(filter %.yaml,$^)

debug-plot:
	ipython --pdb -- $(script) -s $(tables) -e theor

print-%:
	@echo '$*=$($*)'

clean-all:
	rm plots/*.pdf plots/*.png

publish: all
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp -v plots/* $(publishdir)/
	cp -v $(tables) $(publishdir)/
