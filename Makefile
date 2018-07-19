all: int

int:
	python src/main.py

test:
	python src/test_affichage.py

test_melody:
	python tst/test_monomelody.py

clean: 
	@rm -f src/*~ src/*.pyc 
