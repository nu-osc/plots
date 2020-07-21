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
					  data/*.yaml 

clean:
	latexmk -C theta13.tex
