.PHONY: all clean progress.pdf final.pdf

all: clean progress.pdf final.pdf

clean:
	rm -f progress.pdf final.pdf

progress.pdf: progress.md
	pandoc -t beamer -s progress.md -o progress.pdf


final.pdf: final.md
	pandoc -t beamer -s final.md -o final.pdf
