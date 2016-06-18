.PHONY: deploy run test clean

run:
	python app.py

clean:
	rm *.pyc -f
