variable = theta13
version  = v0-1
suffix   = anim

.PHONY: all tables debug clean clean-all publish
.SUFFIXES: .dat .fig .yaml

data-dayabay = $(shell realpath $(wildcard data/dayabay*.yaml))
data-dchooz  = $(shell realpath $(wildcard data/dchooz*.yaml))
data-reno    = $(shell realpath $(wildcard data/reno*.yaml))
data-t2k     = $(shell realpath $(wildcard data/t2k*.yaml))
exp-list     = dayabay reno dchooz t2k_NO t2k_IO
data-list    = $(foreach n,$(exp-list),data-$(n))
data-all     = $(foreach n,$(data-list),$($(n)))

tables       = $(foreach n,$(exp-list),plots/$(variable)-$(n)-$(suffix)_$(version).dat)

publishdir   = ../../../plots/$(variable)-$(suffix)/$(subst -,.,$(version))
scripts      = *.py pylib/*.py
script       = ./$(variable)-$(suffix).py
script-table = maketable.py

#
# Name combinations
#
name         = $(variable)-$(suffix)_$(version)
#name_global  = $(variable)_global_$(version)
#name_dayabay = $(variable)_dayabay_$(version)
#names        = $(name) $(name_global) $(name_dayabay)
names        = $(name)
extensions   = gif apng

#
# Targets
#
targets      = $(foreach n,$(names),$(foreach ext,$(extensions),plots/$(n).$(ext)))

.PRECIOUS: $(tables) $(targets)

#
# Recipes
#

all: $(targets) | plots

tables: $(tables) $(data-all)

plots:
	test -d plots || mkdir plots

$(targets) &: $(tables) $(script) | plots
	ipython --pdb -- \
		$(script) $(tables) -o $(targets)

#plots/$(variable)_dayabay_$(version).pdf plots/$(variable)_dayabay_$(version).png: $(variable)_$(version).dat $(script) | plots
	#$(script) $< -o $@ -e theor --dayabay

#plots/$(variable)_global_$(version).pdf plots/$(variable)_global_$(version).png: $(variable)_$(version).dat $(script) | plots
	#$(script) $< -o $@

theta13-%.dat: maketable.py data/%_*.yaml
	ipython --pdb -- \
	./maketable.py -v $(variable) \
	               -o $@ \
				   $(filter %.yaml,$^)

#debug-plot:
	#ipython --pdb -- $(script) -s $(tables) --dayabay

print-%:
	@echo '$*=$($*)'

clean-all:
	rm plots/*.pdf plots/*.png

publish: all
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp -v plots/* $(publishdir)/
