data:
	for i in 1 2; do \
		for j in 1 2 3 4 5 6 7 8; do \
    		wget -O 'raw/sub'$$i'_run'$$j'_raw.nii.gz' https://nipy.bic.berkeley.edu/rcsds/ds113/sub00$$i/BOLD/task001_run00$$j/bold_dico_dico7Tad2grpbold7Tad_nl.nii.gz ;\
		done \
	done
	gzip -d raw/*.gz

validate:
	python data.py

README.pdf: README.md
	pandoc -o README.pdf README.md
