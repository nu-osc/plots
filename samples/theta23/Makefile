variable = theta23
version_num = 6
suffix   =
beta=
version_prev = 4
version_dash = $(subst .,-,${version_num})
version  = v${version_dash}${beta}

.PHONY: all table debug clean clean-all publish
.SUFFIXES: .tex .dat .pdf .png .yaml
SHELL:=$(shell which bash)
.ONESHELL:

publishdir = ../../../plots/$(variable)/${variable}-v${version_num}-${suffix}
data_latest = $(shell realpath $(wildcard data_latest/*.yaml))
data_published = $(shell realpath $(wildcard data_published/*.yaml))
data = $(data_latest) $(data_published)

#
# Name combinations
#
names0 = \
		NMO/latest/$(variable)_$(version)_NMO_latest \
		NMO/latest/$(variable)_$(version)_NMO_latest_global \
		NMO/latest/$(variable)_$(version)_NMO_latest_global_future \
		NMO/latest/$(variable)_$(version)_NMO_latest_future \
		NMO/published/$(variable)_$(version)_NMO_published \
		NMO/published/$(variable)_$(version)_NMO_published_global \
		NMO/published/$(variable)_$(version)_NMO_published_global_future \
		NMO/published/$(variable)_$(version)_NMO_published_future 

names = $(subst NMO,NO,$(names0)) $(subst NMO,IO,$(names0))

# Extensions
extensions = pdf png

#
# Tables
#
tables0 = \
		 plots/$(variable)_$(version)_NMO_latest.dat \
		 plots/$(variable)_$(version)_NMO_published.dat
tables = $(subst NMO,NO,$(tables0)) $(subst NMO,IO,$(tables0))

#
# Targets
#
targets_plots = $(foreach n,$(names),$(foreach ext,$(extensions),plots/$(ext)/$(n).$(ext)))
target_readme = plots/Readme.md
targets       = $(target_readme) $(targets_plots)

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
	TYPE="theor estimation"
	case "$@" in
		*_NO_*) NMO=NO;;
		*_IO_*) NMO=IO;;
	esac
	case "$@" in
		*_global*)    TYPE="$${TYPE#theor}"      ;;&
		*_future*)    TYPE="$${TYPE%estimation}" ;;&
		*_latest*)    SOURCE=plots/$(variable)_$(version)_"$$NMO"_latest.dat ;;&
		*_published*) SOURCE=plots/$(variable)_$(version)_"$$NMO"_published.dat ;;&
	esac
	test "$${TYPE# }" && OPTS="$$OPTS -e $$TYPE"
	./$< $$SOURCE $$OPTS -o $@

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
	ipython --pdb -- $(script) -s $(table_NO) --nmo NO

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
