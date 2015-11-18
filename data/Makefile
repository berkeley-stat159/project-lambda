data:
	wget https://googledrive.com/host/0Byvo26QiFSvZTGJDRmd1eHZlR2c/raw.tgz
	tar -xf raw.tgz

validate:
	python data.py

README.pdf: README.md
	pandoc -o README.pdf README.md
