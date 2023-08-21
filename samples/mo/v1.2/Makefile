variable = mo
version  = v1-2
suffix   = none 

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

plots/$(variable)_$(version).png: $(data) mo.py | plots
	./mo.py $(data) -o $@ 

plots/$(variable)_$(version).pdf: $(data) mo.py | plots
	./mo.py $(data) -o $@

print-%:
	@echo '$*=$($*)'

clean-all:
	rm plots/*.pdf plots/*.png

publish: all
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp -v plots/* $(publishdir)/
