# Run Classification Validation App 🎯

A Streamlit-based application for validating automated run classifications from experimental logbook data. Designed to help researchers efficiently review and correct automated classifications of sample runs, calibration runs, alignment runs, and background runs.

## Features

### ✨ Core Functionality
- **Interactive validation interface** with activity-focused decision making
- **Bulk operations** for common patterns (DARK runs, water runs, etc.)
- **Keyboard shortcuts** for efficient navigation and validation
- **Progress tracking** with statistics and completion metrics
- **JSON export** for integration with analysis pipelines

### 🚀 Efficiency Features
- **Smart suggestions** based on activity patterns
- **Pattern recognition** for bulk validation
- **Progress persistence** - resume work anytime
- **Quick navigation** between runs and experiments

### 📊 Statistics & Insights
- Real-time validation progress
- Accuracy metrics (corrections vs confirmations)
- Classification breakdowns
- Recent corrections history

## Installation

### Option 1: Install as Python Package (Recommended)

**For end users who want a simple command-line tool:**

1. **Install the package**
   ```bash
   cd /path/to/run-classification-validation-app
   pip install .
   ```

2. **Run the application**
   ```bash
   # Simple usage
   run-classification-validator
   
   # Or use short alias
   rcv
   
   # With custom settings
   run-classification-validator --data-path /path/to/experiments --port 8502
   ```

3. **Access the app**
   Open your browser to `http://localhost:8501` (or your custom port)

### Option 2: Development Setup

**For developers or users who want to modify the code:**

1. **Clone or download this directory**
   ```bash
   cd /path/to/run-classification-validation-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   # OR use the included script
   ./run_app.sh
   ```

4. **Access the app**
   Open your browser to `http://localhost:8501`

### CLI Tool Usage

Once installed as a package, you can use the command-line interface:

```bash
# Show help
run-classification-validator --help

# Basic usage with default settings
run-classification-validator

# Specify custom data directory and validation directory
run-classification-validator --data-path /path/to/experiments --validation-dir /custom/validations

# Use custom port and reviewer name
run-classification-validator --port 8502 --reviewer "Jane Doe"

# Run without auto-opening browser
run-classification-validator --no-browser

# Run in debug mode
run-classification-validator --debug
```

#### CLI Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--data-path` | `-d` | Path to experiment markdown files | (configurable in UI) |
| `--validation-dir` | `-v` | Validation data directory | `validations` or `$VALIDATION_DATA_DIR` |
| `--reviewer` | `-r` | Reviewer name for validations | `Reviewer` |
| `--port` | `-p` | Streamlit server port | `8501` |
| `--host` | | Streamlit server host | `localhost` |
| `--no-browser` | | Don't auto-open browser | `false` |
| `--debug` | | Enable debug logging | `false` |
| `--version` | | Show version information | |
| `--help` | `-h` | Show help message | |

## Configuration

### Environment Variables

You can customize the application behavior using environment variables:

- **`VALIDATION_DATA_DIR`**: Directory where validation progress files are stored
  - Default: `validations`
  - Example: `export VALIDATION_DATA_DIR=/path/to/custom/validations`

### Setting Custom Validation Directory

1. **Via Environment Variable** (recommended for permanent setup):
   ```bash
   # Option 1: Set directly
   export VALIDATION_DATA_DIR=/path/to/my/validation/data
   streamlit run app.py
   
   # Option 2: Use .env file
   cp .env.example .env
   # Edit .env file with your custom settings
   streamlit run app.py
   ```

2. **Via Application Interface**: 
   - Use the "Validation data directory" field in the sidebar
   - Overrides the environment variable for the current session

3. **Examples**:
   ```bash
   # Store validations in home directory
   export VALIDATION_DATA_DIR=~/experiment_validations
   
   # Store validations in shared project directory
   export VALIDATION_DATA_DIR=/shared/project/validations
   
   # Store validations in current working directory
   export VALIDATION_DATA_DIR=./validation_progress
   ```

## Usage

### Getting Started

