# Examples Directory

Example scripts demonstrating how to use the color-mass analysis toolkit.

## Available Examples

### 1. Basic Usage (`basic_usage.py`)

Simple example that:
- Loads data from configured paths
- Applies dust correction
- Creates a color-mass diagram

**Use this if:** You want the quickest way to generate a plot with default settings.

### 2. Custom Sample Analysis (`custom_sample_analysis.py`)

Advanced example that:
- Loads and inspects data
- Analyzes green valley membership
- Demonstrates customization options

**Use this if:** You want to understand the workflow and customize analysis.

---

## Running Examples

### Prerequisites

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download data files** (see `data/README.md`)

3. **Update configuration** in `color_mass_diagram.py`:
   - Set `BASE_PATH` to your data directory
   - Set file paths for your data

### Run Basic Example

```bash
python examples/basic_usage.py
```

### Run Custom Analysis

```bash
python examples/custom_sample_analysis.py
```

---

## Expected Output

Both examples will:
1. Print status messages to console
2. Generate plot(s) in `output/` directory
3. Display summary statistics

---

## Troubleshooting

**"File not found" errors:**
- Check that `BASE_PATH` is set correctly in `color_mass_diagram.py`
- Verify data files exist in the `data/` directory

**Import errors:**
- Run `pip install -r requirements.txt`
- Check that you're running from the repository root directory

**"No module named 'extinction_coefficient'":**
- Install package: `pip install extinction_coefficient`

---

## Questions?

- See main README.md for detailed documentation
- Contact: oliviaallegragreene@gmail.com

---

**Last Updated:** January 2026
