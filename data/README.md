# Data Directory

This directory contains the data files needed to run the color-mass analysis.

## ⚠️ Large Files Not Included

Due to GitHub's 100 MB file size limit, large data files are **not included** in this repository.

---

## Required Data Files

### 1. Background Sample (`background_sample.csv`)

**Description:** Large random SDSS sample for density contour mapping  
**Size:** ~200 MB  
**Galaxies:** 50,000+ (balanced blue cloud and red sequence)  
**Source:** SDSS DR17 via CasJobs

**Required Columns:**
- `redshift` - Galaxy redshift
- `u`, `g`, `r` - SDSS magnitudes (apparent)
- `log_total_mass_median` - Stellar mass (optional)

**Download:** [Coming Soon - Zenodo DOI]

---

### 2. Your Galaxy Sample (`your_sample.csv`)

**Description:** Your galaxy catalog to analyze (e.g., E+A galaxies, post-starburst systems)  
**Size:** Variable  
**Source:** Your research

**Required Columns:**
- `plateifu` - MaNGA galaxy identifier (or your ID system)
- `redshift` - Galaxy redshift
- `u`, `g`, `r` - SDSS magnitudes (apparent)
- `log_nsa_elpetro_mass` - Stellar mass

**Example:** See `examples/sample_data_template.csv`

---

### 3. Morphology Data (`morphology_data.csv`) *[Optional]*

**Description:** Morphological classifications from MVM-VAC or equivalent  
**Source:** Vázquez-Mata et al. (2022), MNRAS, 512, 2222

**Required Columns:**
- `plateifu` - MaNGA galaxy identifier (must match your sample)
- `morphology` - Hubble classification (e.g., "SBb", "E", "S0")

**Download:** [SDSS Data Release 17 - MVM-VAC](https://data.sdss.org/sas/dr17/manga/morphology/vac/)

---

## Data Format Examples

### Background Sample Format
```csv
redshift,u,g,r,log_total_mass_median
0.045,18.234,17.123,16.543,10.234
0.062,19.012,17.891,17.234,9.876
```

### Your Sample Format
```csv
plateifu,redshift,u,g,r,log_nsa_elpetro_mass
8485-12701,0.0452,17.543,16.789,16.234,10.456
8485-12702,0.0389,18.123,17.234,16.678,10.123
```

### Morphology Format
```csv
plateifu,morphology
8485-12701,SBb
8485-12702,E
8485-12703,S0
```

---

## Setting Up Your Data

1. **Download data files** (from Zenodo, SDSS, or your own sources)
2. **Place files in this `data/` directory**
3. **Update paths** in `color_mass_diagram.py`:
   ```python
   BASE_PATH = '/path/to/your/data/'
   BACKGROUND_SAMPLE_FILE = f"{BASE_PATH}background_sample.csv"
   YOUR_SAMPLE_FILE = f"{BASE_PATH}your_sample.csv"
   MORPHOLOGY_FILE = f"{BASE_PATH}morphology_data.csv"
   ```

---

## Generating Your Own Background Sample

If you want to create your own background sample from SDSS:

### CasJobs Query (SDSS DR17)
```sql
SELECT TOP 50000
    z AS redshift,
    u, g, r,
    log_total_mass_median
FROM SpecPhotoAll
WHERE 
    z > 0.01 AND z < 0.15
    AND u > 0 AND g > 0 AND r > 0
    AND specClass = 2  -- Galaxies only
ORDER BY NEWID()  -- Random sample
```

Save results as `background_sample.csv` in this directory.

---

## Questions?

- **Data access issues?** Contact: oliviaallegragreene@gmail.com
- **Format questions?** See `examples/` directory for templates
- **Citation info?** See main README.md

---

**Last Updated:** January 2026
