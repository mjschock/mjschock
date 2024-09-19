dist:
	pandoc "data/RESUME.md" \
		--css=data/style.css \
		--pdf-engine=weasyprint \
		--output "assets/Resume - Michael James Schock.pdf"

	# pandoc "data/RESUME.md" \
	# 	--css=data/style.css \
	# 	--pdf-engine=weasyprint \
	# 	--output "assets/Resume - Michael James Schock.ipynb"

	# jupyter nbconvert --allow-chromium-download --to webpdf "assets/Resume - Michael James Schock.ipynb"
	# jupyter nbconvert --to html "assets/Resume - Michael James Schock.ipynb"
	# jupyter nbconvert --to latex "assets/Resume - Michael James Schock.ipynb"
	# jupyter nbconvert --to markdown "assets/Resume - Michael James Schock.ipynb"

	# # pandoc "data/RESUME.md" \
	# # 	--css=data/style.css \
	# # 	--pdf-engine=weasyprint \
	# # 	--output "assets/Resume - Michael James Schock.pdf"

	# # pandoc "assets/Resume - Michael James Schock.ipynb" \
	# # 	--output="assets/Resume - Michael James Schock.docx"

	# # pandoc "assets/Resume - Michael James Schock.ipynb" \
	# # 	--pdf-engine=weasyprint \
	# # 	--output="assets/Resume - Michael James Schock.pdf"

	# # pandoc "data/RESUME.md" \
	# # 	--css=data/style.css \
	# # 	--pdf-engine=weasyprint \
	# # 	--pdf-engine-opt=--pdf-variant=pdf/ua-1 \
	# # 	--output "assets/Resume - Michael James Schock.pdf"

	# # pandoc "data/RESUME.md" \
	# # 	--css=data/style.css \
	# # 	--read=markdown \
	# # 	--output "assets/Resume - Michael James Schock.html" \
	# # 	--pdf-engine=weasyprint \
	# # 	--write=html

	# # pandoc "assets/Resume - Michael James Schock.html" \
	# # 	--css=data/style.css \
	# # 	--read=html \
	# # 	--output="assets/Resume - Michael James Schock.docx" \
	# # 	--write=docx

	# # pandoc "assets/Resume - Michael James Schock.html" \
	# # 	--css=data/style.css \
	# # 	--read=html \
	# # 	--output="assets/Resume - Michael James Schock.pdf" \
	# # 	--pdf-engine=weasyprint \
	# # 	--write=pdf
