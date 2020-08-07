variable = future_nmo
version  = v1-0
suffix   = neutrino2020

.PHONY: all table debug clean clean-all publish
.SUFFIXES: .tex .dat .pdf .png .yaml
.PRECIOUS: %.tex %.dat %.pdf %.png plots/$(variable)_$(version).pdf plots/$(variable)_$(version).png

publishdir = ../../../plots/$(variable)/$(subst -,.,$(version))-$(suffix)
scripts  = maketable.py pylib/*.py
data     = $(shell realpath $(wildcard data/*.yaml))
targets  = plots/$(variable)_$(version).png plots/$(variable)_$(version).pdf

all: $(targets) | plots

plots:
	test -d plots || mkdir plots

plots/$(variable)_$(version).png: $(data) future_mo.py | plots
	./future_mo.py $(data) -o $@

plots/$(variable)_$(version).pdf: $(data) future_mo.py | plots
	./future_mo.py $(data) -o $@

print-%:
	@echo '$*=$($*)'

clean-all:
	rm plots/*.pdf plots/*.png

publish: all
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp plots/* $(publishdir)/
	cp $(table_IO) $(table_NO) $(publishdir)/
