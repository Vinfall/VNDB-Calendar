# Varables
VENV = .venv
# PYTHON = $(VENV)/bin/python
# PIP = $(VENV)/bin/pip
PYTHON = python
PIP = pip

# Dependencies & scripts
REQUIREMENTS = requirements.txt
GENERATOR = vndb_calendar.py

install: $(VENV) ## install dependencies in venv
	$(PIP) install -r $(REQUIREMENTS)

$(VENV):
	@echo "Setting up virtualenv..."
	virtualenv $(VENV)
	source $(VENV)/bin/activate; \
	$(PIP) install -r $(REQUIREMENTS)

run: ## build my custom calendar
	$(PYTHON) ${GENERATOR}

en: ## build VNDB calendar with en & ja releases
	$(PYTHON) ${GENERATOR} -f "0572171_4YsVe122gen2gjaN48721gwcomplete-" -t 0 -d 1

zh: ## build VNDB calendar with zh-Hans/zh-Hant & ja releases
	$(PYTHON) ${GENERATOR} -f "0572171_4YsVe132gja2wzh_dHans-2wzh_dHant-N48721gwcomplete-" -t 0 -d 1

clean: ## clean up outputs
	-rm output/*

uninstall: ## uninstall venv & clean cache
	@echo "Cleaning up..."
	@deactivate || true
	rm -rf $(VENV)
	pip cache purge || true

help: ## show this help
	@echo "Specify a command:"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-12s\033[m %s\n", $$1, $$2}'
	@echo ""
.PHONY: help
