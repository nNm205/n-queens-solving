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

The Elsevier CAS template files are present in this directory, including `cas-sc.cls`, `cas-common.sty`, and `cas-model2-names.bst`. MiKTeX has been configured with a CTAN repository and the required CAS dependencies are installed in the current User-mode setup.

MiKTeX Console is configured to install missing packages on the fly. The manuscript source intentionally keeps `\documentclass[a4paper,fleqn]{cas-sc}` and should not be changed to a generic class for the final submission. The figures are generated as PDF files because `pdflatex` does not consume SVG directly.

The earlier draft was compiled successfully to `manuscript.pdf` on 10 October 2026. The manuscript source has since been revised with a repeated Pairwise cross-solver batch, so the existing PDF is stale and should not be used to review the new text. In the current shell, `pdflatex` and `bibtex` are not discoverable, so this revision has not yet been compiled. Rebuild the PDF after restoring MiKTeX's executable path, then review the remaining layout warnings.

The repository tracks only the CAS files required by this manuscript: `cas-sc.cls`, `cas-common.sty`, `cas-model2-names.bst`, and the CAS contact-icon thumbnails. Sample manuscripts, documentation sources, and generated build files are intentionally kept out of the project commit.

The draft uses the repeated Pairwise results in `results/pairwise_solver_comparison_repeat3.csv` and retains license-limited outcomes explicitly. The Gurobi and CPLEX MIP licenses still restrict larger instances, and CPLEX CP Optimizer was not discoverable during the repeated rerun. A matched five-method comparison remains to be run after the license and executable issues are resolved.
