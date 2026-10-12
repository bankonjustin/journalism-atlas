# Nodes and Networks preview: docx in, page out.
#   make -C tools/preview-build preview DOCX="/path/to/export.docx"
# DOCX is optional; when given it becomes the new "docx" in config.json.
# Steps: parse -> build page -> build-dist.sh (what Cloudflare serves) -> Playwright checks.

PY ?= python3
REPO := $(abspath ../..)

.PHONY: preview parse page dist validate

preview: parse page dist validate
	@echo; echo "Review: git diff -- tools/preview-build/content/content.md"

parse:
ifdef DOCX
	$(PY) -c "import json,sys; p=\"config.json\"; c=json.load(open(p)); c[\"docx\"]=sys.argv[1]; open(p,\"w\").write(json.dumps(c,indent=2,ensure_ascii=False)+\"\\n\")" "$(DOCX)"
endif
	$(PY) parse_docx.py

page:
	$(PY) build_page.py

dist:
	cd "$(REPO)" && sh build-dist.sh

validate:
	$(PY) validate.py
