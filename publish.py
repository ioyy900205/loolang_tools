#!/usr/bin/env python3
"""
Script to publish the WAV loo package to PyPI.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(f"Error: {e.stderr}")
        return None


def main():
    """Main publishing process."""
    print("🚀 Starting WAV loo package publishing process...\n")
    
    # Check if we're in the right directory
    if not Path("setup.py").exists() or not Path("wav_loo").exists():
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Step 1: Clean previous builds
    print("🧹 Cleaning previous builds...")
    run_command("rm -rf build/ dist/ *.egg-info/", "Cleaning build artifacts")
    
    # Step 2: Build the package
    print("\n🔨 Building package...")
    if not run_command("python3 -m build", "Building package"):
        print("❌ Build failed. Please check the errors above.")
        sys.exit(1)
    
    # Step 3: Check the package
    print("\n🔍 Checking package...")
    if not run_command("python3 -m twine check dist/*", "Checking package"):
        print("❌ Package check failed. Please fix the issues above.")
        sys.exit(1)
    
    # Step 4: Publish to PyPI
    print("\n📦 Package is ready for publishing!")
    print("Generated files:")
    for file in Path("dist").glob("*"):
        print(f"  - {file}")
    
    print("\n🚀 Publishing to PyPI...")
    if run_command("python3 -m twine upload --skip-existing dist/*", "Publishing to PyPI"):
        print("\n🎉 Successfully published to PyPI!")
        print("Your package is now available at: https://pypi.org/project/wav-loo/")
    else:
        print("❌ Publishing failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main() 