variable = dm32
version_num = 5.0
suffix   = neutrino2020
beta = b
version_prev = 4.1
version_dash = $(subst .,-,${version_num})
version  = v${version_dash}${beta}

.PHONY: all table debug debug-plot clean clean-all publish
.SUFFIXES: .tex .dat .pdf .png .yaml

publishdir = ../../../plots/$(variable)/${variable}-${version_num}-${suffix}
scripts    = *.py pylib/*.py
script     = ./$(variable).py
data       = $(shell realpath $(wildcard data/*.yaml))

#
# Name combinations
#
name_no               = $(variable)_NO_$(version)
name_io               = $(variable)_IO_$(version)
names_0               = $(name_no) $(name_io)
name_global_no        = $(variable)_NO_global_$(version)
name_global_io        = $(variable)_IO_global_$(version)
names_global          = $(name_global_no) $(name_global_io)
name_global_future_no = $(variable)_NO_global_future_$(version)
name_global_future_io = $(variable)_IO_global_future_$(version)
names_global_future   = $(name_global_future_no) $(name_global_future_io)
name_dayabay_no       = $(variable)_NO_dayabay_$(version)
name_dayabay_io       = $(variable)_IO_dayabay_$(version)
names_dayabay         = $(name_dayabay_no) $(name_dayabay_io)
names                 = $(names_1) $(names_global) $(names_global_future) $(names_dayabay)
# Extensions
extensions   = pdf png

#
# Targets
#
table_no              = plots/$(name_no).dat
table_io              = plots/$(name_io).dat
tables                = $(table_no) $(table_io)
targets_0             = $(foreach n,$(names_0),$(foreach ext,$(extensions),plots/$(n).$(ext)))
targets_global        = $(foreach n,$(names_global),$(foreach ext,$(extensions),plots/$(n).$(ext)))
targets_global_future = $(foreach n,$(names_global_future),$(foreach ext,$(extensions),plots/$(n).$(ext)))
targets_dayabay       = $(foreach n,$(names_dayabay),$(foreach ext,$(extensions),plots/$(n).$(ext)))
targets               = $(targets_0) $(targets_global) $(targets_dayabay) $(targets_global_future) plots/Readme.md

.PRECIOUS: $(tables) $(targets)

#
# Recipes
#

all: $(targets) | plots

plots:
	test -d plots || mkdir plots

plots/Readme.md: Readme.md Makefile | plots
	cat $< | version_num=${version_num} beta=${beta} version_dash=${version_dash} version_prev=${version_prev} envsubst > $@

plots/$(variable)_NO_$(version).pdf plots/$(variable)_NO_$(version).png: plots/$(variable)_NO_$(version).dat $(script) | plots
	$(script) $< -o $@ -e theor estimation

plots/$(variable)_IO_$(version).pdf plots/$(variable)_IO_$(version).png: plots/$(variable)_IO_$(version).dat $(script) | plots
	$(script) $< -o $@ -e theor estimation

plots/$(variable)_NO_global_$(version).pdf plots/$(variable)_NO_global_$(version).png: plots/$(variable)_NO_$(version).dat $(script) | plots
	$(script) $< -o $@ -e estimation

plots/$(variable)_IO_global_$(version).pdf plots/$(variable)_IO_global_$(version).png: plots/$(variable)_IO_$(version).dat $(script) | plots
	$(script) $< -o $@ -e estimation

plots/$(variable)_NO_global_future_$(version).pdf plots/$(variable)_NO_global_future_$(version).png: plots/$(variable)_NO_$(version).dat $(script) | plots
	$(script) $< -o $@

plots/$(variable)_IO_global_future_$(version).pdf plots/$(variable)_IO_global_future_$(version).png: plots/$(variable)_IO_$(version).dat $(script) | plots
	$(script) $< -o $@

plots/$(variable)_NO_dayabay_$(version).pdf plots/$(variable)_NO_dayabay_$(version).png: plots/$(variable)_NO_$(version).dat $(script) | plots
	$(script) $< -o $@ -e theor estimation --dayabay

plots/$(variable)_IO_dayabay_$(version).pdf plots/$(variable)_IO_dayabay_$(version).png: plots/$(variable)_IO_$(version).dat $(script) | plots
	$(script) $< -o $@ -e theor estimation --dayabay

table: $(table)

$(table_no): $(scripts) $(data)
	./maketable.py -v splitting_large \
	               -o $@ \
		           --nmo NO \
				   $(filter %.yaml,$^)

$(table_io): $(scripts) $(data)
	./maketable.py -v splitting_large \
		           -o $@ \
		           --nmo IO \
				   $(filter %.yaml,$^)

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

clean-all: clean
	rm plots/*.pdf plots/*.png

publish: $(targets) | plots
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp -v plots/* $(publishdir)/
