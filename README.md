# MaNGA Color-Mass Analysis Tools

Comprehensive color-mass and color-magnitude analysis suite with empirically-derived green valley boundaries and dust corrections for SDSS-IV MaNGA galaxy samples.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This toolkit provides methods for analyzing galaxy evolution through color-mass diagrams with explicit green valley modeling. Developed for post-starburst galaxy research, these tools implement uniform dust corrections, empirically-derived evolutionary boundaries, and mass-scaling visualizations to place galaxies in evolutionary context.

**Key Innovation:** Explicitly defines green valley boundaries (typically referenced but rarely quantified in literature) using balanced sampling of blue cloud and red sequence populations from large SDSS catalogs.

## Features

- **Dust Correction Implementation**: Uses Schlegel+ extinction maps with extinction_coefficient package in "simple mode"
- **Empirically-Derived Green Valley Boundaries**: Quantitative definitions from balanced 50k+ galaxy samples
- **Multi-Color Analysis**: (u-r), (g-r), and (u-g) color indices
- **Mass-Scaling Visualization**: Marker size and colormap encode stellar mass information
- **Contour Density Mapping**: 10x10 binning reveals population structure
- **Morphology Integration**: Supports MVM-VAC morphological classifications

## Scientific Context

Traditional studies reference the "green valley" as a transitional region between star-forming (blue cloud) and quiescent (red sequence) populations, but rarely provide explicit boundary definitions. This toolkit addresses that gap by:

1. Filtering large random samples to achieve balanced blue/red representation
2. Modeling tri-modal population structure following Eales+ methodology
3. Extracting quantitative boundaries at specified mass intervals
4. Validating against Schawinski+ evolutionary tracks

**Result:** Reproducible, quantitative green valley boundaries for (u-r) vs. stellar mass, (g-r) vs. M_r, and (u-g) vs. M_g.

## Installation

```bash
git clone https://github.com/InfinitelyCurious/MaNGA-Color-Mass-Analysis.git
cd MaNGA-Color-Mass-Analysis

pip install -r requirements.txt
```

### Dependencies

```
numpy>=1.20
matplotlib>=3.3
astropy>=5.0
pandas>=1.3
scipy>=1.7
extinction_coefficient>=1.0
```

## Quick Start

### Basic Color-Mass Diagram

```python
from color_mass_diagram import create_color_mass_diagram

# Create color-mass diagram with dust correction
create_color_mass_diagram(
    save_plot=True,
    apply_dust_correction=True,
    supplement_background=True
)
```

### Output:
- Contour map of SDSS background population
- Your sample galaxies with morphology-based coloring
- Empirically-derived green valley boundaries
- Mass-scaled markers

## Methodology

### Dust Correction

Implements Schlegel, Finkbeiner & Davis (1998) extinction maps via `extinction_coefficient` package:

```python
from extinction_coefficient import extinction_coefficient

# Get extinction coefficients
A_u = extinction_coefficient("u'", mode='simple')
A_g = extinction_coefficient("g'", mode='simple')  
A_r = extinction_coefficient("r'", mode='simple')

# Apply corrections
u_corrected = u_observed - A_u * E(B-V)
```

**Default E(B-V):** 0.08 (Milky Way foreground)

### Green Valley Modeling

1. **Strategic Sampling:** Load full cidcuts data (~40k galaxies) + SDSS supplement
2. **Blue Boosting:** Replicate blue cloud galaxies (g-r < 0.5) to balance red sequence bias
3. **Density Mapping:** 10x10 histogram with minimum threshold (400 galaxies/bin)
4. **Boundary Extraction:** Linear fits to empirical valley edges

**Resulting boundaries (u-r vs. log M*):**
```
Lower: (u-r) = 2.0 + 0.27*(log M* - 8.5) - 0.42
Upper: (u-r) = 2.0 + 0.27*(log M* - 8.5)
```

### Morphology Classification

Integrates with MaNGA Visual Morphologies VAC (MVM-VAC) for 6-category classification:
- Spiral
- Barred Spiral
- Weakly Barred Spiral
- Lenticular
- Elliptical  
- Unknown

Color-coded markers reveal morphology-evolution decoupling.

## Usage Examples

### Reproduce Dissertation Figures

```python
# Color-mass with morphology (Chapter 3, Greene 2026)
create_color_mass_diagram(
    save_plot=True,
    apply_dust_correction=True,
    supplement_background=True
)
```

### Custom Sample Analysis

```python
# Analyze your own galaxy sample
from color_mass_diagram import load_your_sample, create_color_mass_diagram

# Load your catalog (requires: plateifu, u, g, r, redshift, mass, morphology)
masses, ur, morphologies, *_ = load_your_sample(
    sample_file='your_galaxies.csv',
    apply_dust_correction=True
)

# Customize plot parameters in configuration section
create_color_mass_diagram(save_plot=True)
```

### Generate All Three Color Diagrams

```python
# (u-r) vs. log M*
create_color_mass_diagram(apply_dust_correction=True)

# Additional color indices can be implemented following the same framework
```

## Data Requirements

