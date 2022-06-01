variable = theta12
version_num = 5
suffix = neutrino2022
beta=b
version_prev = 4
version_dash = $(subst .,-,${version_num})
version  = v${version_dash}${beta}

.SUFFIXES: .tex .dat .pdf .png .yaml
.ONESHELL:

publishdir = ../../../plots/$(variable)/${variable}-v${version_num}-${suffix}
data_latest = $(shell realpath $(wildcard data_latest/*.yaml))
data_published = $(shell realpath $(wildcard data_published/*.yaml))
data = $(data_latest) $(data_published)

#
# Name combinations
#
names = \
		latest/$(variable)_$(version)_latest \
		latest/$(variable)_$(version)_latest_global \
	    latest/$(variable)_$(version)_latest_global_future \
	    latest/$(variable)_$(version)_latest_future \
		published/$(variable)_$(version)_published \
		published/$(variable)_$(version)_published_global \
	    published/$(variable)_$(version)_published_global_future \
	    published/$(variable)_$(version)_published_future

# Extensions
extensions = pdf png

#
# Targets
#
tables_latest = plots/$(variable)_$(version)_latest.dat
tables_published = plots/$(variable)_$(version)_published.dat
tables           = $(tables_latest) $(tables_published)
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
plots/Readme.md: Readme.md Makefile | plots
	cat $< | version_num=$(version_num) beta=$(beta) version_dash=$(version_dash) version_prev=$(version_prev) variable=$(variable) suffix=$(suffix) envsubst > $@

$(targets_plots): $(variable).py configuration.py $(tables) | plots
	@
	DIRNAME=$$(dirname $@)
	test -d $$DIRNAME || mkdir -p $$DIRNAME
	OPTS=; TYPE="theor estimation"; SOURCE=
	case "$@" in
		*_global*)    TYPE="$${TYPE#theor}"      ;;&
		*_future*)    TYPE="$${TYPE%estimation}" ;;&
		*_latest*)    SOURCE=$(tables_latest)    ;;&
		*_published*) SOURCE=$(tables_published) ;;&
	esac
	test "$${TYPE# }" && OPTS="$$OPTS -e $$TYPE"
	./$< $(script) $$SOURCE $$OPTS -o $@

#
# Tables
#
.PHONY: tables
tables: $(tables)
$(tables): maketable.py pylib/*.py $(data) | plots
	@
	case "$@" in
		*_latest*)    SOURCE="$(data_latest)"    ;;&
		*_published*) SOURCE="$(data_published)" ;;&
	esac
	./$< -v $(variable) \
	     -o $@ \
	     $$SOURCE

#
# Misc
#
.PHONY: debug-plot
debug-plot:
	ipython --pdb -- $(script) -s $(tables) -e theor

print-%:
	@echo '$*=$($*)'

.PHONY: clean
clean:
	@rm -rv plots/*

.PHONY: unstage
unstage:
	@git rm --cached --ignore-unmatch -r ./plots/

#
# Publish
#
.PHONY: publish
publish: $(targets) | plots
	@
	test -d $(publishdir) || mkdir -vp $(publishdir)
	cp -rv plots/* $(publishdir)/

.PHONY: publish-readme
publish-readme: plots/Readme.md
	@cp -v $< $(publishdir)/
