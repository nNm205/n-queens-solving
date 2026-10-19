# Report workspace

The first English manuscript draft is in `manuscript.tex` and follows the Elsevier `cas-sc` document class requested for the assignment. References are in `references.bib`.

## Local compilation

From this directory, run:

```powershell
pdflatex -interaction=nonstopmode manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

The Elsevier CAS template files are present in this directory, including `cas-sc.cls`, `cas-common.sty`, and `cas-model2-names.bst`. MiKTeX 25.12 is installed at `E:\Apps\MiKTeX`; `pdflatex.exe` and `bibtex.exe` are in `E:\Apps\MiKTeX\miktex\bin\x64`, and this directory is present in the user PATH. Terminals opened before the PATH update must be restarted.

MiKTeX Console is configured to install missing packages on the fly. The manuscript source intentionally keeps `\documentclass[a4paper,fleqn]{cas-sc}` and should not be changed to a generic class for the final submission. The figures are generated as PDF files because `pdflatex` does not consume SVG directly.

The current manuscript was compiled to `manuscript.pdf` on 19 October 2026 using pdfLaTeX, BibTeX, and two final pdfLaTeX passes. The seven-page PDF reports the latest complete SAT-encoding and matched five-method benchmark reruns. Citations render in author-year format, and the custom PDF chart writer uses valid PDF drawing operators and visible text. The log retains one `\maketitle` overfull-box warning and empty-anchor warnings from the CAS front matter; no citation, bibliography, or figure parse errors remain.

The repository tracks only the CAS files required by this manuscript: `cas-sc.cls`, `cas-common.sty`, `cas-model2-names.bst`, and the CAS contact-icon thumbnails. Sample manuscripts, documentation sources, and generated build files are intentionally kept out of the project commit.

The draft uses the latest matched five-method results in `results/solver_comparison_matched_n8-128_repeat3.csv`. All solvers solve every tested size through `N = 128`; all 150 matched runs and 54 SAT-encoding runs have validated solutions with no license-limit, timeout, or error outcomes. The matched batch was rerun in full after academic license activation.
