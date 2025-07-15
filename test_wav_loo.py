#!/usr/bin/env python3
"""
Test script for WAV Finder functionality.
"""

import os
import tempfile
from pathlib import Path
from wav_loo import WavFinder


def test_local_path():
    """Test finding WAV files from local path."""
    print("Testing local path functionality...")
    
    # Create a temporary directory with some test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create some test files
        (temp_path / "test1.wav").touch()
        (temp_path / "test2.WAV").touch()
        (temp_path / "test3.txt").touch()
        (temp_path / "subdir").mkdir()
        (temp_path / "subdir" / "test4.wav").touch()
        
        # Test the finder
        finder = WavFinder()
        wav_files = finder.find_wav_files(str(temp_path))
        
        print(f"Found {len(wav_files)} WAV files:")
        for wav_file in wav_files:
            print(f"  - {wav_file}")
        
        # Verify we found the expected files
        expected_files = [
            str(temp_path / "test1.wav"),
            str(temp_path / "test2.WAV"),
            str(temp_path / "subdir" / "test4.wav")
        ]
        
        assert len(wav_files) == 3, f"Expected 3 files, got {len(wav_files)}"
        for expected in expected_files:
            assert expected in wav_files, f"Expected {expected} not found"
        
        print("✓ Local path test passed!")


def test_single_file():
    """Test finding a single WAV file."""
    print("Testing single file functionality...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_file = temp_path / "single_test.wav"
        test_file.touch()
        
        finder = WavFinder()
        wav_files = finder.find_wav_files(str(test_file))
        
        print(f"Found {len(wav_files)} WAV files:")
        for wav_file in wav_files:
            print(f"  - {wav_file}")
        
        assert len(wav_files) == 1, f"Expected 1 file, got {len(wav_files)}"
        assert str(test_file) in wav_files, f"Expected {test_file} not found"
        
        print("✓ Single file test passed!")


def test_non_wav_file():
    """Test handling of non-WAV files."""
    print("Testing non-WAV file handling...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_file = temp_path / "test.txt"
        test_file.touch()
        
        finder = WavFinder()
        wav_files = finder.find_wav_files(str(test_file))
        
        print(f"Found {len(wav_files)} WAV files:")
        for wav_file in wav_files:
            print(f"  - {wav_file}")
        
        assert len(wav_files) == 0, f"Expected 0 files, got {len(wav_files)}"
        
        print("✓ Non-WAV file test passed!")


def main():
    """Run all tests."""
    print("Running WAV Finder tests...\n")
    
    try:
        test_local_path()
        print()
        test_single_file()
        print()
        test_non_wav_file()
        print()
        print("🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 