.PHONY: publish

publish:
	@echo "Reading current version..."
	@CURRENT_VERSION=$$(python -c "import tomli; print(tomli.load(open('pyproject.toml', 'rb'))['project']['version'])") && \
	echo "Current version: $$CURRENT_VERSION" && \
	MAJOR=$$(echo $$CURRENT_VERSION | cut -d. -f1) && \
	MINOR=$$(echo $$CURRENT_VERSION | cut -d. -f2) && \
	PATCH=$$(echo $$CURRENT_VERSION | cut -d. -f3) && \
	SUGGESTED_VERSION="$$MAJOR.$$MINOR.$$(( PATCH + 1 ))" && \
	echo "Suggested new version: $$SUGGESTED_VERSION" && \
	echo "Enter the new version (or press Enter to use suggested version):" && \
	read NEW_VERSION && \
	NEW_VERSION=$${NEW_VERSION:-$$SUGGESTED_VERSION} && \
	echo "Using version: $$NEW_VERSION" && \
	echo "Updating pyproject.toml..." && \
	sed -i.bak "s/version = \"$$CURRENT_VERSION\"/version = \"$$NEW_VERSION\"/" pyproject.toml && \
	rm pyproject.toml.bak && \
	echo "Cleaning dist directory..." && \
	rm -f dist/*.whl dist/*.tar.gz && \
	echo "Building package..." && \
	uv build && \
	echo "Please enter your PyPI token (input will be hidden):" && \
	stty -echo && \
	read PYPI_TOKEN && \
	stty echo && \
	echo "\nPublishing package..." && \
	uv publish --token "$$PYPI_TOKEN"
