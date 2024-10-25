dist:
	pandoc "data/RESUME.md" \
		--css=data/style.css \
		--pdf-engine=weasyprint \
		--output "assets/Resume - Michael James Schock.pdf"

swe_agent_run:
	. .venv/bin/activate && \
	cd swe_agent/agent && \
	python main.py
