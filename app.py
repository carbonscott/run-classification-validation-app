import streamlit as st
import json
import re
import os
import pandas as pd
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
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "detail"  # "list" or "detail"
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""
if 'classification_filter' not in st.session_state:
    st.session_state.classification_filter = "All"
if 'validation_status_filter' not in st.session_state:
    st.session_state.validation_status_filter = "All"
if 'selected_run_indices' not in st.session_state:
    st.session_state.selected_run_indices = []
if 'show_group_confirmation' not in st.session_state:
    st.session_state.show_group_confirmation = False

def get_validation_directory() -> str:
    """Get validation directory from environment variable or default"""
    return os.getenv('VALIDATION_DATA_DIR', 'validations')

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

def create_runs_dataframe(runs_data: List[Dict], validation_data: Dict, search_term: str = "", 
                         classification_filter: str = "All", status_filter: str = "All") -> Any:
    """Create a filtered dataframe for the list view"""
    
    # Create base dataframe
    df_data = []
    for i, run in enumerate(runs_data):
        # Get validation status
        run_str = str(run['number'])
        validation = validation_data["validations"].get(run_str, {})
        is_validated = bool(validation)
        validated_classification = validation.get('validated', run.get('classification', 'unknown'))
        
        # Truncate activities for display
        activities_text = " | ".join(run.get('activities', []))
        if len(activities_text) > 100:
            activities_text = activities_text[:100] + "..."
        
        df_data.append({
            'Run #': run['number'],
            'Sample': run.get('sample', ''),
            'Original': run.get('classification', 'unknown'),
            'Validated': validated_classification if is_validated else '',
            'Status': '✅ Validated' if is_validated else '⏳ Pending',
            'Confidence': run.get('confidence', ''),
            'Activities': activities_text,
            'original_index': i  # Keep track of original index for navigation
        })
    
    df = pd.DataFrame(df_data)
    
    # Apply filters
    if search_term:
        search_lower = search_term.lower()
        mask = (
            df['Sample'].str.lower().str.contains(search_lower, na=False) |
            df['Activities'].str.lower().str.contains(search_lower, na=False) |
            df['Original'].str.lower().str.contains(search_lower, na=False) |
            df['Validated'].str.lower().str.contains(search_lower, na=False)
        )
        df = df[mask]
    
    if classification_filter != "All":
        df = df[df['Original'] == classification_filter]
    
    if status_filter == "Validated":
        df = df[df['Status'].str.contains('✅')]
    elif status_filter == "Pending":
        df = df[df['Status'].str.contains('⏳')]
    
    return df

def get_unique_classifications(runs_data: List[Dict]) -> List[str]:
    """Get unique classification types from the data"""
    classifications = set()
    for run in runs_data:
        if run.get('classification'):
            classifications.add(run['classification'])
    return sorted(list(classifications))

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
    
    # Validation data directory configuration
    default_validation_dir = get_validation_directory()
    validation_data_dir = st.text_input(
        "Validation data directory:",
        value=default_validation_dir,
        help=f"Directory to store validation progress files. Default from VALIDATION_DATA_DIR env var or 'validations'"
    )
    
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
            validation_file = Path(validation_data_dir) / f"{selected_file.stem}_validation.json"
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
    
    # View mode toggle (only show if not in other modes)
    if not st.session_state.bulk_mode and not st.session_state.show_stats:
        current_view = "📋 List View" if st.session_state.view_mode == "detail" else "🔍 Detail View"
        if st.button(current_view, help="Switch between list and detail views"):
            st.session_state.view_mode = "list" if st.session_state.view_mode == "detail" else "detail"
            st.rerun()
    
    if st.button("⚡ Toggle Bulk Mode", help="Switch to bulk validation mode"):
        st.session_state.bulk_mode = not st.session_state.bulk_mode
        # Return to detail view when switching modes
        if st.session_state.bulk_mode:
            st.session_state.view_mode = "detail"
        st.rerun()
    
    if st.button("📈 Show Statistics", help="View detailed statistics"):
        st.session_state.show_stats = not st.session_state.show_stats
        # Return to detail view when switching modes
        if st.session_state.show_stats:
            st.session_state.view_mode = "detail"
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
                                   ["sample_run", "calibration_run", "alignment_run", "test_run", "commissioning_run", "unknown_run"])
    
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

