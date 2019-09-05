zip:
	rm -rf snail
	rm -f snail.zip
	git clone https://github.com/pblottiere/snail
	rm -f snail/.gitignore
	rm -rf snail/.git
	rm -f snail/Makefile
	zip -r snail.zip snail
	rm -rf snail
