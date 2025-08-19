#!/usr/bin/env python3
"""
Demo script to show how validation data is structured.
This creates a sample validation file for testing.
"""

import json
from datetime import datetime
from pathlib import Path
import utils

def create_demo_validation():
    """Create a demo validation file to show the data structure"""
    
    # Parse a sample experiment
    experiment_file = Path("test_data/mfx10089532_full_enrichment.md")
    runs = utils.parse_experiment_file(experiment_file)
    
    print(f"📋 Loaded experiment with {len(runs)} runs")
    
    # Create demo validation data
    validation_data = {
        "experiment_id": "mfx10089532",
        "source_file": "mfx10089532_full_enrichment.md",
        "reviewer": "Demo User",
        "started_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "stats": {
            "total_runs": len(runs),
            "validated_runs": 6,
            "corrections_made": 3,
            "accuracy_rate": 50.0
        },
        "validations": {},
        "bulk_operations": []
    }
    
    # Add some sample validations
    sample_validations = [
        {
            "run": 7,
            "original": "alignment_run",
            "validated": "alignment_run",
            "notes": "Correct - beam alignment activities confirmed"
        },
        {
            "run": 8,
            "original": "calibration_run", 
            "validated": "calibration_run",
            "notes": "Correct - energy scan for calibration"
        },
        {
            "run": 19,
            "original": "calibration_run",
            "validated": "sample_run",
            "notes": "Corrected - Fe_foil_1e-3_ka_only is clearly a sample measurement"
        },
        {
            "run": 28,
            "original": "calibration_run",
            "validated": "background_run", 
            "notes": "Corrected - water runs are background measurements"
        },
        {
            "run": 34,
            "original": "calibration_run",
            "validated": "sample_run",
            "notes": "Corrected - despite realignment activities, primary purpose was Fe foil measurement"
        },
        {
            "run": 105,
            "original": "sample_run",
            "validated": "unknown_run",
            "notes": "Ambiguous - note says 'ignore this one, only half the data in it' - unclear purpose"
        }
    ]
    
    # Add validations to data structure
    for validation in sample_validations:
        validation_data["validations"][str(validation["run"])] = {
            "original": validation["original"],
            "validated": validation["validated"],
            "method": "manual",
            "notes": validation["notes"]
        }
    
    # Add a sample bulk operation
    validation_data["bulk_operations"] = [
        {
            "pattern": "All DARK runs → calibration_run",
            "applied_to": [14, 15, 17, 18, 20, 30, 55, 56, 59, 60, 102, 103, 115],
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    # Save demo validation file
    output_path = Path("validations/demo_validation.json")
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(validation_data, f, indent=2)
    
    print(f"💾 Created demo validation file: {output_path}")
    print(f"📊 Contains {len(validation_data['validations'])} individual validations (including unknown_run example)")
    print(f"⚡ Contains {len(validation_data['bulk_operations'])} bulk operations")
    
    # Show some sample runs for context
    print("\n📋 Sample runs from the experiment:")
    for run in runs[:5]:
        print(f"Run {run['number']}: {run['classification']} ({run['confidence']}) - {run.get('sample', 'No sample')}")
        print(f"  Activities: {run['activities'][:2]}{'...' if len(run['activities']) > 2 else ''}")
        print()
    
    # Show bulk pattern detection
    patterns = utils.get_bulk_patterns(runs)
    print(f"🚀 Detected {len(patterns)} bulk patterns:")
    for pattern in patterns:
        print(f"  • {pattern['name']}: {len(pattern['runs'])} runs")
    
    print(f"\n✨ Demo complete! Validation data structure ready for your analysis scripts.")

if __name__ == "__main__":
    create_demo_validation()