elif st.session_state.view_mode == "list":
    # List view mode
    st.header("📋 Run List View")
    
    # Filter controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Search runs:",
            value=st.session_state.search_term,
            placeholder="Search activities, samples, classifications...",
            help="Search across run activities, sample names, and classifications"
        )
        if search_term != st.session_state.search_term:
            st.session_state.search_term = search_term
            st.rerun()
    
    with col2:
        # Get all classification types for filter
        all_classifications = ["sample_run", "calibration_run", "alignment_run", "test_run", "commissioning_run", "unknown_run"]
        classification_options = ["All"] + all_classifications
        
        classification_filter = st.selectbox(
            "Classification:",
            classification_options,
            index=classification_options.index(st.session_state.classification_filter) if st.session_state.classification_filter in classification_options else 0
        )
        if classification_filter != st.session_state.classification_filter:
            st.session_state.classification_filter = classification_filter
            st.rerun()
    
    with col3:
        status_filter = st.selectbox(
            "Status:",
            ["All", "Validated", "Pending"],
            index=["All", "Validated", "Pending"].index(st.session_state.validation_status_filter)
        )
        if status_filter != st.session_state.validation_status_filter:
            st.session_state.validation_status_filter = status_filter
            st.rerun()
    
    # Create filtered dataframe
    df = create_runs_dataframe(
        runs_data, 
        validation_data, 
        st.session_state.search_term,
        st.session_state.classification_filter,
        st.session_state.validation_status_filter
    )
    
    
    # Show summary with active filters
    total_filtered = len(df)
    total_runs = len(runs_data)
    
    # Build filter summary
    active_filters = []
    if st.session_state.search_term:
        active_filters.append(f"🔍 '{st.session_state.search_term}'")
    if st.session_state.classification_filter != "All":
        active_filters.append(f"📂 {st.session_state.classification_filter}")
    if st.session_state.validation_status_filter != "All":
        active_filters.append(f"📋 {st.session_state.validation_status_filter}")
    
    if active_filters:
        col_info, col_clear = st.columns([4, 1])
        with col_info:
            filter_text = " | ".join(active_filters)
            st.info(f"Showing {total_filtered} of {total_runs} runs | Filters: {filter_text}")
        with col_clear:
            if st.button("🗑️ Clear Filters", help="Reset all filters"):
                st.session_state.search_term = ""
                st.session_state.classification_filter = "All"
                st.session_state.validation_status_filter = "All"
                st.rerun()
    else:
        st.info(f"Showing {total_filtered} of {total_runs} runs (no filters applied)")
    
    # Display the table
    if total_filtered > 0:
        # Configure dataframe display
        if 'df_key' not in st.session_state:
            st.session_state.df_key = 0
            
        event = st.dataframe(
            df.drop('original_index', axis=1),  # Hide internal column
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="multi-row",
            key=f"runs_dataframe_{st.session_state.df_key}"
        )
        
        # Handle row selection and update session state
        if event.selection and event.selection.rows:
            selected_rows = event.selection.rows
            st.session_state.selected_run_indices = [df.iloc[i]['original_index'] for i in selected_rows]
        else:
            st.session_state.selected_run_indices = []
        
        # Contextual panels based on selection count
        num_selected = len(st.session_state.selected_run_indices)
        
        if num_selected == 1:
            # Single selection - Show "View Details" panel
            selected_idx = st.session_state.selected_run_indices[0]
            selected_run = runs_data[selected_idx]
            run_number = selected_run['number']
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(f"👁️ **View Run {run_number}**")
            with col2:
                if st.button("View Details", type="primary", help=f"Go to detail view for Run {run_number}"):
                    st.session_state.current_run = selected_idx
                    st.session_state.view_mode = "detail"
                    st.rerun()
        
        elif num_selected > 1:
            # Multiple selection - Show group validation panel
            st.info(f"🔄 **Group Validate {num_selected} runs**")
            
            # Simple one-row layout
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                classification_options = ["sample_run", "calibration_run", "alignment_run", "test_run", "commissioning_run", "unknown_run"]
                classification_labels = [
                    "🧪 Sample Run",
                    "⚙️ Calibration Run",  
                    "🎯 Alignment Run",
                    "🧪 Test Run",
                    "🔧 Commissioning Run",
                    "❓ Unknown Run"
                ]
                
                group_classification = st.selectbox(
                    "Classification:",
                    classification_options,
                    format_func=lambda x: classification_labels[classification_options.index(x)],
                    key="group_classification_select"
                )
            
            with col2:
                if st.button("✅ Validate All", type="primary", help=f"Validate all {num_selected} selected runs"):
                    st.session_state.show_group_confirmation = True
                    st.rerun()
            
            with col3:
                if st.button("❌ Cancel", help="Clear selection"):
                    st.session_state.selected_run_indices = []
                    # Force dataframe reset
                    st.session_state.df_key += 1
                    st.rerun()
            
            # Group notes field (second row)
            st.text_area(
                "📝 Group Notes (optional):",
                placeholder="Explain why these runs are grouped together (e.g., 'All runs during detector calibration', 'Same sample preparation batch')...",
                help="Optional notes that will be applied to all selected runs",
                key="group_notes_input",
                height=80
            )
    else:
        st.warning("No runs match the current filters.")
    
    
    # Group validation confirmation dialog
    if st.session_state.show_group_confirmation:
        st.divider()
        st.subheader("⚠️ Confirm Group Validation")
        
        # Get the selected classification and notes from session state
        target_classification = st.session_state.get('group_classification_select', 'sample_run')
        group_notes = st.session_state.get('group_notes_input', '').strip()
        
        # Show detailed preview of what will change
        st.warning(f"**You are about to validate {len(st.session_state.selected_run_indices)} runs as '{target_classification}'**")
        
        # Show preview table
        preview_data = []
        for idx in st.session_state.selected_run_indices:
            if idx < len(runs_data):
                run = runs_data[idx]
                run_str = str(run['number'])
                existing_validation = validation_data["validations"].get(run_str, {})
                current_classification = existing_validation.get('validated', run.get('classification', 'unknown'))
                
                preview_data.append({
                    'Run #': run['number'],
                    'Sample': run.get('sample', 'N/A'),
                    'Current': current_classification,
                    'New': target_classification,
                    'Change': '✓' if current_classification != target_classification else '→'
                })
        
        if preview_data:
            preview_df = pd.DataFrame(preview_data)
            st.dataframe(preview_df, use_container_width=True, hide_index=True)
        
        # Show custom notes if provided
        if group_notes:
            st.info(f"**📝 Group Notes:** {group_notes}")
        
        # Confirmation buttons
        col_confirm, col_cancel_conf = st.columns(2)
        
        with col_confirm:
            if st.button("🚀 Confirm & Apply", type="primary", help="Apply group validation to all selected runs"):
                # Apply group validation
                changes_made = 0
                for idx in st.session_state.selected_run_indices:
                    if idx < len(runs_data):
                        run = runs_data[idx]
                        run_str = str(run['number'])
                        
                        # Create or update validation entry
                        # Use custom notes if provided, otherwise fallback to generic message
                        notes_text = group_notes if group_notes else f"Group validation applied to {len(st.session_state.selected_run_indices)} runs"
                        
                        validation_data["validations"][run_str] = {
                            "original": run.get('classification', 'unknown'),
                            "validated": target_classification,
                            "method": "group_validation",
                            "notes": notes_text
                        }
                        changes_made += 1
                
                # Record the group operation
                validation_data["bulk_operations"].append({
                    "pattern": f"Group validation: {len(st.session_state.selected_run_indices)} runs → {target_classification}",
                    "applied_to": [runs_data[idx]['number'] for idx in st.session_state.selected_run_indices if idx < len(runs_data)],
                    "timestamp": datetime.now().isoformat(),
                    "method": "group_validation"
                })
                
                # Save the validation file
                save_validation_file(validation_file, validation_data)
                
                # Reset state and show success
                st.session_state.selected_run_indices = []
                st.session_state.show_group_confirmation = False
                st.session_state.df_key += 1  # Reset dataframe
                
                st.success(f"✅ Successfully validated {changes_made} runs as '{target_classification}'!")
                st.rerun()
        
        with col_cancel_conf:
            if st.button("❌ Cancel", help="Cancel group validation and return to selection"):
                st.session_state.show_group_confirmation = False
                st.rerun()

