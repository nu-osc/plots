variable = future_nmo
version_num = 3
suffix   = ufn_2021
beta =
version_prev = 2.0
version_dash = $(subst .,-,${version_num})
version  = v${version_dash}${beta}

.PHONY: all table debug clean clean-all publish
.SUFFIXES: .tex .dat .pdf .png .yaml
.PRECIOUS: %.tex %.dat %.pdf %.png plots/$(variable)_$(version).pdf plots/$(variable)_$(version).png

publishdir = ../../../plots/$(variable)/${variable}-${version_num}-${suffix}
scripts    = *.py pylib/*.py
data       = $(shell realpath $(wildcard data/*.yaml))
targets    = plots/$(variable)_$(version).png plots/$(variable)_$(version).pdf plots/Readme.md

#
# Recipes
#
.PHONY: all
all: $(targets) | plots

plots:
	test -d plots || mkdir plots

.PHONY: readme
readme: plots/Readme.md
plots/Readme.md: Readme.md Makefile | plots
	cat $< | version_num=$(version_num) beta=$(beta) version_dash=$(version_dash) version_prev=$(version_prev) variable=$(variable) suffix=$(suffix) envsubst > $@

plots/$(variable)_$(version).%: $(data) future_mo.py | plots
	./future_mo.py $(data) -o $@

#
# Misc
#
print-%:
	@echo '$*=$($*)'

.PHONY: clean
clean:
	@rm -rv plots/*

.PHONY: unstage
unstage:
	@git rm --cached --ignore-unmatch -r ./plots/

.PHONY: stage
stage: $(targets)
	@git add -f ./plots/

#
# Publish
#
publish: $(targets)
	@
	test -d $(publishdir) || mkdir -vp $(publishdir)
	cp -rv plots/* $(publishdir)/

.PHONY: publish-readme
publish-readme: plots/Readme.md
	@cp -v $< $(publishdir)/
