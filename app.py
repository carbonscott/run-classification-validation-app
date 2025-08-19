import streamlit as st
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import utils

# Configure page
st.set_page_config(
    page_title="Run Classification Validator",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if 'current_run' not in st.session_state:
    st.session_state.current_run = 0
if 'bulk_mode' not in st.session_state:
    st.session_state.bulk_mode = False
if 'show_stats' not in st.session_state:
    st.session_state.show_stats = False

def load_validation_file(validation_path: Path) -> Dict:
    """Load existing validation JSON or create new one"""
    if validation_path.exists():
        with open(validation_path, 'r') as f:
            return json.load(f)
    return {
        "experiment_id": "",
        "source_file": "",
        "reviewer": "",
        "started_at": datetime.now().isoformat(),
        "last_updated": "",
        "stats": {
            "total_runs": 0,
            "validated_runs": 0,
            "corrections_made": 0,
            "accuracy_rate": 0.0
        },
        "validations": {},
        "bulk_operations": []
    }

def save_validation_file(validation_path: Path, data: Dict):
    """Save validation data to JSON file"""
    data["last_updated"] = datetime.now().isoformat()
    validation_path.parent.mkdir(parents=True, exist_ok=True)
    with open(validation_path, 'w') as f:
        json.dump(data, f, indent=2)

def get_validation_stats(validations: Dict, total_runs: int) -> Dict:
    """Calculate validation statistics"""
    validated_count = len(validations)
    corrections = sum(1 for v in validations.values() 
                     if v['original'] != v['validated'])
    accuracy = ((validated_count - corrections) / validated_count * 100) if validated_count > 0 else 0
    
    return {
        "total_runs": total_runs,
        "validated_runs": validated_count,
        "corrections_made": corrections,
        "accuracy_rate": accuracy
    }

# Title and header
st.title("🎯 Run Classification Validator")
st.markdown("---")

# Sidebar: File selection and configuration
with st.sidebar:
    st.header("📁 Configuration")
    
    data_path = st.text_input(
        "Path to experiment files:",
        value="/sdf/data/lcls/ds/prj/prjcwang31/results/proj-peaknet-1m/fully_enriched_experiments",
        help="Directory containing the markdown experiment files"
    )
    
    reviewer_name = st.text_input("Your name:", value="Reviewer")
    
    # File selection
    if Path(data_path).exists():
        md_files = sorted(list(Path(data_path).glob("*_full_enrichment.md")))
        if md_files:
            selected_file_name = st.selectbox(
                "Select experiment:",
                [f.name for f in md_files],
                help="Choose an experiment file to validate"
            )
            selected_file = Path(data_path) / selected_file_name
            
            # Load validation file
            validation_file = Path("validations") / f"{selected_file.stem}_validation.json"
            validation_data = load_validation_file(validation_file)
            
            if validation_data["experiment_id"] == "":
                validation_data["experiment_id"] = selected_file.stem
                validation_data["source_file"] = selected_file_name
                validation_data["reviewer"] = reviewer_name
        else:
            st.error("No experiment files found in the specified directory!")
            st.stop()
    else:
        st.error("Directory not found!")
        st.stop()

    st.divider()
    
    # Load and parse experiment data
    try:
        runs_data = utils.parse_experiment_file(selected_file)
        validation_data["stats"] = get_validation_stats(
            validation_data["validations"], 
            len(runs_data)
        )
    except Exception as e:
        st.error(f"Error parsing file: {e}")
        st.stop()
    
    # Statistics
    st.header("📊 Progress")
    stats = validation_data["stats"]
    st.metric("Progress", f"{stats['validated_runs']}/{stats['total_runs']}")
    st.metric("Corrections Made", stats['corrections_made'])
    st.metric("Accuracy Rate", f"{stats['accuracy_rate']:.1f}%")
    
    # Mode toggles
    st.divider()
    if st.button("⚡ Toggle Bulk Mode", help="Switch to bulk validation mode"):
        st.session_state.bulk_mode = not st.session_state.bulk_mode
        st.rerun()
    
    if st.button("📈 Show Statistics", help="View detailed statistics"):
        st.session_state.show_stats = not st.session_state.show_stats
        st.rerun()
    
    # Export button
    st.divider()
    if st.button("💾 Export Validation", help="Download validation JSON"):
        save_validation_file(validation_file, validation_data)
        st.success("Validation saved!")
        st.download_button(
            "Download JSON",
            data=json.dumps(validation_data, indent=2),
            file_name=f"{validation_data['experiment_id']}_validation.json",
            mime="application/json"
        )

# Main content area
if st.session_state.show_stats:
    # Statistics view
    st.header("📈 Detailed Statistics")
    
    # Classification breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Classifications")
        original_counts = {}
        for run in runs_data:
            cls = run.get('classification', 'unknown')
            original_counts[cls] = original_counts.get(cls, 0) + 1
        
        for cls, count in original_counts.items():
            st.write(f"• {cls}: {count}")
    
    with col2:
        st.subheader("Validated Classifications") 
        validated_counts = {}
        for validation in validation_data["validations"].values():
            cls = validation['validated']
            validated_counts[cls] = validated_counts.get(cls, 0) + 1
        
        for cls, count in validated_counts.items():
            st.write(f"• {cls}: {count}")
    
    # Recent corrections
    st.subheader("Recent Corrections")
    corrections = [(k, v) for k, v in validation_data["validations"].items() 
                  if v['original'] != v['validated']]
    
    if corrections:
        for run_num, correction in corrections[-10:]:  # Last 10
            st.write(f"Run {run_num}: {correction['original']} → {correction['validated']}")
    else:
        st.write("No corrections made yet.")

elif st.session_state.bulk_mode:
    # Bulk operations mode
    st.header("⚡ Bulk Operations")
    
    # Get bulk patterns
    bulk_patterns = utils.get_bulk_patterns(runs_data)
    
    st.subheader("🚀 Quick Patterns")
    for i, pattern in enumerate(bulk_patterns):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"**{pattern['name']}**")
            st.caption(f"Affects {len(pattern['runs'])} runs: {pattern['runs'][:5]}{'...' if len(pattern['runs']) > 5 else ''}")
        
        with col2:
            if st.button(f"Preview {i}", help="Preview changes"):
                st.session_state[f"preview_{i}"] = True
        
        with col3:
            if st.button(f"Apply {i}", type="primary", help="Apply this pattern"):
                # Apply bulk operation
                for run_num in pattern['runs']:
                    run_str = str(run_num)
                    if run_str not in validation_data["validations"]:
                        # Find the original run data
                        original_run = next((r for r in runs_data if r['number'] == run_num), None)
                        if original_run:
                            validation_data["validations"][run_str] = {
                                "original": original_run.get('classification', 'unknown'),
                                "validated": pattern['classification'] if pattern['classification'] != 'original' else original_run.get('classification', 'unknown'),
                                "method": "bulk_pattern",
                                "notes": f"Applied pattern: {pattern['name']}"
                            }
                
                # Record bulk operation
                validation_data["bulk_operations"].append({
                    "pattern": pattern['name'],
                    "applied_to": pattern['runs'],
                    "timestamp": datetime.now().isoformat()
                })
                
                save_validation_file(validation_file, validation_data)
                st.success(f"Applied pattern to {len(pattern['runs'])} runs!")
                st.rerun()
    
    # Custom pattern
    st.subheader("🎯 Custom Pattern")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("Activity contains:", placeholder="e.g., Fe(III)")
    
    with col2:
        target_class = st.selectbox("Classification:", 
                                   ["sample_run", "calibration_run", "alignment_run", "background_run"])
    
    with col3:
        if search_term and st.button("Apply Custom"):
            matching_runs = utils.find_matching_runs(runs_data, search_term)
            
            for run_num in matching_runs:
                run_str = str(run_num)
                original_run = next((r for r in runs_data if r['number'] == run_num), None)
                if original_run:
                    validation_data["validations"][run_str] = {
                        "original": original_run.get('classification', 'unknown'),
                        "validated": target_class,
                        "method": "custom_pattern",
                        "notes": f"Custom pattern: activities containing '{search_term}'"
                    }
            
            validation_data["bulk_operations"].append({
                "pattern": f"Custom: activities containing '{search_term}' → {target_class}",
                "applied_to": matching_runs,
                "timestamp": datetime.now().isoformat()
            })
            
            save_validation_file(validation_file, validation_data)
            st.success(f"Applied custom pattern to {len(matching_runs)} runs!")
            st.rerun()