else:
    # Individual run validation mode
    if not runs_data:
        st.error("No runs found in the selected experiment file.")
        st.stop()
    
    # Back to list button
    if st.button("← Back to List", help="Return to the run list view"):
        st.session_state.view_mode = "list"
        st.rerun()
    
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
            classification_options = ["sample_run", "calibration_run", "alignment_run", "test_run", "commissioning_run", "unknown_run"]
            classification_labels = [
                "🧪 [1] Sample Run (chemical samples, materials)",
                "⚙️ [2] Calibration Run (DARK, pedestal, energy)",  
                "🎯 [3] Alignment Run (beam alignment, focus)",
                "🧪 [4] Test Run (equipment testing, verification)",
                "🔧 [5] Commissioning Run (setup, initial config)",
                "❓ [6] Unknown Run (ambiguous, unclear purpose)"
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


# Navigation help
st.divider()
with st.expander("🖱️ Navigation Guide", expanded=False):
    st.markdown("""
    **List View Navigation:**
    - Click rows to select them (Ctrl/Cmd+click for multi-select on some systems)
    - Use selection buttons: ☑️ Select All, 🔲 Clear Selection, 🔍 Select Pending
    - When 1 run selected: Use 👁️ View Details button to see full details
    - When 2+ runs selected: Group validation panel appears automatically
    
    **Detail View Navigation:**
    - Use ← Previous/Next → buttons to navigate runs
    - Use the numbered radio buttons [1-6] for quick classification selection
    - Use Skip button to move without saving
    - Use Save & Next button to save and proceed
    - Use Jump to field to go directly to a specific run
    
    **Group Validation:**
    - Select multiple runs → Choose classification → ✅ Apply to All
    - Preview dialog shows what will change before confirming
    - Perfect for validating similar runs together (e.g., all DARK runs)
    
    **Modes:**
    - 📋 List View: Browse and select runs with filtering
    - 🔍 Detail View: Individual run validation with full context
    - ⚡ Bulk Mode: Apply patterns to multiple runs at once
    - 📈 Statistics: View validation progress and accuracy
    """)

# Auto-save current state
save_validation_file(validation_file, validation_data)