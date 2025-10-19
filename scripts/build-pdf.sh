#!/bin/bash

# Build PDF from Markdown README
# This script installs necessary dependencies and generates a PDF from README.md

set -e  # Exit on any error

echo "🚀 Starting PDF build process..."

# Check if we're on Ubuntu/Debian
if ! command -v apt-get &> /dev/null; then
    echo "❌ This script is designed for Ubuntu/Debian systems with apt-get"
    echo "   Please install pandoc and weasyprint manually for your system"
    exit 1
fi

# Update package list
echo "📦 Updating package list..."
sudo apt-get update

# Install pandoc
echo "📝 Installing pandoc..."
sudo apt-get install -y pandoc

# Install system dependencies for WeasyPrint
echo "🔧 Installing system dependencies for WeasyPrint..."
sudo apt-get install -y \
    libgobject-2.0-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    python3 \
    python3-pip

# Install WeasyPrint
echo "🐍 Installing WeasyPrint..."
# Try system package first, then fall back to pip with --break-system-packages
if ! apt-get install -y python3-weasyprint 2>/dev/null; then
    echo "   System package not available, using pip with --break-system-packages..."
    pip3 install weasyprint --break-system-packages
fi

# Check if README.md exists
if [ ! -f "README.md" ]; then
    echo "❌ README.md not found in current directory"
    echo "   Please run this script from the directory containing README.md"
    exit 1
fi

# Check if style.css exists
if [ ! -f "style.css" ]; then
    echo "⚠️  style.css not found, generating PDF without custom styling"
    CSS_ARG=""
else
    echo "🎨 Using style.css for PDF styling"
    CSS_ARG="--css=style.css"
fi

# Create artifacts directory if it doesn't exist
mkdir -p artifacts

# Generate PDF
echo "📄 Generating PDF..."
pandoc "README.md" $CSS_ARG --output "artifacts/Mike Schock - Resume.pdf" --pdf-engine=weasyprint

# Check if PDF was created successfully
if [ -f "artifacts/Mike Schock - Resume.pdf" ]; then
    echo "✅ PDF generated successfully: artifacts/Mike Schock - Resume.pdf"
    echo "📊 File size: $(du -h 'artifacts/Mike Schock - Resume.pdf' | cut -f1)"
else
    echo "❌ PDF generation failed"
    exit 1
fi

echo "🎉 Build complete!"
