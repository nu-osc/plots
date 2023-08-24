$pdflatex = 'pdflatex -file-line-error -interaction=nonstopmode -synctex=1 %O %S';
$pdflatex = 'lualatex --file-line-error --interaction=nonstopmode --synctex=1 %O %S';
@default_files = ('dm32_NO.tex', 'dm32_IO.tex');

$pdf_mode = 1;
