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

The current MiKTeX installation does not contain `cas-sc.cls`, so compilation is currently blocked until the Elsevier CAS template/class is installed or copied into this directory. The manuscript source intentionally keeps `\documentclass[a4paper,fleqn]{cas-sc}` and should not be changed to a generic class for the final submission.

The draft uses the current local pilot results. Results that depend on academic licenses are explicitly marked as limitations and should be refreshed after the licenses are activated.
