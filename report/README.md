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

The Elsevier CAS template files are now present in this directory, including `cas-sc.cls`, `cas-common.sty`, and `cas-model2-names.bst`. The current MiKTeX installation is minimal and still needs dependencies used by `cas-common.sty`, such as `makecell`, `multirow`, `xstring`, `footmisc`, `stfloats`, `moreverb`, and `wrapfig`.

In MiKTeX Console, enable automatic installation of missing packages (`Always install missing packages on-the-fly`), then run the compilation commands again. The manuscript source intentionally keeps `\documentclass[a4paper,fleqn]{cas-sc}` and should not be changed to a generic class for the final submission.

The draft uses the current local pilot results. Results that depend on academic licenses are explicitly marked as limitations and should be refreshed after the licenses are activated.
