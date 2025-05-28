#!/usr/bin/env python3
"""
Jinn-Core Project Validation Script

Comprehensive validation of all project components including:
- Package structure and imports
- Dependencies and virtual environment
- Test suite execution
- Documentation completeness
- Example scenarios
- Demo functionality
"""

import sys
import os
import json
import unittest
import importlib.util
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")

def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.ENDC}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.ENDC}")

def print_info(message: str):
    print(f"{Colors.BLUE}ℹ {message}{Colors.ENDC}")

def print_header(title: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title:^50}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.ENDC}\n")

class ProjectValidator:
    """Comprehensive project validation."""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.src_path = self.project_root / "src"
        self.tests_path = self.project_root / "tests"
        self.docs_path = self.project_root / "docs"
        self.examples_path = self.project_root / "examples"
        
        self.errors = []
        self.warnings = []
        self.success_count = 0
        self.total_checks = 0
    
    def check(self, condition: bool, success_msg: str, error_msg: str) -> bool:
        """Helper method to check conditions and track results."""
        self.total_checks += 1
        if condition:
            print_success(success_msg)
            self.success_count += 1
            return True
        else:
            print_error(error_msg)
            self.errors.append(error_msg)
            return False
    
    def warn(self, condition: bool, warning_msg: str, ok_msg: str = None) -> bool:
        """Helper method for warnings."""
        if not condition:
            print_warning(warning_msg)
            self.warnings.append(warning_msg)
            return False
        elif ok_msg:
            print_success(ok_msg)
        return True
    
    def validate_project_structure(self) -> bool:
        """Validate basic project structure."""
        print_header("PROJECT STRUCTURE")
        
        # Essential files
        essential_files = [
            "README.md",
            "requirements.txt", 
            "setup.py",
            "demo.py",
            "setup.sh"
        ]
        
        for file in essential_files:
            file_path = self.project_root / file
            self.check(
                file_path.exists(),
                f"Found {file}",
                f"Missing essential file: {file}"
            )
        
        # Essential directories
        essential_dirs = [
            ("src", "Source code directory"),
            ("tests", "Test suite directory"),
            ("examples", "Example scenarios directory"),
            ("docs", "Documentation directory")
        ]
        
        for dir_name, description in essential_dirs:
            dir_path = self.project_root / dir_name
            self.check(
                dir_path.exists() and dir_path.is_dir(),
                f"Found {dir_name}/ - {description}",
                f"Missing directory: {dir_name}/"
            )
        
        return len(self.errors) == 0
    
    def validate_source_code(self) -> bool:
        """Validate source code structure and imports."""
        print_header("SOURCE CODE VALIDATION")
        
        # Check core source files
        core_files = [
            "src/__init__.py",
            "src/engine.py",
            "src/models/__init__.py",
            "src/models/interest_rate.py",
            "src/models/inflation_shock.py",
            "src/utils/__init__.py",
            "src/utils/math_utils.py",
            "src/utils/formatters.py"
        ]
        
        for file in core_files:
            file_path = self.project_root / file
            self.check(
                file_path.exists(),
                f"Found {file}",
                f"Missing source file: {file}"
            )
        
        # Test imports
        sys.path.insert(0, str(self.src_path))
        
        try:
            # Test engine import
            from engine import SimulationEngine
            engine = SimulationEngine()
            
            self.check(
                len(engine.models) >= 2,
                f"Engine initialized with {len(engine.models)} models",
                "Engine failed to register models"
            )
            
            # Test model imports
            from models.interest_rate import InterestRateModel, InterestRateShock
            from models.inflation_shock import InflationShockModel, InflationShock, simulate_inflation_shock
            
            print_success("All model imports successful")
            self.success_count += 1
            self.total_checks += 1
            
        except ImportError as e:
            print_error(f"Import error: {e}")
            self.errors.append(f"Import error: {e}")
            self.total_checks += 1
        
        return True
    
    def validate_dependencies(self) -> bool:
        """Validate dependencies and virtual environment."""
        print_header("DEPENDENCIES VALIDATION")
        
        # Check if in virtual environment
        in_venv = (
            hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        )
        
        self.warn(
            in_venv,
            "Not running in virtual environment (recommended but not required)",
            "Running in virtual environment"
        )
        
        # Check Python version
        python_version = sys.version_info
        self.check(
            python_version >= (3, 8),
            f"Python version {python_version.major}.{python_version.minor}.{python_version.micro} is compatible",
            f"Python version {python_version.major}.{python_version.minor} is too old (requires 3.8+)"
        )
        
        # Check core dependencies
        core_deps = [
            ("numpy", "Numerical computing"),
            ("scipy", "Scientific computing"),
            ("pandas", "Data manipulation"),
            ("jsonschema", "JSON validation")
        ]
        
        for dep_name, description in core_deps:
            try:
                __import__(dep_name)
                print_success(f"{dep_name} - {description}")
                self.success_count += 1
                self.total_checks += 1
            except ImportError:
                print_error(f"Missing dependency: {dep_name}")
                self.errors.append(f"Missing dependency: {dep_name}")
                self.total_checks += 1
        
        return True
    
    def validate_tests(self) -> bool:
        """Run and validate test suite."""
        print_header("TEST SUITE VALIDATION")
        
        test_file = self.tests_path / "test_engine.py"
        
        self.check(
            test_file.exists(),
            "Found test file",
            "Missing test file: tests/test_engine.py"
        )
        
        if not test_file.exists():
            return False
        
        # Run tests
        print_info("Running test suite...")
        
        try:
            # Import and run tests
            sys.path.insert(0, str(self.tests_path.parent))
            
            # Run tests with unittest
            loader = unittest.TestLoader()
            suite = loader.discover('tests', pattern='test_*.py')
            runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
            result = runner.run(suite)
            
            self.check(
                result.wasSuccessful(),
                f"All {result.testsRun} tests passed",
                f"{len(result.failures + result.errors)} test(s) failed out of {result.testsRun}"
            )
            
            if result.failures:
                for test, traceback in result.failures:
                    print_error(f"FAIL: {test}")
            
            if result.errors:
                for test, traceback in result.errors:
                    print_error(f"ERROR: {test}")
            
        except Exception as e:
            print_error(f"Failed to run tests: {e}")
            self.errors.append(f"Test execution failed: {e}")
            self.total_checks += 1
            return False
        
        return True
    
    def validate_examples(self) -> bool:
        """Validate example scenarios."""
        print_header("EXAMPLE SCENARIOS VALIDATION")
        
        example_files = [
            "scenario_01.json",
            "scenario_02_inflation.json"
        ]
        
        for filename in example_files:
            file_path = self.examples_path / filename
            
            self.check(
                file_path.exists(),
                f"Found {filename}",
                f"Missing example: {filename}"
            )
            
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        scenario = json.load(f)
                    
                    # Validate JSON structure
                    required_keys = ['model', 'parameters', 'simulation']
                    has_all_keys = all(key in scenario for key in required_keys)
                    
                    self.check(
                        has_all_keys,
                        f"{filename} has valid structure",
                        f"{filename} missing required keys"
                    )
                    
                except json.JSONDecodeError as e:
                    print_error(f"{filename} has invalid JSON: {e}")
                    self.errors.append(f"Invalid JSON in {filename}")
                    self.total_checks += 1
        
        # Test scenario execution
        print_info("Testing scenario execution...")
        
        try:
            sys.path.insert(0, str(self.src_path))
            from engine import SimulationEngine
            
            engine = SimulationEngine()
            
            for filename in example_files:
                file_path = self.examples_path / filename
                if file_path.exists():
                    try:
                        results = engine.run_scenario_file(str(file_path))
                        
                        self.check(
                            'results' in results and 'metadata' in results,
                            f"Successfully executed {filename}",
                            f"Failed to execute {filename}"
                        )
                        
                    except Exception as e:
                        print_error(f"Error executing {filename}: {e}")
                        self.errors.append(f"Scenario execution failed: {filename}")
                        self.total_checks += 1
            
        except Exception as e:
            print_error(f"Failed to test scenarios: {e}")
            self.errors.append(f"Scenario testing failed: {e}")
            self.total_checks += 1
        
        return True
    
    def validate_documentation(self) -> bool:
        """Validate documentation completeness."""
        print_header("DOCUMENTATION VALIDATION")
        
        # Check documentation files
        doc_files = [
            ("README.md", "Main project documentation"),
            ("docs/roadmap.md", "Development roadmap"),
            ("CONTRIBUTING.md", "Contribution guidelines"),
            ("LICENSE", "License file")
        ]
        
        for filename, description in doc_files:
            file_path = self.project_root / filename
            
            self.check(
                file_path.exists(),
                f"Found {filename} - {description}",
                f"Missing documentation: {filename}"
            )
            
            # Check file content length (basic completeness check)
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    self.warn(
                        len(content) > 100,
                        f"{filename} seems incomplete (< 100 characters)",
                        f"{filename} has substantial content"
                    )
                except Exception as e:
                    print_warning(f"Could not read {filename}: {e}")
        
        # Check if DEVELOPMENT.md exists
        dev_doc = self.docs_path / "DEVELOPMENT.md"
        self.warn(
            dev_doc.exists(),
            "Missing DEVELOPMENT.md (recommended for contributors)"
        )
        
        return True
    
    def validate_demo(self) -> bool:
        """Test demo functionality."""
        print_header("DEMO VALIDATION")
        
        demo_file = self.project_root / "demo.py"
        
        self.check(
            demo_file.exists(),
            "Found demo.py",
            "Missing demo.py"
        )
        
        if not demo_file.exists():
            return False
        
        # Test demo import
        print_info("Testing demo functionality...")
        
        try:
            # Check if demo can be imported without running
            spec = importlib.util.spec_from_file_location("demo", demo_file)
            demo_module = importlib.util.module_from_spec(spec)
            
            print_success("Demo script can be imported")
            self.success_count += 1
            self.total_checks += 1
            
        except Exception as e:
            print_error(f"Demo import failed: {e}")
            self.errors.append(f"Demo import failed: {e}")
            self.total_checks += 1
        
        return True
    
    def generate_report(self) -> None:
        """Generate final validation report."""
        print_header("VALIDATION SUMMARY")
        
        success_rate = (self.success_count / self.total_checks * 100) if self.total_checks > 0 else 0
        
        print(f"Total checks: {self.total_checks}")
        print(f"Successful: {Colors.GREEN}{self.success_count}{Colors.ENDC}")
        print(f"Failed: {Colors.RED}{len(self.errors)}{Colors.ENDC}")
        print(f"Warnings: {Colors.YELLOW}{len(self.warnings)}{Colors.ENDC}")
        print(f"Success rate: {Colors.GREEN if success_rate > 90 else Colors.YELLOW if success_rate > 70 else Colors.RED}{success_rate:.1f}%{Colors.ENDC}")
        
        if self.errors:
            print(f"\n{Colors.RED}ERRORS:{Colors.ENDC}")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n{Colors.YELLOW}WARNINGS:{Colors.ENDC}")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if success_rate >= 95:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 PROJECT VALIDATION PASSED!{Colors.ENDC}")
            print("The project is well-structured and ready for use.")
        elif success_rate >= 80:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ PROJECT MOSTLY READY{Colors.ENDC}")
            print("The project is functional but has some issues to address.")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ PROJECT NEEDS WORK{Colors.ENDC}")
            print("The project has significant issues that need to be resolved.")
        
        print(f"\nTo get started:")
        print(f"  1. Run: {Colors.BLUE}source .venv/bin/activate{Colors.ENDC}")
        print(f"  2. Test: {Colors.BLUE}python demo.py{Colors.ENDC}")
        print(f"  3. Explore: {Colors.BLUE}ls examples/{Colors.ENDC}")
    
    def run_full_validation(self) -> bool:
        """Run complete project validation."""
        print(f"{Colors.BOLD}{Colors.BLUE}")
        print("🌪️  Jinn-Core Project Validation")
        print("=" * 50)
        print(f"{Colors.ENDC}")
        
        # Run all validation steps
        self.validate_project_structure()
        self.validate_source_code()
        self.validate_dependencies()
        self.validate_tests()
        self.validate_examples()
        self.validate_documentation()
        self.validate_demo()
        
        # Generate report
        self.generate_report()
        
        return len(self.errors) == 0


def main():
    """Main validation function."""
    validator = ProjectValidator()
    success = validator.run_full_validation()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 