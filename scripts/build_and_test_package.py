#!/usr/bin/env python3
"""
Script to build and test the package locally before publishing to PyPI.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def clean_build_artifacts():
    """Clean up build artifacts."""
    print("\n🧹 Cleaning build artifacts...")
    artifacts = ['build', 'dist', '*.egg-info']
    for artifact in artifacts:
        for path in Path('.').glob(artifact):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"Removed directory: {path}")
            else:
                path.unlink()
                print(f"Removed file: {path}")

def main():
    """Main function to build and test package."""
    print("🚀 Building and testing EdgeX Python SDK package")
    
    # Change to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Clean previous builds
    clean_build_artifacts()
    
    # Install build dependencies
    if not run_command("pip install --upgrade pip build twine", "Installing build dependencies"):
        return 1
    
    # Build the package
    if not run_command("python -m build", "Building package"):
        return 1
    
    # Check the package
    if not run_command("twine check dist/*", "Checking package"):
        return 1
    
    # List built files
    print("\n📦 Built packages:")
    dist_dir = Path("dist")
    if dist_dir.exists():
        for file in dist_dir.iterdir():
            print(f"  - {file.name}")
    
    print("\n✅ Package build and check completed successfully!")
    print("\n📋 Next steps:")
    print("1. Test install locally: pip install dist/edgex_python_sdk-*.whl")
    print("2. Upload to Test PyPI: twine upload --repository testpypi dist/*")
    print("3. Test install from Test PyPI: pip install --index-url https://test.pypi.org/simple/ edgex-python-sdk")
    print("4. If everything works, upload to PyPI: twine upload dist/*")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
