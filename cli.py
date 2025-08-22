#!/usr/bin/env python3
"""
Command Line Interface for Run Classification Validator

This module provides a CLI for launching the Streamlit-based run classification
validation application with configurable parameters.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def get_version():
    """Get the version from pyproject.toml or return a default."""
    try:
        import tomllib
        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)
            return data["project"]["version"]
    except (ImportError, FileNotFoundError, KeyError):
        return "1.0.0"


def validate_directory(path_str):
    """Validate that a directory path exists or can be created."""
    if not path_str:
        return None
    
    path = Path(path_str).expanduser().resolve()
    
    # If it's an existing directory, great
    if path.exists() and path.is_dir():
        return str(path)
    
    # If it doesn't exist, try to create it
    try:
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
    except (PermissionError, OSError) as e:
        raise argparse.ArgumentTypeError(f"Cannot create directory '{path}': {e}")


def validate_port(port_str):
    """Validate port number."""
    try:
        port = int(port_str)
        if 1024 <= port <= 65535:
            return port
        raise ValueError("Port must be between 1024 and 65535")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid port: {port_str}")


def setup_argument_parser():
    """Set up and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="run-classification-validator",
        description="Launch the Run Classification Validator Streamlit application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --data-path /path/to/experiments
  %(prog)s -d /experiments -v /custom/validations -p 8502
  %(prog)s --reviewer "Jane Doe" --port 8503

Environment Variables:
  VALIDATION_DATA_DIR    Directory for validation progress files (default: validations)

For more information, see the README.md file.
        """,
    )

    # Data configuration
    parser.add_argument(
        "-d", "--data-path",
        type=validate_directory,
        help="Path to directory containing experiment markdown files",
    )
    
    parser.add_argument(
        "-v", "--validation-dir",
        type=validate_directory,
        help="Directory to store validation progress files (overrides VALIDATION_DATA_DIR)",
    )
    
    parser.add_argument(
        "-r", "--reviewer",
        type=str,
        help="Reviewer name to record with validations",
    )

    # Server configuration
    parser.add_argument(
        "-p", "--port",
        type=validate_port,
        default=8501,
        help="Port for Streamlit server (default: 8501)",
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host for Streamlit server (default: localhost)",
    )

    # Other options
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't automatically open browser",
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run in debug mode with additional logging",
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
    )

    return parser


def set_environment_variables(args):
    """Set environment variables based on command line arguments."""
    env_vars = {}
    
    # Set validation directory if specified
    if args.validation_dir:
        env_vars["VALIDATION_DATA_DIR"] = args.validation_dir
        print(f"📁 Using validation directory: {args.validation_dir}")
    
    # Set reviewer name if specified
    if args.reviewer:
        env_vars["REVIEWER_NAME"] = args.reviewer
        print(f"👤 Using reviewer name: {args.reviewer}")
    
    # Add to current environment
    for key, value in env_vars.items():
        os.environ[key] = value
    
    return env_vars


def launch_streamlit_app(args):
    """Launch the Streamlit application with the specified configuration."""
    # Find the app.py file
    app_path = Path(__file__).parent / "app.py"
    if not app_path.exists():
        print(f"❌ Error: Could not find app.py at {app_path}")
        sys.exit(1)
    
    # Build streamlit command
    cmd = [
        "streamlit", "run", str(app_path),
        "--server.port", str(args.port),
        "--server.address", args.host,
    ]
    
    if args.no_browser:
        cmd.extend(["--server.headless", "true"])
    
    if args.debug:
        cmd.extend(["--logger.level", "debug"])
    
    # Print startup information
    print("🎯 Starting Run Classification Validator...")
    if args.data_path:
        print(f"📂 Data path: {args.data_path}")
    if args.reviewer:
        print(f"👤 Reviewer: {args.reviewer}")
    print(f"🌐 Server: http://{args.host}:{args.port}")
    print("⚡ Use Ctrl+C to stop the application")
    print("")
    
    # Launch the application
    try:
        if args.debug:
            print(f"🔧 Running command: {' '.join(cmd)}")
        
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        sys.exit(0)
    except FileNotFoundError:
        print("❌ Error: Streamlit not found. Please install with: pip install streamlit")
        sys.exit(1)


def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import streamlit
        return True
    except ImportError:
        print("❌ Error: Streamlit not found.")
        print("Please install dependencies with: pip install streamlit")
        print("Or install this package with: pip install .")
        return False


def main():
    """Main entry point for the CLI."""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Set environment variables
    set_environment_variables(args)
    
    # Launch the application
    launch_streamlit_app(args)


if __name__ == "__main__":
    main()