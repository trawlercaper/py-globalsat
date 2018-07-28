lock:
	pipenv lock

install:
	make lock && pipenv install --dev
