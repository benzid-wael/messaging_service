

clean:
	find -name '*.pyc' -delete
	find -name '*~' -delete

test:
	python runtests.py -v
