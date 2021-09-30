variable = theta23
version_num = 2.0
suffix   = neutrino2020
beta = b
version_prev = 1.0
version_dash = $(subst .,-,${version_num})
version  = v${version_dash}${beta}

.PHONY: all table debug clean clean-all publish
.SUFFIXES: .tex .dat .pdf .png .yaml

publishdir = ../../../plots/$(variable)/${variable}-${version_num}-${suffix}
scripts    = *.py pylib/*.py
script     = ./$(variable).py
data       = $(shell realpath $(wildcard data/*.yaml))
table_NO   = plots/$(variable)_NO_$(version).dat
table_IO   = plots/$(variable)_IO_$(version).dat
tables     = $(table_NO) $(table_IO)
targets_NO = $(table_NO:%.dat=%.png) $(table_NO:%.dat=%.pdf)
targets_IO = $(table_IO:%.dat=%.png) $(table_IO:%.dat=%.pdf)
targets_NO_future = $(table_NO:%.dat=%_future.png) $(table_NO:%.dat=%_future.pdf)
targets_IO_future = $(table_IO:%.dat=%_future.png) $(table_IO:%.dat=%_future.pdf)
targets    = $(targets_NO) $(targets_IO) $(targets_NO_future) $(targets_IO_future) plots/Readme.md

.PRECIOUS: %.tex %.dat %.pdf %.png $(tables) $(targets)

all: $(targets) | plots

plots:
	test -d plots || mkdir plots

plots/Readme.md: Readme.md Makefile | plots
	cat $< | version_num=${version_num} beta=${beta} version_dash=${version_dash} version_prev=${version_prev} envsubst > $@

#define plot = 
	#$(script) $< -o $@
#endef

plots/$(variable)_%_$(version).png: plots/$(variable)_%_$(version).dat $(script) | plots
	$(script) $< -o $@ -e estimation

plots/$(variable)_%_$(version).pdf: plots/$(variable)_%_$(version).dat $(script) | plots
	$(script) $< -o $@ -e estimation

plots/$(variable)_%_$(version)_future.png: plots/$(variable)_%_$(version).dat $(script) | plots
	$(script) $< -o $@ 

plots/$(variable)_%_$(version)_future.pdf: plots/$(variable)_%_$(version).dat $(script) | plots
	$(script) $< -o $@ 

table: $(tables)

$(tables): $(scripts) $(data) | plots
	./maketable.py -v $(variable) \
	               -o $@ \
				   $(filter %.yaml,$^)

debug-plot:
	ipython --pdb -- $(script) -s $(table_NO) --nmo NO

print-%:
	@echo '$*=$($*)'

clean-all:
	rm plots/*.pdf plots/*.png

publish: $(targets) | plots
	test -d $(publishdir) || mkdir -p $(publishdir)
	cp -v plots/* $(publishdir)/
