#!/usr/bin/env python3
"""Runner script for all tests in the AI Research Agent project."""
import os
import sys
import unittest
import argparse
from pathlib import Path

def discover_and_run_tests(verbose=False, pattern="test_*.py"):
    """Discover and run all tests in the project."""
    # Configure test verbosity
    verbosity = 2 if verbose else 1
    
    # Find all tests in the tests directory
    test_dir = Path(__file__).parent / "tests"
    if not test_dir.exists():
        print(f"Error: Test directory {test_dir} not found.")
        return False
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(str(test_dir), pattern=pattern)
    
    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Return True if all tests passed
    return result.wasSuccessful()

def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="Run tests for AI Research Agent")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show verbose test output")
    parser.add_argument("--pattern", "-p", type=str, default="test_*.py", 
                      help="Pattern to match test files (default: test_*.py)")
    
    args = parser.parse_args()
    
    print("Running AI Research Agent tests...")
    success = discover_and_run_tests(args.verbose, args.pattern)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 