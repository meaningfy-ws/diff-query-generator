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
	@ pytest

#-----------------------------------------------------------------------------
# Generator commands
#-----------------------------------------------------------------------------
# example: make generate_queries ap=dqgen/resources/aps/owl-core.csv output=./output
generate_queries:
	@ python -m dqgen.entrypoints.cli.generate_queries $(ap) $(output)

#-----------------------------------------------------------------------------
# Generator commands
#-----------------------------------------------------------------------------
# example: make generate_html_templates ap=dqgen/resources/aps/owl-core.csv output=./output
generate_html_templates:
	@ python -m dqgen.entrypoints.cli.generate_html_template $(ap) $(output)
