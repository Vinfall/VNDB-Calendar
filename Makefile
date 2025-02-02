# Varables
GENERATOR = vndb_calendar.py

run: ## build my custom calendar
	uv run ${GENERATOR}

en: ## build VNDB calendar with en & ja releases
	uv run ${GENERATOR} -f "0572171_4YsVe122gen2gjaN48721gwcomplete-" -t 0 -d 1

zh: ## build VNDB calendar with zh-Hans/zh-Hant & ja releases
	uv run ${GENERATOR} -f "0572171_4YsVe132gja2wzh_dHans-2wzh_dHant-N48721gwcomplete-" -t 0 -d 1

clean: ## clean up outputs
	-rm output/*

## generate changelog (only run after git tag)
changelog:
	git cliff -o CHANGELOG.md
	git add CHANGELOG.md
	git commit -m 'chore: update changelog'

help: ## show this help
	@echo "Specify a command:"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-12s\033[m %s\n", $$1, $$2}'
	@echo ""
.PHONY: help
