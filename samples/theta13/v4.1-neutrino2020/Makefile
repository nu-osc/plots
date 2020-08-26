variable = theta13
version  = v4-1
suffix   = neutrino2020

.PHONY: all table debug clean clean-all publish
.SUFFIXES: .tex .dat .pdf .png .yaml 

publishdir = ../../../plots/$(variable)/$(subst -,.,$(version))-$(suffix)
scripts    = *.py pylib/*.py
script     = ./$(variable).py
data       = $(shell realpath $(wildcard data/*.yaml))

#
# Name combinations
#
name         = $(variable)_$(version)
name_global  = $(variable)_global_$(version)
name_dayabay = $(variable)_dayabay_$(version)
names        = $(name) $(name_global) $(name_dayabay)
# Extensions
extensions   = pdf png

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

plots/$(variable)_$(version).pdf plots/$(variable)_$(version).png: $(variable)_$(version).dat $(script) | plots
	$(script) $< -o $@ -e theor
	cp -v $< plots/

plots/$(variable)_dayabay_$(version).pdf plots/$(variable)_dayabay_$(version).png: $(variable)_$(version).dat $(script) | plots
	$(script) $< -o $@ -e theor --dayabay

plots/$(variable)_global_$(version).pdf plots/$(variable)_global_$(version).png: $(variable)_$(version).dat $(script) | plots
	$(script) $< -o $@

$(tables): $(scripts) $(data)
	./maketable.py -v $(variable) \
	               -o $@ \
				   $(filter %.yaml,$^)

debug-plot:
	ipython --pdb -- $(script) -s $(tables) --dayabay

print-%:
	@echo '$*=$($*)'

clean-all:
	rm plots/*.pdf plots/*.png

publish: all
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp plots/* $(publishdir)/
