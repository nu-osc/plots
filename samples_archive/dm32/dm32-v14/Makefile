variables=dm31 dm32
variable=dm32
version_num=14
suffix=none
beta=
version_prev=13
version_dash=$(subst .,-,${version_num})
version=v${version_dash}${beta}

.SUFFIXES: .tex .dat .pdf .png .yaml
SHELL:=$(shell which bash)
.ONESHELL:

publishdir=../../../plots/$(variable)/${variable}-v${version_num}-${suffix}
data_latest=$(shell realpath $(wildcard data_latest/*.yaml))
data_published=$(shell realpath $(wildcard data_published/*.yaml))
data=$(data_latest) $(data_published)

#
# Name combinations
#
times=latest published
suffixes=_ _global _global_future _future
names=$(foreach NMO,NO IO,$(foreach variable,$(variables),$(foreach time,$(times),$(foreach suffix,$(suffixes),$(NMO)/$(time)/$(variable)/$(variable)_$(version)_$(NMO)_$(time)$(suffix)))))
names:=$(names:_=)

# Extensions
extensions=pdf png

#
# Tables
#
tables=$(foreach variable,$(variables),$(foreach NMO,NO IO,$(foreach time,$(times),plots/$(variable)_$(version)_$(NMO)_$(time).dat)))

#
# Targets
#
targets_plots=$(foreach n,$(names),$(foreach ext,$(extensions),plots/$(ext)/$(n).$(ext)))
target_readme=plots/Readme.md
targets=$(target_readme) $(targets_plots)

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
		*/dm32/*) VAR=dm32;;
		*/dm31/*) VAR=dm31;;
	esac
	case "$@" in
		*_dayabay*)   OPTS="$$OPTS --dayabay"                                   ;;&
		*_global*)    TYPE="$${TYPE#theor}"                                     ;;&
		*_future*)    TYPE="$${TYPE%estimation}"                                ;;&
		*_latest*)    SOURCE=plots/"$$VAR"_$(version)_"$$NMO"_latest.dat    ;;&
		*_published*) SOURCE=plots/"$$VAR"_$(version)_"$$NMO"_published.dat ;;&
	esac
	test "$${TYPE# }" && OPTS="$$OPTS -e $$TYPE"
	./$< $$SOURCE -v $$VAR $$OPTS -o $@

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
		*_NO_*)       NMO=NO                     ;;&
		*_IO_*)       NMO=IO                     ;;&
		*/dm32_*)     VAR=dm32                   ;;&
		*/dm31_*)     VAR=dm31                   ;;&
	esac
	./$< -v $$VAR \
	     -o $@ \
		 --nmo $$NMO \
		$$SOURCE



#
# Misc
#
.PHONY: debug-plot
debug-plot:
	$(script) plots/$(variable)_NO_$(version).dat -s --dayabay

debug:
	ipython --pdb -- \
		./maketable.py -v splitting_large \
					   -o plots/$(variable)_NO.dat \
					   --nmo NO \
					   $(data)

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

