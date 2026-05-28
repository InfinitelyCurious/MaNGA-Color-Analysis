# Output Directory

Generated plots and figures are saved here.

## Default Output Files

When you run `create_color_mass_diagram()`, the following files are generated:

- **`color_mass_diagram_morphology_dust_corrected.png`** - Color-mass diagram with dust correction applied
- **`color_mass_diagram_morphology.png`** - Color-mass diagram without dust correction

## File Naming Convention

```
color_mass_diagram_[options].png
```

**Options:**
- `morphology` - Includes morphology-based coloring
- `dust_corrected` - Dust corrections applied

## Customization

### Change Output Location

Edit `OUTPUT_PATH` in `color_mass_diagram.py`:

```python
OUTPUT_PATH = '/your/custom/path/'
```

### Change Resolution

Edit `PLOT_DPI` in `color_mass_diagram.py`:

```python
PLOT_DPI = 300  # Default (publication quality)
PLOT_DPI = 150  # Lower resolution (faster)
PLOT_DPI = 600  # High resolution (large file size)
```

## Output Specifications

**Default Settings:**
- **Format:** PNG
- **DPI:** 300 (publication quality)
- **Size:** ~12 x 9 inches
- **Color space:** RGB

**Typical File Size:** 2-5 MB per plot

## Questions?

Contact: oliviaallegragreene@gmail.com
```
