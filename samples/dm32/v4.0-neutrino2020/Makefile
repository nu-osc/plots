.PHONY: all place table

all: place

place: plots/dm32_NO_v4-0.pdf plots/dm32_NO_v4-0.png plots/dm32_IO_v4-0.pdf plots/dm32_IO_v4-0.png

plots/dm32_NO_v4-0.pdf plots/dm32_NO_v4-0.png: dm32_NO.pdf
	cp dm32_NO.pdf plots/dm32_NO_v4-0.pdf
	convert -density 300 plots/dm32_NO_v4-0.pdf plots/dm32_NO_v4-0.png

plots/dm32_IO_v4-0.pdf plots/dm32_IO_v4-0.png: dm32_IO.pdf
	cp dm32_IO.pdf plots/dm32_IO_v4-0.pdf
	convert -density 300 plots/dm32_IO_v4-0.pdf plots/dm32_IO_v4-0.png

dm32_NO.pdf: dm32_NO.dat dm32_NO.tex
	latexmk dm32_NO.tex

dm32_IO.pdf: dm32_IO.dat dm32_IO.tex
	latexmk dm32_IO.tex

table: dm32_NO.dat dm32_IO.dat

dm32_NO.dat dm32_IO.dat: maketable.py
	./maketable.py -v splitting_large \
	               -o dm32_NO.dat \
		           --nmo NO \
				   data/*.yaml
	./maketable.py -v splitting_large \
		           -o dm32_IO.dat \
		           --nmo IO \
				   data/*.yaml

clean:
	latexmk -C dm32_NO.tex dm32_IO.tex
