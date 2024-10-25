dist:
	pandoc "data/RESUME.md" \
		--css=data/style.css \
		--pdf-engine=weasyprint \
		--output "assets/Resume - Michael James Schock.pdf"
