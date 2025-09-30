# How to Compile the LaTeX Documents

## Option 1: Online (Easiest - No Installation Required)

### Using Overleaf (Recommended)
1. Go to https://www.overleaf.com/
2. Create free account
3. Click "New Project" → "Upload Project"
4. Upload `findings_report.tex`
5. Click "Recompile"
6. Download PDF

**Advantage:** No installation, renders immediately, easy to share

---

## Option 2: Local Installation

### Windows
1. Install MiKTeX: https://miktex.org/download
2. Open terminal in `docs/latex/` directory
3. Run:
```bash
pdflatex findings_report.tex
pdflatex findings_report.tex  # Run twice for references
```

### Mac
1. Install MacTeX: https://www.tug.org/mactex/
2. Open terminal in `docs/latex/` directory
3. Run:
```bash
pdflatex findings_report.tex
pdflatex findings_report.tex
```

### Linux
```bash
sudo apt-get install texlive-full  # Ubuntu/Debian
# OR
sudo yum install texlive  # Fedora/RHEL

cd docs/latex
pdflatex findings_report.tex
pdflatex findings_report.tex
```

---

## Option 3: Convert to Markdown (For LinkedIn Post)

If you just want to share on LinkedIn without PDF:

1. The LaTeX contains all the content
2. Copy sections directly to LinkedIn as text
3. Use LinkedIn formatting (bold, italics, bullets)
4. Add the GitHub link

**Key sections to include:**
- Executive Summary
- The Scale of the Problem
- What the Data Reveals (temporal, seasonal, causes)
- The Containment Effectiveness Problem
- The Path Forward
- Link to GitHub repo

---

## Files Created

- `findings_report.tex` - Main findings document (LinkedIn-ready)
- `methodology.tex` - Full technical methodology (academic)

Both are publication-quality LaTeX documents ready for compilation.

---

## Troubleshooting

**"Package not found" errors:**
- MiKTeX/MacTeX will auto-install missing packages on first compile
- Click "Install" when prompted
- May need to run pdflatex 2-3 times for all references to resolve

**Compilation takes forever:**
- First compile is slow (installs packages)
- Subsequent compiles are fast

**Still having issues:**
- Use Overleaf (online, always works)
- Or share the `.tex` file directly - many professionals can compile it