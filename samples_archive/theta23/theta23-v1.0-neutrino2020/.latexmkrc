$pdflatex = 'pdflatex -file-line-error -interaction=nonstopmode -synctex=1 %O %S';
$pdflatex = 'lualatex --file-line-error --interaction=nonstopmode --synctex=1 %O %S';
@default_files = ('theta13.tex');

$pdf_mode = 1;
