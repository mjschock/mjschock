deploy:
	cd mjschock && \
	fly deploy

dist:
	pandoc "data/RESUME.md" \
		--css=data/style.css \
		--output "assets/Resume - Michael James Schock.pdf" \
		--pdf-engine=weasyprint

	pandoc "data/RESUME.md" \
		--output "assets/Resume - Michael James Schock.docx" \
		--reference-doc=data/custom-reference.docx
	
	pandoc "data/RESUME.md" \
		--output "assets/Resume - Michael James Schock.html" \
		--css=data/style.css

reference_doc:
	pandoc -o data/custom-reference.docx --print-default-data-file reference.docx

swe_agent_run:
	. .venv/bin/activate && \
	cd swe_agent/agent && \
	python main.py
