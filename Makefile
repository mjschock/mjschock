dist:
	pandoc "data/RESUME.md" \
		--css=data/style.css \
		--pdf-engine=weasyprint \
		-o "assets/Resume - Michael James Schock.pdf"
