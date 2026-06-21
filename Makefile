#include docker/.env

BUILD_PRINT = \e[1;34mSTEP: \e[0m
DEFAULT_OUTPUT := ./output
APS_DIR := dqgen/resources/aps
# Always generate for ALL application profiles discovered under APS_DIR.
ALL_APS := $(patsubst %.csv,%,$(notdir $(wildcard $(APS_DIR)/*.csv)))
# Template variants dqgen renders into the rdf-differ bundle.
BUNDLE_VARIANTS := html asciidoc
# Static (profile-independent) json variant shipped as a resource and copied verbatim.
JSON_VARIANT_SRC := dqgen/resources/rdf_differ_bundle/json

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
# Batch generation for ALL profiles (flat layout: <output>/<ap>/{queries,html,asciidoc})
#-----------------------------------------------------------------------------
# Usage: make generate_all_profiles_templates output=./output
generate_all_profiles_templates:
	@ set -e; out=$(if $(output),$(output),$(DEFAULT_OUTPUT)); \
	echo "==> Generating all templates for: $(ALL_APS)"; \
	for profile in $(ALL_APS); do \
		ap_path=$(APS_DIR)/$${profile}.csv; \
		echo "$(BUILD_PRINT)$$profile: queries"; python -m dqgen.entrypoints.cli.generate_queries $$ap_path $$out; \
		echo "$(BUILD_PRINT)$$profile: html";    python -m dqgen.entrypoints.cli.generate_html_template $$ap_path $$out; \
		echo "$(BUILD_PRINT)$$profile: asciidoc";python -m dqgen.entrypoints.cli.generate_asciidoc_template $$ap_path $$out; \
	done

#-----------------------------------------------------------------------------
# rdf-differ bundles: for ALL profiles, emit the rdf-differ folder layout so the
# per-profile folders can be copy/pasted into rdf-differ resources/templates/.
#   <output>/<ap>/queries/
#   <output>/<ap>/template_variants/<variant>/{config.json,templates/}
#-----------------------------------------------------------------------------
# Usage: make generate_rdf_differ_bundles output=./output
generate_rdf_differ_bundles:
	@ set -e; out=$(if $(output),$(output),$(DEFAULT_OUTPUT)); \
	echo "==> Generating rdf-differ bundles for: $(ALL_APS) into $$out"; \
	for ap in $(ALL_APS); do \
		ap_path=$(APS_DIR)/$$ap.csv; \
		echo "$(BUILD_PRINT)$$ap: queries"; python -m dqgen.entrypoints.cli.generate_queries $$ap_path $$out; \
		echo "$(BUILD_PRINT)$$ap: html";    python -m dqgen.entrypoints.cli.generate_html_template $$ap_path $$out; \
		echo "$(BUILD_PRINT)$$ap: asciidoc";python -m dqgen.entrypoints.cli.generate_asciidoc_template $$ap_path $$out; \
		test -d $$out/$$ap/queries || { echo "ERROR: $$out/$$ap/queries missing - generation failed (check python env)"; exit 1; }; \
		for v in $(BUNDLE_VARIANTS); do \
			test -d $$out/$$ap/$$v || { echo "ERROR: $$out/$$ap/$$v missing - $$v generation failed"; exit 1; }; \
			mkdir -p $$out/$$ap/template_variants/$$v; \
			rm -rf $$out/$$ap/template_variants/$$v/templates; \
			mv $$out/$$ap/$$v $$out/$$ap/template_variants/$$v/templates; \
			tmpl=main.html; [ "$$v" = asciidoc ] && tmpl=main.adoc; \
			printf '{\n    "template": "%s",\n    "conf":\n    {\n        "default_endpoint": "http://localhost:3030/dataset_test/sparql",\n        "title": "RDF Diff report",\n        "type": "report",\n        "author": "Meaningfy",\n        "ns_file": "data/prefix.csv",\n        "query_folder_path": "resources/templates/%s/queries/"\n    }\n}\n' "$$tmpl" "$$ap" > $$out/$$ap/template_variants/$$v/config.json; \
		done; \
		rm -rf $$out/$$ap/template_variants/json; \
		mkdir -p $$out/$$ap/template_variants/json; \
		cp -r $(JSON_VARIANT_SRC)/. $$out/$$ap/template_variants/json/; \
		echo "$(BUILD_PRINT)$$ap: bundled -> $$out/$$ap"; \
	done

clean:
	@ echo "$(BUILD_PRINT)Cleaning up generated files"
	@ rm -rf $(DEFAULT_OUTPUT)/*
