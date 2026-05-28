"""
Custom sample analysis example for MaNGA Color-Mass Analysis Tools

This script demonstrates how to customize the analysis for your specific data.

Author: Olivia A. Greene, PhD
"""

import sys
sys.path.append('..')

from color_mass_diagram import (
    create_color_mass_diagram,
    load_your_sample,
    load_background_sample
)
import numpy as np

# ============================================================================
# CUSTOM ANALYSIS EXAMPLE
# ============================================================================

def analyze_custom_sample():
    """
    Example of custom analysis workflow
    """
    
    print("=" * 60)
    print("CUSTOM SAMPLE ANALYSIS")
    print("=" * 60)
    
    # Step 1: Load and inspect your data
    print("\nStep 1: Loading data...")
    R, G, gr, ug, ur, masses, morphologies = load_your_sample(
        apply_dust_correction=True
    )
    
    print(f"\nSample loaded: {len(masses)} galaxies")
    print(f"Mass range: {masses.min():.2f} - {masses.max():.2f} log(M*/M_sun)")
    print(f"Color range (u-r): {ur.min():.2f} - {ur.max():.2f}")
    
    # Step 2: Create color-mass diagram
    print("\nStep 2: Creating color-mass diagram...")
    create_color_mass_diagram(
        save_plot=True,
        apply_dust_correction=True
    )
    
    # Step 3: Analyze green valley membership
    print("\nStep 3: Analyzing green valley membership...")
    analyze_green_valley_membership(masses, ur)
    
    # Step 4: Morphology breakdown
    print("\nStep 4: Morphology breakdown...")
    print_morphology_summary(morphologies)
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


def analyze_green_valley_membership(masses, ur_colors):
    """
    Determine which galaxies fall in the green valley
    
    Parameters:
    -----------
    masses : array
        Stellar masses (log M*/M_sun)
    ur_colors : array
        (u-r) colors
    """
    # Green valley boundaries from Greene (2026)
    GV_BASE = 2.0
    GV_SLOPE = 0.27
    GV_MASS_ZERO = 8.5
    GV_WIDTH = 0.42
    
    # Calculate boundaries for each galaxy
    upper_boundary = GV_BASE + GV_SLOPE * (masses - GV_MASS_ZERO)
    lower_boundary = upper_boundary - GV_WIDTH
    
    # Check membership
    in_green_valley = (ur_colors >= lower_boundary) & (ur_colors <= upper_boundary)
    above_valley = ur_colors > upper_boundary
    below_valley = ur_colors < lower_boundary
    
    print(f"\nGreen valley members: {in_green_valley.sum()} / {len(masses)}")
    print(f"  Percentage: {100 * in_green_valley.sum() / len(masses):.1f}%")
    print(f"\nRed sequence (above valley): {above_valley.sum()}")
    print(f"  Percentage: {100 * above_valley.sum() / len(masses):.1f}%")
    print(f"\nBlue cloud (below valley): {below_valley.sum()}")
    print(f"  Percentage: {100 * below_valley.sum() / len(masses):.1f}%")


def print_morphology_summary(morphologies):
    """
    Print summary of morphology distribution
    
    Parameters:
    -----------
    morphologies : array
        Morphology classifications
    """
    unique_morphs, counts = np.unique(morphologies, return_counts=True)
    
    print("\nMorphology distribution:")
    for morph, count in zip(unique_morphs, counts):
        percentage = 100 * count / len(morphologies)
        print(f"  {morph}: {count} ({percentage:.1f}%)")


if __name__ == "__main__":
    analyze_custom_sample()