1. **Configure data path**: Enter the path to your experiment markdown files
2. **Set reviewer name**: Your name will be recorded with validations
3. **Set validation directory**: Choose where to store progress files (optional)
4. **Select experiment**: Choose an experiment file to validate
5. **Start validating**: Review activities and confirm/correct classifications

### Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│ 🎯 Run 34/127 - Sample Name        [████████░░ 67%]     │
├─────────────────────────────────────────────────────────┤
│ 📋 ACTIVITIES (What actually happened):                 │
│ • Run Number 34: Running Fe(III)_CA_100mV              │
│ • Kuntal says we need to realign Kalpha                │
│ • XES before realignment                                │
│                                                         │
│ 🤖 Original: calibration_run (high confidence)         │
│                                                         │
│ ✅ YOUR VALIDATION:                                     │
│ 🧪 [1] ◉ Sample Run     ⚙️ [2] ○ Calibration Run     │
│ 🎯 [3] ○ Alignment Run  🧪 [4] ○ Test Run            │
│ 🔧 [5] ○ Commissioning  ❓ [6] ○ Unknown Run         │
│                                                         │
│ [✓ Save & Next] [→ Skip] [⚡ Bulk Mode] [📈 Stats]     │
└─────────────────────────────────────────────────────────┘
```

### Navigation

- **← Previous / Next →**: Navigate between runs
- **Jump to**: Enter specific run number
- **Skip**: Skip unclear runs for later review
- **Progress bar**: Visual progress through experiment

### Validation Process

1. **Read activities**: The key information for making decisions
2. **Review original classification**: See automated classification and confidence
3. **Make decision**: 
   - ✅ Confirm if original is correct
   - 🔄 Select different classification if needed
4. **Add notes**: Optional context for your decision
5. **Save & continue**: Move to next run

### Classification Types

| Type | Description | Common Indicators |
|------|-------------|------------------|
| 🧪 **Sample Run** | Chemical samples, materials under investigation | Fe(III), organic compounds, foil samples |
| ⚙️ **Calibration Run** | Detector/instrument calibration | DARK measurements, pedestal runs, energy scans |
| 🎯 **Alignment Run** | Beam alignment and positioning | Focus adjustments, beam positioning, optical setup |
| 🧪 **Test Run** | Equipment testing and verification | Performance tests, detector tests, system checks |
| 🔧 **Commissioning Run** | Initial setup and configuration | New equipment setup, commissioning activities, installation |
| ❓ **Unknown Run** | Ambiguous or unclear activities | Insufficient information, mixed activities, vague descriptions |

### Bulk Operations

Access bulk mode for efficient validation of similar runs:

#### Quick Patterns
- **All DARK runs → calibration_run**: Automatically classify detector dark measurements
- **All water runs → background_run**: Classify water reference measurements  
- **All foil runs → sample_run**: Classify foil sample measurements
- **All test/verification runs → test_run**: Classify equipment testing runs
- **All commissioning/setup runs → commissioning_run**: Classify initial setup runs
- **Confirm high confidence**: Accept all high-confidence automated classifications

#### Custom Patterns
- **Search term**: Find runs containing specific text in activities
- **Target classification**: Apply classification to all matching runs
- **Preview**: See affected runs before applying

### Keyboard Shortcuts

#### Navigation
- `←/→` Arrow keys: Previous/Next run
- `Space`: Skip run
- `Enter`: Save & Next

#### Classification
- `1`: Select Sample Run
- `2`: Select Calibration Run
- `3`: Select Alignment Run
- `4`: Select Test Run
- `5`: Select Commissioning Run
- `6`: Select Unknown Run

#### Modes
- `B`: Toggle Bulk Mode
- `S`: Show Statistics

### Statistics & Progress

Track your validation progress with:
- **Completion percentage**: Runs validated vs total
- **Corrections made**: How many classifications you've changed
- **Accuracy rate**: Percentage of original classifications confirmed
- **Classification breakdown**: Distribution of run types
- **Recent corrections**: History of your recent changes

## Data Format

### Input: Markdown Files
The app expects markdown files with run sections in this format:
```markdown
### Run 34
**Duration**: 4.0 minutes
**Total entries**: 3 (1 unique)
**Activities**:
- Run Number 34: Running Fe(III)_CA_100mV
- XES before realignment
- XES Kalpha realigned

