.PHONY: all place table

all: place

place: plots/theta13_v4-0.pdf plots/theta13_v4-0.png

plots/theta13_v4-0.pdf plots/theta13_v4-0.png: theta13.pdf
	cp theta13.pdf plots/theta13_v4-0.pdf
	convert -density 300 plots/theta13_v4-0.pdf plots/theta13_v4-0.png

theta13.pdf: theta13.dat theta13.tex
	latexmk theta13.tex

table: theta13.dat

theta13.dat:
	./maketable.py -o theta13.dat \
					  data/dayabay_2016-07-neutrino2016.yaml \
					  data/dayabay_2018-06-neutrino2018.yaml \
					  data/reno_2018-06-neutrino2018.yaml \
					  data/reno_2020-06-neutrino2020.yaml \
					  data/dchooz_2020-06-neutrino2020.yaml \
					  data/t2k_2020-06-neutrino2020.yaml

clean:
	latexmk -C theta13.tex
