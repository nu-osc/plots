variable = theta13
version_num = 1
suffix=special
beta=
version_prev = 8
version_dash = $(subst .,-,${version_num})
version  = v${version_dash}${beta}

.SUFFIXES: .tex .dat .pdf .png .yaml
SHELL:=$(shell which bash)
.ONESHELL:

publishdir = ../../../plots/$(variable)/${variable}-v${version_num}-${suffix}
data_latest = $(shell realpath $(wildcard data_latest/*.yaml))
data = $(data_latest)

#
# Name combinations
#
names0 = \
		NMO/latest/$(variable)_$(version)_NMO_latest

names = $(subst NMO,NO,$(names0)) $(subst NMO,IO,$(names0))

# Extensions
extensions = pdf png

#
# Targets
#
tables0 = \
		 plots/$(variable)_$(version)_NMO_latest.dat
tables = $(subst NMO,NO,$(tables0)) $(subst NMO,IO,$(tables0))

targets_plots    = $(foreach n,$(names),$(foreach ext,$(extensions),plots/$(ext)/$(n).$(ext)))
targets          = $(targets_plots) plots/Readme.md

.PRECIOUS: $(tables) $(targets)

#
# Recipes
#
.PHONY: all
all: $(targets) | plots

plots:
	test -d plots || mkdir plots

.PHONY: readme
readme: plots/Readme.md
#plots/Readme.md: Readme.md Makefile | plots
#	cat $< | version_num=$(version_num) beta=$(beta) version_dash=$(version_dash) version_prev=$(version_prev) variable=$(variable) suffix=$(suffix) envsubst > $@

$(targets_plots): $(variable).py configuration.py $(tables) | plots
	@
	DIRNAME=$$(dirname $@)
	test -d $$DIRNAME || mkdir -p $$DIRNAME
	OPTS=; TYPE="theor estimation"; SOURCE=
	case "$@" in
	    *_NO_*) NMO=NO;;
	    *_IO_*) NMO=IO;;
	esac
	case "$@" in
		*_dayabay*)   OPTS="$$OPTS --dayabay"    ;;&
		*_latest*)    SOURCE=plots/$(variable)_$(version)_"$$NMO"_latest.dat ;;&

	esac
	test "$${TYPE# }" && OPTS="$$OPTS -e $$TYPE"
	./$< $$SOURCE $$OPTS -o $@

#
# Tables
#
.PHONY: tables
tables: $tables

$(tables): maketable.py pylib/*.py $(data) | plots
	@
	case "$@" in
		*_latest*)    SOURCE="$(data_latest)"    ;;&
		*_NO_*)       NMO=NO ;;&
		*_IO_*)       NMO=IO ;;&
	esac
	./$< -v $(variable) \
	               -o $@ \
				   $$SOURCE

#
# Misc
#
.PHONY: debug-plot
debug-plot:
	ipython --pdb -- $(script) -s $(tables) --dayabay

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
.PHONY: publish
publish: $(targets)
	@
	test -d $(publishdir) || mkdir -vp $(publishdir)
	cp -rv plots/* $(publishdir)/

.PHONY: publish-readme
publish-readme: plots/Readme.md
	#@cp -v $< $(publishdir)/
