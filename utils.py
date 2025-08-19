import re
from pathlib import Path
from typing import List, Dict, Tuple, Any

def parse_experiment_file(filepath: Path) -> List[Dict]:
    """
    Parse a markdown experiment file and extract run data.
    Returns a list of dictionaries containing run information.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        raise Exception(f"Could not read file {filepath}: {e}")
    
    runs = []
    
    # Split content by run sections (### Run X)
    run_sections = re.split(r'\n### Run (\d+)', content)
    
    # Skip the first element (content before first run)
    for i in range(1, len(run_sections), 2):
        if i + 1 < len(run_sections):
            run_number = int(run_sections[i])
            run_content = run_sections[i + 1]
            
            run_data = parse_run_section(run_number, run_content)
            if run_data:
                runs.append(run_data)
    
    return sorted(runs, key=lambda x: x['number'])

def parse_run_section(run_number: int, content: str) -> Dict:
    """Parse individual run section and extract structured data"""
    run_data = {
        'number': run_number,
        'duration': '',
        'total_entries': '',
        'activities': [],
        'classification': '',
        'confidence': '',
        'key_evidence': '',
        'sample': ''
    }
    
    lines = content.strip().split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        # Stop at next run section
        if line.startswith('###'):
            break
        
        # Skip empty lines but continue parsing
        if not line:
            continue
            
        # Extract duration
        if line.startswith('**Duration**:'):
            run_data['duration'] = line.split(':', 1)[1].strip()
        
        # Extract total entries
        elif line.startswith('**Total entries**:'):
            run_data['total_entries'] = line.split(':', 1)[1].strip()
        
        # Track sections
        elif line == '**Activities**:':
            current_section = 'activities'
        elif line.startswith('**Run classification**:'):
            run_data['classification'] = line.split(':', 1)[1].strip()
            current_section = 'classification'
        elif line.startswith('**Confidence**:'):
            run_data['confidence'] = line.split(':', 1)[1].strip()
            current_section = 'classification'
        elif line.startswith('**Key evidence**:'):
            run_data['key_evidence'] = line.split(':', 1)[1].strip()
            current_section = 'classification'
        
        # Collect activities
        elif current_section == 'activities' and line.startswith('-'):
            activity = line[1:].strip()  # Remove the dash
            
            # Skip repeated entries notation
            if not activity.startswith('[Repeated') and activity:
                # Clean up activity text
                if activity.startswith('Run Number'):
                    # Extract the main activity from run number lines
                    if 'Running ' in activity:
                        parts = activity.split('Running ', 1)
                        if len(parts) > 1:
                            sample_name = parts[1].split(' Run ended')[0]
                            activity = f"Running {sample_name}"
                            # Extract sample name for the run
                            if not run_data['sample'] and sample_name:
                                run_data['sample'] = sample_name.strip()
                
                run_data['activities'].append(activity)
        
        # Extract sample name from activities (fallback)
        elif 'Running ' in line and not run_data['sample']:
            sample_match = re.search(r'Running ([^:]+)', line)
            if sample_match:
                sample_candidate = sample_match.group(1).strip()
                # Clean up common endings
                sample_candidate = sample_candidate.split(' Run ended')[0]
                sample_candidate = sample_candidate.split(' with')[0]  
                if sample_candidate:
                    run_data['sample'] = sample_candidate
    
    return run_data

def get_bulk_patterns(runs: List[Dict]) -> List[Dict]:
    """
    Identify common patterns in runs for bulk operations.
    Returns list of pattern dictionaries with affected run numbers.
    """
    patterns = []
    
    # Pattern 1: DARK runs
    dark_runs = []
    for run in runs:
        activities_str = ' '.join(run['activities']).upper()
        if 'DARK' in activities_str:
            dark_runs.append(run['number'])
    
    if dark_runs:
        patterns.append({
            'name': 'All DARK runs → calibration_run',
            'runs': dark_runs,
            'classification': 'calibration_run',
            'description': 'DARK measurements are typically calibration runs'
        })
    
    # Pattern 2: Water runs
    water_runs = []
    for run in runs:
        activities_str = ' '.join(run['activities']).lower()
        sample_str = run.get('sample', '').lower()
        if 'water' in activities_str or 'water' in sample_str or 'h2o' in activities_str:
            water_runs.append(run['number'])
    
    if water_runs:
        patterns.append({
            'name': 'All water runs → background_run',
            'runs': water_runs,
            'classification': 'background_run',
            'description': 'Water runs are typically background/reference measurements'
        })
    
    # Pattern 3: Empty/background runs
    empty_runs = []
    for run in runs:
        activities_str = ' '.join(run['activities']).lower()
        sample_str = run.get('sample', '').lower()
        if ('empty' in activities_str or 'empty' in sample_str or 
            'background' in activities_str or 'background' in sample_str):
            empty_runs.append(run['number'])
    
    if empty_runs:
        patterns.append({
            'name': 'All empty/background runs → background_run',
            'runs': empty_runs,
            'classification': 'background_run',
            'description': 'Empty and background measurements'
        })
    
    # Pattern 4: Foil runs (likely samples)
    foil_runs = []
    for run in runs:
        activities_str = ' '.join(run['activities']).lower()
        sample_str = run.get('sample', '').lower()
        if 'foil' in activities_str or 'foil' in sample_str:
            foil_runs.append(run['number'])
    
    if foil_runs:
        patterns.append({
            'name': 'All foil runs → sample_run',
            'runs': foil_runs,
            'classification': 'sample_run',
            'description': 'Foil measurements are typically sample runs'
        })
    
    # Pattern 5: Chemical formula runs (Fe(II), Fe(III), etc.)
    chemical_runs = []
    chemical_pattern = re.compile(r'\b[A-Z][a-z]?\([IVX]+\)')  # Matches Fe(III), Mn(II), etc.
    
    for run in runs:
        activities_str = ' '.join(run['activities'])
        sample_str = run.get('sample', '')
        if (chemical_pattern.search(activities_str) or 
            chemical_pattern.search(sample_str)):
            chemical_runs.append(run['number'])
    
    if chemical_runs:
        patterns.append({
            'name': 'All chemical sample runs → sample_run',
            'runs': chemical_runs,
            'classification': 'sample_run',
            'description': 'Runs with chemical formulas are typically sample measurements'
        })
    
    # Pattern 6: High confidence originals (confirm them)
    high_conf_runs = []
    for run in runs:
        if run.get('confidence', '').lower() == 'high':
            high_conf_runs.append(run['number'])
    
    if high_conf_runs:
        patterns.append({
            'name': 'Confirm all high confidence classifications',
            'runs': high_conf_runs,
            'classification': 'original',  # Keep original classification
            'description': 'Accept all high confidence automated classifications'
        })
    
    # Pattern 7: Alignment runs
    alignment_runs = []
    for run in runs:
        activities_str = ' '.join(run['activities']).lower()
        if ('alignment' in activities_str or 'align' in activities_str or 
            'focus' in activities_str or 'beam' in activities_str):
            alignment_runs.append(run['number'])
    
    if alignment_runs:
        patterns.append({
            'name': 'All alignment/focus runs → alignment_run',
            'runs': alignment_runs,
            'classification': 'alignment_run',
            'description': 'Runs with alignment or focus activities'
        })
    
    return patterns

def find_matching_runs(runs: List[Dict], search_term: str) -> List[int]:
    """
    Find runs that match a custom search term in their activities.
    Returns list of matching run numbers.
    """
    matching_runs = []
    search_term_lower = search_term.lower()
    
    for run in runs:
        activities_str = ' '.join(run['activities']).lower()
        sample_str = run.get('sample', '').lower()
        
        if (search_term_lower in activities_str or 
            search_term_lower in sample_str):
            matching_runs.append(run['number'])
    
    return matching_runs

def suggest_classification(run: Dict) -> Tuple[str, str]:
    """
    Suggest a classification for a run based on its activities.
    Returns (classification, reason) tuple.
    """
    activities_str = ' '.join(run['activities']).lower()
    sample_str = run.get('sample', '').lower()
    combined_text = activities_str + ' ' + sample_str
    
    # Check for DARK measurements
    if 'dark' in combined_text:
        return 'calibration_run', 'DARK measurements are typically calibration runs'
    
    # Check for water runs
    if 'water' in combined_text or 'h2o' in combined_text:
        return 'background_run', 'Water runs are typically background measurements'
    
    # Check for empty/background
    if 'empty' in combined_text or 'background' in combined_text:
        return 'background_run', 'Empty/background runs are reference measurements'
    
    # Check for chemical formulas (sample runs)
    chemical_pattern = re.compile(r'\b[A-Z][a-z]?\([IVX]+\)')
    if chemical_pattern.search(activities_str) or chemical_pattern.search(sample_str):
        return 'sample_run', 'Chemical formulas indicate sample measurements'
    
    # Check for foil runs
    if 'foil' in combined_text:
        return 'sample_run', 'Foil measurements are typically sample runs'
    
    # Check for alignment activities
    alignment_keywords = ['alignment', 'align', 'focus', 'beam positioning', 'calibration']
    if any(keyword in combined_text for keyword in alignment_keywords):
        # Distinguish between alignment and calibration
        if 'beam' in combined_text and ('focus' in combined_text or 'alignment' in combined_text):
            return 'alignment_run', 'Beam alignment and focus activities detected'
        elif 'pedestal' in combined_text or 'calibration' in combined_text:
            return 'calibration_run', 'Calibration activities detected'
    
    # Check for energy scans or spectrometer settings
    if ('energy' in combined_text and 'scan' in combined_text) or 'spectrometer' in combined_text:
        return 'calibration_run', 'Energy scans and spectrometer settings are calibration activities'
    
    # Check for unclear/minimal activities that suggest unknown classification
    if (not activities_str.strip() or 
        len(run.get('activities', [])) == 0 or
        (len(run.get('activities', [])) == 1 and len(activities_str.strip()) < 20)):
        return 'unknown_run', 'Insufficient or unclear activity information'
    
    # If nothing specific found, keep original
    original_classification = run.get('classification', 'sample_run')
    return original_classification, 'No clear pattern detected, keeping original classification'

def get_classification_hints() -> Dict[str, str]:
    """Return helpful hints for each classification type"""
    return {
        'sample_run': 'Chemical samples, materials under investigation, Fe(III), organic compounds',
        'calibration_run': 'DARK measurements, pedestal runs, energy scans, detector calibration',
        'alignment_run': 'Beam alignment, focus adjustments, positioning, optical setup',
        'background_run': 'Water, empty cell, reference measurements, baseline data',
        'unknown_run': 'Ambiguous activities, insufficient information, unclear purpose, mixed activities'
    }