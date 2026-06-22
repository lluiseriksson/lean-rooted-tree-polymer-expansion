.PHONY: all clean check

all: main.pdf graphical-abstract-final.pdf graphical-abstract.png

main.pdf: main.tex references.bib
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

graphical-abstract-final.pdf: graphical-abstract.tex
	pdflatex -interaction=nonstopmode -halt-on-error graphical-abstract.tex
	cp graphical-abstract.pdf graphical-abstract-final.pdf

graphical-abstract.png: graphical-abstract-final.pdf
	pdftoppm -png -singlefile -r 130 graphical-abstract-final.pdf graphical-abstract

check: all
	pdffonts main.pdf
	pdfinfo main.pdf

clean:
	latexmk -C main.tex
	latexmk -C graphical-abstract.tex
	rm -f main.bbl main.blg main.run.xml main.synctex.gz graphical-abstract-final.pdf graphical-abstract.png
