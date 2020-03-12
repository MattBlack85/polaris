PIPENV_RUN = pipenv run

.PHONY: bootstrap \
	cheeseshop \
	get-latest \
	nuke-venv \

bootstrap: nuke-venv cheeseshop

cheeseshop:
	@pipenv install --dev

get-latest:
	@$(PIPENV_RUN) python polariscv.py

nuke-venv:
	@pipenv --rm;\
	EXIT_CODE=$$?;\
	if [ $$EXIT_CODE -eq 1 ]; then\
		echo Skipping virtualenv removal;\
	fi
