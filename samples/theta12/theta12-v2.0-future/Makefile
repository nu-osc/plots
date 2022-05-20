variable = theta12
version_num = 2.0
suffix   = neutrino2020
beta=
version_prev = 1.0
version_dash = $(subst .,-,${version_num})
version  = v${version_dash}${beta}

.PHONY: all table debug clean clean-all publish
.SUFFIXES: .tex .dat .pdf .png .yaml

publishdir = ../../../plots/$(variable)/${variable}-${version_num}-${suffix}
scripts    = *.py pylib/*.py
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
tables       = plots/$(name).dat
targets      = $(foreach n,$(names),$(foreach ext,$(extensions),plots/$(n).$(ext))) plots/Readme.md

.PRECIOUS: $(tables) $(targets)

#
# Recipes
#

all: $(targets) | plots

plots:
	test -d plots || mkdir plots

plots/Readme.md: Readme.md Makefile | plots
	cat $< | version_num=${version_num} beta=${beta} version_dash=${version_dash} version_prev=${version_prev} envsubst > $@

plots/$(variable)_$(version).pdf plots/$(variable)_$(version).png: plots/$(variable)_$(version).dat $(script) | plots
	$(script) $< -o $@ -e theor estimation

plots/$(variable)_global_$(version).pdf plots/$(variable)_global_$(version).png: plots/$(variable)_$(version).dat $(script) | plots
	$(script) $< -o $@ -e estimation

plots/$(variable)_global_future_$(version).pdf plots/$(variable)_global_future_$(version).png: plots/$(variable)_$(version).dat $(script) | plots
	$(script) $< -o $@

table: $(tables)

$(tables): $(scripts) $(data) | plots
	./maketable.py -v $(variable) \
	               -o $@ \
				   $(filter %.yaml,$^)

debug-plot:
	ipython --pdb -- $(script) -s $(tables) -e theor

print-%:
	@echo '$*=$($*)'

clean-all:
	rm plots/*.pdf plots/*.png

publish: $(targets) | plots
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp -v plots/* $(publishdir)/