### Background Sample
- **Source:** SDSS DR17 random catalog via CasJobs
- **Size:** 50,000 galaxies (balanced blue/red after strategic filtering)
- **Columns:** redshift, u, g, r, log_total_mass_median

### Your Sample  
- **Source:** Your catalog (e.g., 183 E+A galaxies or custom sample)
- **Columns:** plateifu (or galaxy ID), redshift, u, g, r, log_mass, morphology (optional)

**Note:** Large data files (>100 MB) are excluded via `.gitignore`. See `data/README.md` for download instructions and required CSV structure.

## Customization

The code is designed to be generic and user-friendly. Key configuration options:

**In the USER CONFIGURATION section** (top of `color_mass_diagram.py`):
- `BASE_PATH`: Your data directory
- `BACKGROUND_SAMPLE_FILE`: Your background galaxy CSV
- `YOUR_SAMPLE_FILE`: Your galaxy sample CSV
- Column name mappings (adjust to match your CSV headers)
- `APPLY_DUST_CORRECTION`: Toggle dust corrections
- `MAX_BACKGROUND_GALAXIES`: Sample size for contour mapping

See inline comments in code for detailed customization instructions.

## Output Examples

**Color-Mass Diagram Features:**
- Background contours reveal bimodal population structure
- Green valley boundaries (green lines) separate evolutionary regions
- Sample galaxies color-coded by morphology
- Marker size scales with stellar mass
- Legend includes morphology counts

**Files Generated:**
- `color_mass_diagram_morphology_dust_corrected.png`
- Customizable DPI (default: 300)
- Publication-ready formatting

## Validation

Boundaries validated against:
- Schawinski+ (2014) evolutionary tracks ✓
- Eales+ tri-modal modeling ✓
- Independent MaNGA color-mass distributions ✓

**Consistency:** 74% of 183 E+A galaxies fall within defined green valley (expected for post-starburst systems).

## Scientific Applications

### Post-Starburst Research
- Confirm green valley residence of E+A galaxies
- Track evolutionary position of quenched systems
- Morphology-evolution decoupling analysis

### General Galaxy Evolution
- Quantify blue cloud → red sequence transition rates
- Measure green valley residence times
- Morphology-independent evolutionary studies

### Survey Planning
- Define color-based selection for transitional populations
- Estimate contamination from non-transitional systems

## Citation

```bibtex
@phdthesis{Greene2026thesis,
  author = {Greene, Olivia A},
  title = {Seeing What Is, What Was, What Could Be, What Must Not: 
           Refining, Cataloging, and Investigating A Complete, 
           Spatially Resolved Spectrophotometric Sample of Nearby 
           Post-Starburst E+A Galaxies in SDSS-IV MaNGA},
  school = {Vanderbilt University},
  year = {2026},
  note = {Chapter 3: Color-Mass Analysis Methodology}
}

@article{Greene2026,
  author = {Greene, Olivia A., et. al.},
  title = {A Complete Catalog of Post-starburst, E+A Galaxies in SDSS-IV MaNGA (MPL-11):
           A Citizen Science Approach to Spectrophotometric Classification \&
           the Automation of Equivalent Width Measurements},
  journal = {The Astrophysical Journal},
  year = {2026},
  note = {In Preparation}
}
```

## Related Projects

- **[MEWS](https://github.com/InfinitelyCurious/Measuring-Equivalent-Width-in-Spectra-MEWS-)**: Equivalent width measurement pipeline
- **E+A Galaxy Catalog**: 183 spatially-resolved post-starburst galaxies (in development)
- **MOONJAM**: MaNGA diagnostic suite (collaborative project, in development)

## Contributing

Contributions welcome! Areas for enhancement:
- Additional color indices (e.g., NUV-optical)
- Machine learning boundary optimization
- Interactive visualization tools
- Extended redshift coverage

## Troubleshooting

**Common Issues:**

**"File not found" errors**
→ Update `BASE_PATH` and filename variables in USER CONFIGURATION section

**"Red sequence bias in background sample"**
→ Increase blue boosting factor (currently 3x replication in code)

**"Green valley boundaries don't match literature"**
→ Check dust correction applied consistently to both background and sample

**"Morphology data missing"**
→ Script continues without morphology; ensure MVM-VAC catalog downloaded and plateifu formats match

**Column name mismatches**
→ Update column mapping variables in configuration section to match your CSV headers

## Acknowledgments

Developed at Vanderbilt University (2020-2026) as part of dissertation research on post-starburst galaxies in MaNGA.

**Advisors:**
- Dr. Kelly Holley-Bockelmann (Vanderbilt University)
- Dr. Charles T. Liu (CUNY College of Staten Island / American Museum of Natural History)

**Data Sources:**
- SDSS-IV MaNGA Survey
- Schlegel, Finkbeiner & Davis (1998) dust maps
- MaNGA Visual Morphologies VAC (Domínguez Sánchez+ 2022)

## License

MIT License - See LICENSE file for details

## Contact

**Olivia A. Greene, PhD**  
Astrophysicist | Pipeline Developer  
Email: oliviaallegragreene@gmail.com  
Website: https://galaxygreene.com  
GitHub: [@InfinitelyCurious](https://github.com/InfinitelyCurious)

