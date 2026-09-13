#!/bin/bash

# Build the published resume PDF from README.md.
# Skips package installs when pandoc and WeasyPrint are already available (CI).

set -euo pipefail

cd "$(dirname "$0")/.."

echo "Starting PDF build..."

have_weasyprint() {
    command -v weasyprint >/dev/null 2>&1
}

if ! command -v pandoc >/dev/null 2>&1 || ! have_weasyprint; then
    if ! command -v apt-get >/dev/null 2>&1; then
        echo "pandoc and weasyprint are required. Install them for your system, then retry."
        exit 1
    fi

    echo "Installing pandoc and WeasyPrint dependencies..."
    sudo apt-get update
    sudo apt-get install -y \
        pandoc \
        libgobject-2.0-0 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf-2.0-0 \
        libffi-dev \
        shared-mime-info \
        python3 \
        python3-pip

    if ! have_weasyprint; then
        if ! sudo apt-get install -y python3-weasyprint; then
            echo "System WeasyPrint package unavailable; installing with pip..."
            pip3 install weasyprint --break-system-packages
        fi
    fi
fi

if [ ! -f README.md ]; then
    echo "README.md not found"
    exit 1
fi

if [ -f style.css ]; then
    echo "Using style.css for PDF styling"
    CSS_ARG=(--css=style.css)
else
    echo "style.css not found; generating PDF without custom styling"
    CSS_ARG=()
fi

mkdir -p artifacts

echo "Generating PDF..."
pandoc README.md "${CSS_ARG[@]}" --output "artifacts/Mike Schock - Resume.pdf" --pdf-engine=weasyprint

if [ -f "artifacts/Mike Schock - Resume.pdf" ]; then
    echo "PDF generated: artifacts/Mike Schock - Resume.pdf ($(du -h 'artifacts/Mike Schock - Resume.pdf' | cut -f1))"
else
    echo "PDF generation failed"
    exit 1
fi
