#include docker/.env

BUILD_PRINT = \e[1;34mSTEP: \e[0m

#-----------------------------------------------------------------------------
# Install dev environment
#-----------------------------------------------------------------------------

install:
	@ echo "$(BUILD_PRINT)Installing the requirements"
	@ pip install --upgrade pip
	@ pip install -r requirements.txt

#-----------------------------------------------------------------------------
# Test commands
#-----------------------------------------------------------------------------

test:
	@ echo "$(BUILD_PRINT)Running the tests"
	@ cd tests/unit && pytest

#-----------------------------------------------------------------------------
# Generator commands
#-----------------------------------------------------------------------------
# example: make generate_queries ap=skos_core.csv
# the csv file needs to exist in the resource/aps folder
generate_queries:
	@ python -m dqgen.entrypoints.cli.generate_queries $(ap)

#-----------------------------------------------------------------------------
# Generator commands
#-----------------------------------------------------------------------------
# example: make generate_html_templates ap=skos_core.csv
# the csv file needs to exist in the resource/aps folder
generate_html_templates:
	@ python -m dqgen.entrypoints.cli.generate_html_template $(ap)