**Run classification**: calibration_run
**Confidence**: high
**Key evidence**: XES realignment activities
```

### Output: Validation JSON
Each experiment produces a validation file:
```json
{
  "experiment_id": "mfx10089532",
  "reviewer": "Jane Smith",
  "stats": {
    "total_runs": 127,
    "validated_runs": 85,
    "corrections_made": 23,
    "accuracy_rate": 81.9
  },
  "validations": {
    "34": {
      "original": "calibration_run",
      "validated": "sample_run",
      "method": "manual",
      "notes": "Primary purpose was sample measurement"
    }
  }
}
```

## File Structure

```
run-classification-validation-app/
├── app.py                          # Main Streamlit application
├── utils.py                        # Helper functions and parsers
├── requirements.txt                # Python dependencies
├── validations/                    # Generated validation JSON files
├── test_data/                      # Sample experiment files
└── README.md                       # This file
```

## Tips for Efficient Validation

### 🎯 Focus on Activities
The **Activities** section is the most important information. It tells you what actually happened during the run, which is the key to proper classification.

### ⚡ Use Bulk Operations
- Start with bulk operations for obvious patterns (DARK, water, etc.)
- This can validate 70-80% of runs automatically
- Focus manual effort on ambiguous cases

### 🔄 Work in Passes
1. **First pass**: Bulk operations for clear patterns
2. **Second pass**: Quick manual validation of remaining runs
3. **Third pass**: Detailed review of skipped/uncertain runs

### 📝 Add Notes for Complex Cases
When correcting classifications, add notes explaining your reasoning. This helps with:
- Quality control and review
- Training improvement for automated classification
- Understanding edge cases

### 📊 Monitor Progress
Use the statistics view to:
- Track completion across experiments
- Identify patterns in corrections
- Ensure consistent validation approach

## Troubleshooting

### App won't start
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Ensure Python version is 3.8 or higher
- Try: `streamlit --version` to verify Streamlit installation

### Files not loading
- Verify the data path points to correct directory
- Check that markdown files follow expected format
- Look for parsing errors in the terminal output

### Validation not saving
- Check write permissions in the `validations/` directory
- Ensure sufficient disk space
- Look for error messages in the Streamlit interface

### Performance issues
- Close other browser tabs to free memory
- Restart the Streamlit app: `Ctrl+C` then `streamlit run app.py`
- For very large experiments (>500 runs), consider validating in batches

## Development

### Adding New Bulk Patterns
Edit `utils.py` and add patterns to `get_bulk_patterns()`:

```python
# New pattern example
special_runs = []
for run in runs:
    if 'special_keyword' in run['activities']:
        special_runs.append(run['number'])

patterns.append({
    'name': 'All special runs → sample_run',
    'runs': special_runs,
    'classification': 'sample_run'
})
```

### Customizing Classification Types
Modify the classification options in `app.py`:
```python
classification_options = ["sample_run", "calibration_run", "alignment_run", "background_run", "custom_type"]
```

### Export Format
Validation JSON files can be processed by analysis scripts. The format is designed for easy integration with pandas:

```python
import json
import pandas as pd

# Load validation data
with open('validations/experiment_validation.json') as f:
    data = json.load(f)

# Convert to DataFrame for analysis
validations_df = pd.DataFrame.from_dict(data['validations'], orient='index')
```

## Contributing

This is a focused tool for run classification validation. If you need additional features:

1. **Fork the repository** for major changes
2. **Submit issues** for bugs or feature requests  
3. **Extend patterns** in `utils.py` for new classification logic
4. **Test thoroughly** with real experimental data

## Support

For issues or questions:
1. Check this README for common problems
2. Review error messages in the Streamlit interface
3. Check the terminal output for detailed error information
4. Test with sample data first before using production files

---

**Happy Validating! 🎯**

*This tool helps ensure high-quality run classifications for better experimental data analysis.*