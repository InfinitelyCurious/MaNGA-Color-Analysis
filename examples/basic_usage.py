Basic usage example for MaNGA Color-Mass Analysis Tools

This script demonstrates the simplest way to create a color-mass diagram
with your galaxy sample.

Author: Olivia A. Greene, PhD
"""

import sys
sys.path.append('..')  # Add parent directory to path

from color_mass_diagram import create_color_mass_diagram

# ============================================================================
# BASIC USAGE
# ============================================================================

def main():
    """
    Create a basic color-mass diagram with default settings
    """
    
    print("=" * 60)
    print("BASIC COLOR-MASS DIAGRAM EXAMPLE")
    print("=" * 60)
    
    print("\nBefore running, make sure you've updated these in color_mass_diagram.py:")
    print("  - BASE_PATH (path to your data directory)")
    print("  - BACKGROUND_SAMPLE_FILE (your background data)")
    print("  - YOUR_SAMPLE_FILE (your galaxy sample)")
    print("  - MORPHOLOGY_FILE (optional morphology data)")
    print("\n" + "=" * 60)
    
    # Create diagram with dust correction (default)
    create_color_mass_diagram(
        save_plot=True,                    # Save to output/ directory
        apply_dust_correction=True         # Apply Milky Way dust correction
    )
    
    print("\n" + "=" * 60)
    print("DONE! Check output/ directory for your plot.")
    print("=" * 60)


if __name__ == "__main__":
    main()
