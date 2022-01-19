# This is a Makefile to run different commands, different integrations' test cases


###################
# Generic targets #
###################

# test targets
expecto:
	@echo patronum


#ping:
#    @echo PONG $(NOW) $(FOO)


#ping2: FOO=oof
#ping2: NOW:=$(shell date +'%Y%m%d_%H%M')
#ping2: ping
#    @echo PONG2 $(NOW) $(FOO)


# assuming venv is activated
env:
	pip install -r requirements.txt


# install more packages required for development
devenv: env
	pip install -r requirements-dev.txt


flake8:
	git diff --unified=0 origin/main..HEAD | flake8 \
		--count \
		--diff \
		--statistics \
		--tee \
		--doctests \
		--benchmark \
		--import-order-style google \
		--docstring-convention google


test:
	pytest \
	--cov . \
	--cov-report term-missing \
	--cov-branch \
	-vvv \
	-rA \
	tests/

run:
	ZATTOO_HTTP_BEARER_TOKEN=expectopatronum python run.py