else:
    # Individual run validation mode
    if not runs_data:
        st.error("No runs found in the selected experiment file.")
        st.stop()
    
    # Navigation controls
    col1, col2, col3, col4, col5 = st.columns([1, 1, 4, 1, 1])
    
    with col1:
        if st.button("← Previous") and st.session_state.current_run > 0:
            st.session_state.current_run -= 1
            st.rerun()
    
    with col2:
        if st.button("Next →") and st.session_state.current_run < len(runs_data) - 1:
            st.session_state.current_run += 1
            st.rerun()
    
    with col3:
        # Progress bar
        progress = (st.session_state.current_run + 1) / len(runs_data)
        st.progress(progress, text=f"Run {st.session_state.current_run + 1} of {len(runs_data)} ({progress:.1%})")
    
    with col4:
        if st.button("Skip"):
            if st.session_state.current_run < len(runs_data) - 1:
                st.session_state.current_run += 1
                st.rerun()
    
    with col5:
        # Jump to run
        jump_to = st.number_input("Jump to:", min_value=1, max_value=len(runs_data), value=st.session_state.current_run + 1) - 1
        if jump_to != st.session_state.current_run:
            st.session_state.current_run = jump_to
            st.rerun()
    
    # Current run data
    if st.session_state.current_run < len(runs_data):
        current_run = runs_data[st.session_state.current_run]
        run_number = current_run['number']
        run_str = str(run_number)
        
        # Header
        st.header(f"🔬 Run {run_number}")
        if current_run.get('sample'):
            st.subheader(f"Sample: {current_run['sample']}")
        
        # Run details and activities
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📊 Run Details")
            if current_run.get('duration'):
                st.write(f"**Duration:** {current_run['duration']}")
            if current_run.get('total_entries'):
                st.write(f"**Entries:** {current_run['total_entries']}")
        
        with col2:
            st.subheader("🤖 Original Classification")
            st.info(f"**{current_run.get('classification', 'Unknown')}**")
            if current_run.get('confidence'):
                st.write(f"Confidence: {current_run['confidence']}")
            if current_run.get('key_evidence'):
                st.caption(f"Evidence: {current_run['key_evidence']}")
        
        # Activities (key information for validation)
        st.subheader("📋 Activities")
        with st.container(border=True):
            activities = current_run.get('activities', [])
            if activities:
                for activity in activities:
                    if isinstance(activity, str) and activity.strip():
                        st.write(f"• {activity.strip()}")
            else:
                st.write("No activities recorded for this run.")
        
        # Validation interface
        st.divider()
        st.subheader("✅ Your Validation")
        
        # Get existing validation if it exists
        existing_validation = validation_data["validations"].get(run_str, {})
        current_classification = existing_validation.get('validated', current_run.get('classification', 'sample_run'))
        current_notes = existing_validation.get('notes', '')
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Classification options with keyboard hints
            classification_options = ["sample_run", "calibration_run", "alignment_run", "background_run", "unknown_run"]
            classification_labels = [
                "🧪 [1] Sample Run (chemical samples, materials)",
                "⚙️ [2] Calibration Run (DARK, pedestal, energy)",  
                "🎯 [3] Alignment Run (beam alignment, focus)",
                "🔍 [4] Background Run (water, empty, reference)",
                "❓ [5] Unknown Run (ambiguous, unclear purpose)"
            ]
            
            selected_classification = st.radio(
                "Classification:",
                classification_options,
                index=classification_options.index(current_classification) if current_classification in classification_options else 0,
                format_func=lambda x: classification_labels[classification_options.index(x)]
            )
            
            # Notes
            notes = st.text_area(
                "Notes (optional):",
                value=current_notes,
                placeholder="Add any additional context or reasoning..."
            )
        
        with col2:
            # Quick suggestion based on activities
            suggestion, reason = utils.suggest_classification(current_run)
            if suggestion != current_run.get('classification'):
                st.info(f"💡 **Suggestion:** {suggestion}")
                st.caption(reason)
            
            # Validation actions
            st.write("")  # Spacing
            col_save, col_skip = st.columns(2)
            
            with col_save:
                if st.button("✓ Save & Next", type="primary", help="Save validation and move to next run"):
                    # Save validation
                    validation_data["validations"][run_str] = {
                        "original": current_run.get('classification', 'unknown'),
                        "validated": selected_classification,
                        "method": "manual",
                        "notes": notes
                    }
                    
                    save_validation_file(validation_file, validation_data)
                    
                    # Move to next run
                    if st.session_state.current_run < len(runs_data) - 1:
                        st.session_state.current_run += 1
                    
                    st.rerun()
            
            with col_skip:
                if st.button("→ Skip Run", help="Skip this run without saving"):
                    if st.session_state.current_run < len(runs_data) - 1:
                        st.session_state.current_run += 1
                        st.rerun()

# Keyboard shortcuts info
st.divider()
with st.expander("⌨️ Keyboard Shortcuts", expanded=False):
    st.markdown("""
    **Navigation:**
    - `←/→` Arrow keys: Previous/Next run
    - `Space`: Skip run
    - `Enter`: Save & Next (when validation is selected)
    
    **Classification:**
    - `1`: Select Sample Run
    - `2`: Select Calibration Run  
    - `3`: Select Alignment Run
    - `4`: Select Background Run
    - `5`: Select Unknown Run
    
    **Modes:**
    - `B`: Toggle Bulk Mode
    - `S`: Show Statistics
    """)

# Auto-save current state
save_validation_file(validation_file, validation_data)