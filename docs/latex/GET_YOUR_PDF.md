# Get Your PDF in 2 Minutes

## Simplest Method: Overleaf (100% works, no installation)

### Step 1: Go to Overleaf
**Visit:** https://www.overleaf.com/
- Click "Register" (free account)
- Use Google/email to sign up

### Step 2: Create Project
- Click green **"New Project"** button
- Select **"Upload Project"**

### Step 3: Create ZIP file
**On Windows:**
1. Open File Explorer
2. Navigate to: `C:\Users\ntrie\OneDrive\Documents\Data Projects\FireStarter\FireAnalyst\docs\latex`
3. Select these 6 files (Ctrl+Click each one):
   - ✅ `findings_report.tex`
   - ✅ `fires_over_time.png`
   - ✅ `peak_years_for_fires.png`
   - ✅ `seasonality.png`
   - ✅ `cause_distribution.png`
   - ✅ `containment_effectiveness.png`
4. Right-click → "Send to" → "Compressed (zipped) folder"
5. Name it: `FireAnalyst_Report.zip`

### Step 4: Upload to Overleaf
- In Overleaf, click "Upload Project"
- Select your ZIP file
- Click "Upload"

### Step 5: Compile
- Overleaf opens automatically
- Click green **"Recompile"** button (top right)
- Wait ~10 seconds
- PDF appears in preview!

### Step 6: Download
- Click **"Download PDF"** button (next to Recompile)
- Save to your desktop
- Done! 🎉

---

## Alternative: Use an Online LaTeX Compiler

If you don't want to sign up for Overleaf:

### Option A: LaTeX.Online
**Not recommended** - doesn't handle multiple files well

### Option B: Papeeria
1. Go to: https://papeeria.com/
2. Similar process to Overleaf
3. Free tier available

---

## Install LaTeX Locally (For Future Use)

If you want to compile locally in the future:

### Windows:
1. Download MiKTeX: https://miktex.org/download
2. Run installer (takes ~10 minutes)
3. Then run:
```bash
cd "C:\Users\ntrie\OneDrive\Documents\Data Projects\FireStarter\FireAnalyst\docs\latex"
pdflatex findings_report.tex
pdflatex findings_report.tex  # Run twice for references
```

**Size:** ~500MB installation

---

## Troubleshooting

**"Images not found" error:**
✅ Fixed! All images are now in the same folder as the .tex file

**"Package not found" error:**
- In Overleaf: Auto-installs packages (just wait)
- In MiKTeX: Click "Install" when prompted

**"Compilation timeout":**
- Wait 30 seconds and try again
- Overleaf free tier has limits, but this document is small enough

---

## What the PDF Will Look Like

✅ 8-9 pages, professional layout
✅ 5 embedded visualizations (full color, high res)
✅ Colored boxes for insights
✅ Statistical tables
✅ GitHub links
✅ Ready to attach to LinkedIn post

---

## Quick Reference

**Files Location:**
```
C:\Users\ntrie\OneDrive\Documents\Data Projects\FireStarter\FireAnalyst\docs\latex\
```

**Files Needed (6 total):**
1. findings_report.tex (main document)
2. fires_over_time.png
3. peak_years_for_fires.png
4. seasonality.png
5. cause_distribution.png
6. containment_effectiveness.png

**Overleaf:** https://www.overleaf.com/
**Estimated Time:** 2-5 minutes total

---

## Need Help?

If you get stuck:
1. Check that all 6 files are in the ZIP
2. Make sure ZIP isn't corrupted (try extracting it first)
3. Try uploading files one-by-one instead of ZIP
4. Contact me with the error message

---

**Go to Overleaf now:** https://www.overleaf.com/

It's free, fast, and will definitely work! 🚀