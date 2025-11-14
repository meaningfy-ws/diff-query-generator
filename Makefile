#include docker/.env

BUILD_PRINT = \e[1;34mSTEP: \e[0m
PREFERRED_PROFILES := owl-core shacl-core skos-core
DEFAULT_OUTPUT := ./output

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

#-----------------------------------------------------------------------------
# Generator commands
#-----------------------------------------------------------------------------
# example: make generate_asciidoc_templates ap=dqgen/resources/aps/owl-core.csv output=./output
generate_asciidoc_templates:
	@ python -m dqgen.entrypoints.cli.generate_asciidoc_template $(ap) $(output)

#-----------------------------------------------------------------------------
# Batch generation for multiple profiles
#-----------------------------------------------------------------------------
# Usage: make generate_all PREFERRED_PROFILES="owl-core another-profile" output=./output

generate_all_profiles_templates:
	@ echo "==> Generating all templates for profiles $(PREFERRED_PROFILES)"
	@ for profile in $(PREFERRED_PROFILES); do \
		echo "--> profile: $$profile"; \
		ap_path=dqgen/resources/aps/$${profile}.csv; \
		echo "$(BUILD_PRINT)Generating queries for $$ap_path"; \
		python -m dqgen.entrypoints.cli.generate_queries $$ap_path $(DEFAULT_OUTPUT); \
		echo "$(BUILD_PRINT)Generating HTML templates for $$ap_path"; \
		python -m dqgen.entrypoints.cli.generate_html_template $$ap_path $(DEFAULT_OUTPUT); \
		echo "$(BUILD_PRINT)Generating AsciiDoc templates for $$ap_path"; \
		python -m dqgen.entrypoints.cli.generate_asciidoc_template $$ap_path $(DEFAULT_OUTPUT); \
	done

clean:
	@ echo "$(BUILD_PRINT)Cleaning up generated files"
	@ rm -rf $(DEFAULT_OUTPUT)/*
