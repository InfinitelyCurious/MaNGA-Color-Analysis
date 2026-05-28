"""
MaNGA Color-Mass Analysis Tools
Comprehensive color-mass and color-magnitude analysis with empirically-derived 
green valley boundaries and dust corrections for SDSS-IV MaNGA galaxy samples.

Author: Olivia A. Greene, PhD
Vanderbilt University (2020-2026)
GitHub: @InfinitelyCurious
Contact: oliviaallegragreene@gmail.com
License: MIT

Primary Citation (Dissertation):
Greene, O. A. (2026). "Seeing What Is, What Was, What Could Be, What Must Not: 
Refining, Cataloging, and Investigating A Complete, Spatially Resolved 
Spectrophotometric Sample of Nearby Post-Starburst E+A Galaxies in SDSS-IV MaNGA." 
PhD Dissertation, Vanderbilt University. 339 pages.
Advisors: Dr. Kelly Holley-Bockelmann, Dr. Charles T. Liu

Related Publication (In Prep):
Greene, O. A., et al. (2026). "A Complete Catalog of Post-starburst, E+A Galaxies 
in SDSS-IV MaNGA (MPL-11): A Citizen Science Approach to Spectrophotometric 
Classification & the Automation of Equivalent Width Measurements." 
The Astrophysical Journal (In Preparation).

Methodology from Chapter 3 of dissertation.
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.cosmology import WMAP9 as cosmo
import astropy.units as units
import pandas as pd
from matplotlib.lines import Line2D
import os
from scipy.ndimage import gaussian_filter
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from extinction_coefficient import extinction_coefficient

# ============================================================================
# USER CONFIGURATION - EDIT THESE PATHS AND FILENAMES
# ============================================================================

# Base directory containing your data files
BASE_PATH = '/path/to/your/data/'  # CHANGE THIS to your data directory

# Background sample file (large random SDSS sample for contours)
# Should contain columns: redshift, u, g, r, [optional: log_total_mass_median]
BACKGROUND_SAMPLE_FILE = f"{BASE_PATH}your_background_galaxies.csv"

# Your galaxy sample file (the galaxies you want to plot)
# Should contain columns: plateifu (or galaxy ID), redshift, u, g, r, log_mass
YOUR_SAMPLE_FILE = f"{BASE_PATH}your_galaxy_sample.csv"

# Morphology data file (optional - if you have MVM-VAC or similar classifications)
# Should contain columns: plateifu, morphology
MORPHOLOGY_FILE = f"{BASE_PATH}your_morphology_data.csv"

# Output directory for plots
OUTPUT_PATH = BASE_PATH  # Or specify a different directory

# Dust correction settings
APPLY_DUST_CORRECTION = True  # Set to False to skip dust corrections
DEFAULT_EBV = 0.08  # Milky Way foreground extinction E(B-V) value

# Plot appearance settings
MARKER_COLOR = '#8A9A5B'  # Color for your sample galaxies (if not using morphology)
PLOT_DPI = 300  # Resolution for saved plots

# ============================================================================
# COLUMN NAME MAPPING - ADJUST TO MATCH YOUR DATA FILES
# ============================================================================

# Column names in your BACKGROUND sample CSV
BACKGROUND_COLS = {
    'redshift': 'redshift',  # Redshift column name
    'u': 'u',                # u-band magnitude
    'g': 'g',                # g-band magnitude
    'r': 'r',                # r-band magnitude
    'mass': 'log_total_mass_median'  # Optional: stellar mass column
}

# Column names in YOUR sample CSV
YOUR_SAMPLE_COLS = {
    'id': 'plateifu',              # Galaxy identifier (MaNGA: plateifu)
    'redshift': 'redshift',
    'u': 'u',
    'g': 'g',
    'r': 'r',
    'mass': 'log_nsa_elpetro_mass'  # Stellar mass column name
}

# Column names in MORPHOLOGY CSV (if using)
MORPHOLOGY_COLS = {
    'id': 'plateifu',              # Must match YOUR_SAMPLE_COLS['id']
    'morphology': 'morphology'      # Morphology classification column
}

# ============================================================================
# PLOTTING SETTINGS
# ============================================================================

# Color-mass diagram plot ranges
MASS_MIN, MASS_MAX = 8.5, 12.0      # log(M*/M_sun) range
UR_MIN, UR_MAX = 0.5, 3.5            # (u-r) color range

# Color-magnitude diagram plot ranges  
MR_MIN, MR_MAX = -16, -24            # Absolute r-band magnitude range
GR_MIN, GR_MAX = 0.0, 1.2            # (g-r) color range
UG_MIN, UG_MAX = 0.0, 2.5            # (u-g) color range

# Green valley boundary parameters (for u-r vs mass)
# Boundaries: (u-r) = BASE + SLOPE*(log M* - MASS_ZERO) +/- WIDTH
GV_BASE = 2.0
GV_SLOPE = 0.27
GV_MASS_ZERO = 8.5
GV_WIDTH = 0.42

# Contour settings for background density
N_BINS = 10                  # Number of bins for 2D histogram
N_LEVELS = 10                # Number of contour levels
MIN_DENSITY = 400            # Minimum galaxies per bin for contour

# Maximum background galaxies to use (for performance)
MAX_BACKGROUND_GALAXIES = 50000

# ============================================================================
# STYLE CONFIGURATION
# ============================================================================

plt.style.use('default')
plt.rcParams["axes.edgecolor"] = "0.15"
plt.rcParams["axes.linewidth"] = 1.25
plt.rcParams['text.usetex'] = False

# ============================================================================
# CORE FUNCTIONS - NO NEED TO EDIT BELOW THIS LINE
# ============================================================================

def calculate_absolute_magnitude(apparent_mag, distance_pc):
    """
    Calculate absolute magnitude using distance in parsecs
    
    Parameters:
    -----------
    apparent_mag : array-like
        Apparent magnitude
    distance_pc : array-like
        Distance in parsecs
        
    Returns:
    --------
    absolute_mag : array-like
        Absolute magnitude with h=0.73 correction
    """
    return -5.0 * np.log10(distance_pc) + apparent_mag + 5.0 + 5.0 * np.log10(0.73)


def apply_simple_dust_correction(u, g, r, EBV_avg=DEFAULT_EBV):
    """
    Apply simple dust extinction corrections using extinction_coefficient package
    
    Uses Schlegel, Finkbeiner & Davis (1998) extinction law in simple mode
    
    Parameters:
    -----------
    u, g, r : array-like
        Observed u, g, r magnitudes
    EBV_avg : float
        E(B-V) color excess (default: 0.08 for Milky Way foreground)
        
    Returns:
    --------
    u_corrected, g_corrected, r_corrected : array-like
        Dust-corrected magnitudes
    """
    # Get extinction coefficients for SDSS filters
    A_u = extinction_coefficient("u'", mode='simple')
    A_g = extinction_coefficient("g'", mode='simple')
    A_r = extinction_coefficient("r'", mode='simple')

    # Convert to scalar values if they're arrays
    if hasattr(A_u, '__len__'):
        A_u = A_u[0]
    if hasattr(A_g, '__len__'):
        A_g = A_g[0]
    if hasattr(A_r, '__len__'):
        A_r = A_r[0]

    # Apply corrections: corrected = observed - A_lambda * E(B-V)
    u_corrected = u - A_u * EBV_avg
    g_corrected = g - A_g * EBV_avg
    r_corrected = r - A_r * EBV_avg

    return u_corrected, g_corrected, r_corrected


def load_background_sample(apply_dust_correction=APPLY_DUST_CORRECTION):
    """
    Load and process background galaxy sample for contour mapping
    
    Parameters:
    -----------
    apply_dust_correction : bool
        Apply Milky Way foreground dust corrections
        
    Returns:
    --------
    R, G : array-like
        Absolute r and g magnitudes
    gr, ug, ur : array-like
        Color indices
    masses : array-like
        Stellar masses (if available, else zeros)
    """
    print("Loading background galaxy data...")
    
    # Load background sample
    df = pd.read_csv(BACKGROUND_SAMPLE_FILE)
    
    # Extract data using column name mapping
    redshift = df[BACKGROUND_COLS['redshift']].values
    u = df[BACKGROUND_COLS['u']].values
    g = df[BACKGROUND_COLS['g']].values
    r = df[BACKGROUND_COLS['r']].values
    
    # Load masses if available
    if BACKGROUND_COLS['mass'] in df.columns:
        masses = df[BACKGROUND_COLS['mass']].values
    else:
        print("  Warning: No mass column found in background data")
        masses = np.zeros_like(redshift)
    
    # Filter out invalid redshifts
    mask = redshift > 0
    u, g, r, redshift, masses = u[mask], g[mask], r[mask], redshift[mask], masses[mask]
    
    print(f"  Loaded {len(redshift)} background galaxies")
    
    # Apply dust correction if requested
    if apply_dust_correction:
        print("  Applying dust correction to background data...")
        u, g, r = apply_simple_dust_correction(u, g, r)
    
    # Limit to maximum size for performance
    if len(redshift) > MAX_BACKGROUND_GALAXIES:
        print(f"  Randomly sampling {MAX_BACKGROUND_GALAXIES} galaxies for performance...")
        indices = np.random.choice(len(redshift), MAX_BACKGROUND_GALAXIES, replace=False)
        redshift = redshift[indices]
        u, g, r = u[indices], g[indices], r[indices]
        masses = masses[indices]
    
    # Calculate distances and absolute magnitudes
    print("  Calculating absolute magnitudes and colors...")
    d_Mpc = cosmo.comoving_distance(redshift)
    d_pc = d_Mpc.to(units.pc).value

    R = calculate_absolute_magnitude(r, d_pc)
    G = calculate_absolute_magnitude(g, d_pc)
    
    # Calculate colors
    gr = g - r
    ug = u - g
    ur = u - r

    return R, G, gr, ug, ur, masses


def load_morphology_data():
    """
    Load and process morphology data from CSV file
    
    Returns:
    --------
    morph_dict : dict
        Dictionary mapping galaxy IDs to morphology classifications
    """
    morph_dict = {}
    
    if not os.path.exists(MORPHOLOGY_FILE):
        print(f"Warning: Morphology file not found at {MORPHOLOGY_FILE}")
        print("Continuing without morphology data...")
        return morph_dict
    
    try:
        df = pd.read_csv(MORPHOLOGY_FILE)
        
        # Get column names from mapping
        id_col = MORPHOLOGY_COLS['id']
        morph_col = MORPHOLOGY_COLS['morphology']
        
        # Check if columns exist
        if id_col not in df.columns or morph_col not in df.columns:
            print(f"Warning: Expected columns '{id_col}' and '{morph_col}' not found")
            print(f"Available columns: {df.columns.tolist()}")
            return morph_dict
        
        # Build dictionary
        for idx, row in df.iterrows():
            galaxy_id = str(row[id_col])
            morph_type = row[morph_col] if pd.notna(row[morph_col]) else None
            morph_dict[galaxy_id] = morph_type
        
        print(f"Loaded morphology data for {len(morph_dict)} galaxies")
        
    except Exception as e:
        print(f"Error loading morphology data: {e}")
    
    return morph_dict


def classify_morphology(morph_type):
    """
    Classify detailed morphology into 6 broad categories
    
    Adjust this function to match your morphology classification scheme
    
    Parameters:
    -----------
    morph_type : str
        Detailed morphology string (e.g., from MVM-VAC)
        
    Returns:
    --------
    broad_category : str
        One of: 'Spiral', 'Barred Spiral', 'Weakly Barred Spiral', 
                'Lenticular', 'Elliptical', 'Unknown'
    """
    if pd.isna(morph_type) or morph_type is None or str(morph_type).strip() == '':
        return 'Unknown'

    morph_type = str(morph_type).strip().upper()

    # Ellipticals (E, Edc, E(dSph))
    if morph_type.startswith('E'):
        return 'Elliptical'

    # Handle mergers
    if 'MERGER' in morph_type:
        return 'Unknown'

    # Lenticulars - handle all S0 types
    if 'S0' in morph_type:
        return 'Lenticular'

    # Weakly barred spirals - SAB types (but not SAB0 = lenticulars)
    if morph_type.startswith('SAB'):
        return 'Weakly Barred Spiral'

    # Barred spirals - SB types (but not SB0 = lenticulars)
    if morph_type.startswith('SB'):
        return 'Barred Spiral'

    # Regular spirals (Sa, Sb, Sc, Scd, Sab, Sbc, etc.)
    if morph_type.startswith('S'):
        return 'Spiral'

    return 'Unknown'


def load_your_sample(apply_dust_correction=APPLY_DUST_CORRECTION):
    """
    Load your galaxy sample and match with morphology data
    
    Parameters:
    -----------
    apply_dust_correction : bool
        Apply Milky Way foreground dust corrections
        
    Returns:
    --------
    R, G : array-like
        Absolute r and g magnitudes
    gr, ug, ur : array-like
        Color indices
    masses : array-like
        Stellar masses
    morphologies : array-like
        Morphology classifications (or 'Unknown' if not available)
    """
    print(f"Loading your galaxy sample from {YOUR_SAMPLE_FILE}...")
    
    # Load your sample
    df = pd.read_csv(YOUR_SAMPLE_FILE)
    
    print(f"Loaded {len(df)} galaxies from your sample")
    
    # Extract data using column name mapping
    galaxy_ids = df[YOUR_SAMPLE_COLS['id']].astype(str).values
    redshift = df[YOUR_SAMPLE_COLS['redshift']].values
    u = df[YOUR_SAMPLE_COLS['u']].values
    g = df[YOUR_SAMPLE_COLS['g']].values
    r = df[YOUR_SAMPLE_COLS['r']].values
    masses = df[YOUR_SAMPLE_COLS['mass']].values
    
    # Load morphology data if available
    print("Loading morphology data...")
    morph_dict = load_morphology_data()
    
    # Add morphology to dataframe
    df['detailed_morph'] = df[YOUR_SAMPLE_COLS['id']].astype(str).map(morph_dict)
    df['morph_class'] = df['detailed_morph'].apply(classify_morphology)
    
    # Check for missing morphologies
    missing_morph = df['detailed_morph'].isna().sum()
    if missing_morph > 0:
        print(f"  Warning: {missing_morph} galaxies have no morphology data")
    
    # Print morphology distribution
    morph_counts = df['morph_class'].value_counts()
    print(f"\nMorphology distribution:")
    for morph_type, count in morph_counts.items():
        print(f"  {morph_type}: {count}")
    
    # Extract morphologies
    morphologies = df['morph_class'].values
    
    # Apply dust correction if requested
    if apply_dust_correction:
        print("Applying dust correction to your sample...")
        u, g, r = apply_simple_dust_correction(u, g, r)
    
    # Calculate distances
    d_Mpc = cosmo.comoving_distance(redshift)
    d_pc = d_Mpc.to(units.pc).value

    # Calculate absolute magnitudes and colors
    R = calculate_absolute_magnitude(r, d_pc)
    G = calculate_absolute_magnitude(g, d_pc)
    gr = g - r
    ug = u - g
    ur = u - r

    return R, G, gr, ug, ur, masses, morphologies


def create_color_mass_diagram(save_plot=True, apply_dust_correction=APPLY_DUST_CORRECTION):
    """
    Create color-mass diagram with morphology-based coloring
    
    Parameters:
    -----------
    save_plot : bool
        Save plot to OUTPUT_PATH
    apply_dust_correction : bool
        Apply dust corrections to data
    """
    print("\n" + "="*60)
    print("CREATING COLOR-MASS DIAGRAM")
    print("="*60)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 9))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#F4F4EC')
    
    # Load background sample
    _, _, _, _, ur_background, masses_background = load_background_sample(apply_dust_correction)
    
    # Load your sample
    _, _, _, _, ur_sample, masses_sample, morphologies_sample = load_your_sample(apply_dust_correction)
    
    # Filter background data to plot ranges
    mask_bg = ((masses_background > MASS_MIN) & (masses_background < MASS_MAX) &
               (ur_background > UR_MIN) & (ur_background < UR_MAX))
    
    masses_filtered = masses_background[mask_bg]
    ur_filtered = ur_background[mask_bg]
    
    print(f"\nFiltered background sample: {len(masses_filtered)} galaxies")
    
    # Create contour density map
    bins = np.array([np.linspace(MASS_MIN, MASS_MAX, N_BINS+1),
                     np.linspace(UR_MIN, UR_MAX, N_BINS+1)])
    Z = np.histogram2d(masses_filtered, ur_filtered, bins=bins)[0].T
    extent = [MASS_MIN, MASS_MAX, UR_MIN, UR_MAX]
    
    # Set contour levels
    if Z.max() > MIN_DENSITY:
        levels = np.linspace(MIN_DENSITY, Z.max(), N_LEVELS)
    else:
        levels = np.linspace(Z.max() * 0.1, Z.max(), N_LEVELS)
    
    # Plot contours
    ax.contour(Z, extent=extent, levels=levels, colors='#777777')
    
    # Plot background galaxies
    ax.scatter(masses_filtered, ur_filtered, c='#999999', marker='.', 
               s=0.5, alpha=0.3, zorder=1)
    
    # Generate green valley boundaries
    x = np.linspace(MASS_MIN, MASS_MAX, 100)
    y_upper = GV_BASE + GV_SLOPE * (x - GV_MASS_ZERO)
    y_lower = y_upper - GV_WIDTH
    
    # Plot valley boundaries
    valley_color = 'green'
    ax.plot(x, y_lower, color=valley_color, linestyle='-', 
            linewidth=2, zorder=3, label='Green Valley')
    ax.plot(x, y_upper, color=valley_color, linestyle='-', linewidth=2, zorder=3)
    
    # Define morphology colors (6 categories)
    morph_types = ['Spiral', 'Barred Spiral', 'Weakly Barred Spiral', 
                   'Lenticular', 'Elliptical', 'Unknown']
    morph_colors = ['#B765A7', '#061993', '#1973d1', '#2ca02c', '#d62728', '#ffdd3c']
    morph_color_map = dict(zip(morph_types, morph_colors))
    
    # Use uniform marker size
    uniform_size = 60
    
    # Plot your sample with morphology-based coloring
    for morph_type in morph_types:
        mask = morphologies_sample == morph_type
        if np.sum(mask) > 0:
            ax.scatter(masses_sample[mask], ur_sample[mask],
                      c=morph_color_map[morph_type], s=uniform_size,
                      marker='o', zorder=4, linewidths=0.5,
                      edgecolors='black', alpha=0.8, label=morph_type)
    
    # Set plot limits and labels
    ax.set_ylim(UR_MIN, UR_MAX)
    ax.set_xlim(MASS_MIN, MASS_MAX)
    ax.set_ylabel('$(u-r)$ colour', size=18, labelpad=15)
    ax.set_xlabel(r'Stellar Mass [$\log(M_*/M_{\odot})$]', size=18, labelpad=15)
    
    # Title
    title_suffix = " (Dust Corrected)" if apply_dust_correction else ""
    ax.set_title(f'Colour-Mass Diagram{title_suffix}', size=20, pad=15)
    
    # Add ticks to right side
    ax.tick_params(axis='y', which='both', right=True, labelright=True)
    
    # Create legend
    legend_elements = [plt.Line2D([0], [0], color='green', linewidth=2, 
                                   label='Green Valley')]
    
    # Add morphology legend elements
    for morph_type in morph_types:
        if morph_type in morphologies_sample:
            count = np.sum(morphologies_sample == morph_type)
            if count > 0:
                legend_elements.append(
                    plt.scatter([], [], s=uniform_size, c=morph_color_map[morph_type],
                              marker='o', edgecolors='black', alpha=0.8,
                              label=f'{morph_type} ({count})')
                )
    
    ax.legend(handles=legend_elements, loc='lower right', fontsize=12,
              title='Morphology', title_fontsize=14)
    
    plt.tight_layout()
    
    # Save plot if requested
    if save_plot:
        filename_suffix = "_dust_corrected" if apply_dust_correction else ""
        output_file = os.path.join(OUTPUT_PATH, 
                                   f"color_mass_diagram_morphology{filename_suffix}.png")
        plt.savefig(output_file, dpi=PLOT_DPI, bbox_inches='tight')
        print(f"\nPlot saved to: {output_file}")
    
    print("\n" + "="*60)
    print(f"Your sample: {len(masses_sample)} galaxies plotted")
    print("="*60)
    
    plt.show()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("MaNGA COLOR-MASS ANALYSIS TOOLS")
    print("="*60)
    print(f"\nConfiguration:")
    print(f"  Base path: {BASE_PATH}")
    print(f"  Dust correction: {'ON' if APPLY_DUST_CORRECTION else 'OFF'}")
    print(f"  Output path: {OUTPUT_PATH}")
    
    # Create color-mass diagram
    create_color_mass_diagram(save_plot=True, apply_dust_correction=APPLY_DUST_CORRECTION)
