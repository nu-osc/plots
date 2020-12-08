variable = dm32
version  = v1-0
suffix   = anim

.PHONY: all tables debug clean clean-all publish
.SUFFIXES: .dat .fig .yaml

data-dayabay = $(shell realpath $(wildcard data/dayabay*.yaml))
data-reno    = $(shell realpath $(wildcard data/reno*.yaml))
data-minos   = $(shell realpath $(wildcard data/minos*.yaml))
data-t2k     = $(shell realpath $(wildcard data/t2k*.yaml))
data-nova    = $(shell realpath $(wildcard data/nova*.yaml))
exp-list     = dayabay nova t2k minos reno
data-list    = $(foreach n,$(exp-list),data-$(n))
data-all     = $(foreach n,$(data-list),$($(n)))

tables       = $(foreach n,$(exp-list),plots/data/$(variable)-$(n)-$(suffix)_$(version).dat)

publishdir   = ../../../plots/$(variable)-$(suffix)/$(variable)-$(suffix)-$(subst -,.,$(version))
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

plots/data:
	test -d plots/data || mkdir -p plots/data

$(targets) &: $(tables) $(script) style.py | plots
	ipython --pdb -- \
		$(script) $(tables) -o $(targets)

#plots/$(variable)_dayabay_$(version).pdf plots/$(variable)_dayabay_$(version).png: $(variable)_$(version).dat $(script) | plots
	#$(script) $< -o $@ -e theor --dayabay

#plots/$(variable)_global_$(version).pdf plots/$(variable)_global_$(version).png: $(variable)_$(version).dat $(script) | plots
	#$(script) $< -o $@

plots/data/$(variable)-%-$(suffix)_$(version).dat: maketable.py data/%_*.yaml | plots/data
	ipython --pdb -- \
	./maketable.py -v $(variable) --nmo NO \
	               -o $@ \
				   $(filter %.yaml,$^)

#debug-plot:
	#ipython --pdb -- $(script) -s $(tables) --dayabay

print-%:
	@echo '$*=$($*)'

clean:
	rm plots/*.gif plots/*.apng plots/*.dat

publish: all
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp -v plots/* $(publishdir)/
