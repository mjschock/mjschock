# Makefile for Mike Schock's Resume
# This Makefile provides convenient targets for building and managing the resume PDF

.PHONY: help build clean install-deps test all

# Default target
.DEFAULT_GOAL := help

# Variables
RESUME_SOURCE = README.md
RESUME_PDF = artifacts/Mike Schock - Resume.pdf
BUILD_SCRIPT = scripts/build-pdf.sh

help: ## Show this help message
	@echo "Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

build: $(RESUME_PDF) ## Build the resume PDF

$(RESUME_PDF): $(RESUME_SOURCE) $(BUILD_SCRIPT)
	@echo "🚀 Building resume PDF..."
	@$(BUILD_SCRIPT)
	@echo "✅ Resume PDF built successfully: $(RESUME_PDF)"

install-deps: ## Install system dependencies (requires sudo)
	@echo "📦 Installing system dependencies..."
	@sudo apt-get update
	@sudo apt-get install -y pandoc libgobject-2.0-0 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libffi-dev shared-mime-info python3 python3-pip
	@echo "🐍 Installing WeasyPrint..."
	@if ! apt-get install -y python3-weasyprint 2>/dev/null; then \
		echo "   System package not available, using pip with --break-system-packages..."; \
		pip3 install weasyprint --break-system-packages; \
	fi
	@echo "✅ Dependencies installed successfully"

clean: ## Remove generated files
	@echo "🧹 Cleaning up generated files..."
	@rm -f $(RESUME_PDF)
	@rm -rf artifacts/
	@echo "✅ Cleanup complete"

test: build ## Test the build process
	@echo "🧪 Testing build process..."
	@if [ -f "$(RESUME_PDF)" ]; then \
		echo "✅ Test passed: PDF generated successfully"; \
		echo "📊 File size: $$(du -h '$(RESUME_PDF)' | cut -f1)"; \
	else \
		echo "❌ Test failed: PDF not found"; \
		exit 1; \
	fi

all: clean build ## Clean and build everything

# Development targets
dev: build ## Build and open the PDF (if xdg-open is available)
	@if command -v xdg-open >/dev/null 2>&1; then \
		echo "📖 Opening PDF..."; \
		xdg-open "$(RESUME_PDF)"; \
	else \
		echo "📄 PDF generated: $(RESUME_PDF)"; \
		echo "   (Install xdg-utils to open PDF automatically)"; \
	fi

watch: ## Watch for changes and rebuild (requires entr)
	@echo "👀 Watching for changes in $(RESUME_SOURCE) and style.css..."
	@echo "   Press Ctrl+C to stop watching"
	@if command -v entr >/dev/null 2>&1; then \
		ls $(RESUME_SOURCE) style.css 2>/dev/null | entr -c make build; \
	else \
		echo "❌ entr not found. Install with: sudo apt-get install entr"; \
		exit 1; \
	fi

# Info target
info: ## Show build information
	@echo "Resume Build Information:"
	@echo "  Source file: $(RESUME_SOURCE)"
	@echo "  Output PDF:  $(RESUME_PDF)"
	@echo "  Build script: $(BUILD_SCRIPT)"
	@echo ""
	@echo "Dependencies:"
	@echo "  - pandoc"
	@echo "  - weasyprint"
	@echo "  - system libraries (libgobject, libpango, etc.)"
	@echo ""
	@echo "Usage:"
	@echo "  make build     - Build the resume PDF"
	@echo "  make clean     - Remove generated files"
	@echo "  make test      - Test the build process"
	@echo "  make help      - Show this help"
