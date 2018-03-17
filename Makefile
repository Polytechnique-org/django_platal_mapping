PIP ?= pip
PYTHON ?= python
RM ?= rm -f

all:
	$(PYTHON) manage.py migrate --noinput
	$(PYTHON) manage.py populate_db
	$(PYTHON) manage.py fake_email_accounts

install-deps:
	$(PIP) install -r requirements.txt

shell:
	$(PYTHON) manage.py shell

clean:
	$(RM) db.sqlite

.PHONY: all clean install-deps
