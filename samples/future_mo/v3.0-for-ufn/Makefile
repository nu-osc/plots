variable = future_nmo
version_num = 3.0
suffix   = ufn_2021
beta = b
version_prev = 1.0
version_dash = $(subst .,-,${version_num})
version  = v${version_dash}${beta}

.PHONY: all table debug clean clean-all publish
.SUFFIXES: .tex .dat .pdf .png .yaml
.PRECIOUS: %.tex %.dat %.pdf %.png plots/$(variable)_$(version).pdf plots/$(variable)_$(version).png

publishdir = ../../../plots/$(variable)/${variable}-${version_num}-${suffix}
scripts    = *.py pylib/*.py
data       = $(shell realpath $(wildcard data/*.yaml))
targets    = plots/$(variable)_$(version).png plots/$(variable)_$(version).pdf plots/Readme.md

all: $(targets) | plots

plots:
	test -d plots || mkdir plots

plots/Readme.md: Readme.md Makefile | plots
	cat $< | version_num=${version_num} beta=${beta} version_dash=${version_dash} version_prev=${version_prev} envsubst > $@

plots/$(variable)_$(version).png: $(data) future_mo.py | plots
	./future_mo.py $(data) -o $@

plots/$(variable)_$(version).pdf: $(data) future_mo.py | plots
	./future_mo.py $(data) -o $@

print-%:
	@echo '$*=$($*)'

clean-all:
	rm plots/*.pdf plots/*.png

publish: $(targets) | plots
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp -v plots/* $(publishdir)/
