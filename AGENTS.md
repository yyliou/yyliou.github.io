## Imported Claude Cowork project instructions

## Render notes (for Claude sessions)
- Site: Quarto 1.9.38 (`quarto render`). Quarto cannot run on the mounted folder inside the device shell (sqlite "disk I/O error", temp dirs cannot be removed) — render in the cloud container instead: stage `_quarto.yml`, `_header.html`, `_footer.html`, `styles.css`, `pic.png` and the `.qmd` files, run `quarto render`, then commit back only the changed `.html`, `search.json` and `sitemap.xml`. Unchanged pages reproduce byte-for-byte.
- CV: sources live in the sibling repo `../yyliou/cv/*.Rmd` (8 variants) and are built with `Rscript render.R` (rmarkdown → xelatex, template `jenpan-latex-cv.tex`). Needs R + rmarkdown + xeCJK (texlive-lang-chinese) + TeX Gyre Pagella + the 源雲明體月 (GenWanMin2TW) fonts from `fonts/`. Paper titles appear in both the site (`research*.qmd`) and all 8 CV files — change all of them together.
- Git on the mounted folder: use `git --no-optional-locks status`; plain `git status` leaves a `.git/index.lock` that cannot be deleted from the device shell (move it to `_to_delete/` if it happens).
