#!/bin/bash

# Jinn-Core Setup Script
# Automated setup for development environment

set -e  # Exit on any error

echo "🌪️  Jinn-Core Economic Simulation Engine Setup"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python version
check_python() {
    print_status "Checking Python version..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 8 ]]; then
        print_error "Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
        exit 1
    fi
    
    print_success "Python $PYTHON_VERSION detected ✓"
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    
    if [[ -d ".venv" ]]; then
        print_warning "Virtual environment already exists. Removing and recreating..."
        rm -rf .venv
    fi
    
    $PYTHON_CMD -m venv .venv
    print_success "Virtual environment created ✓"
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    
    if [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
        print_success "Virtual environment activated ✓"
    elif [[ -f ".venv/Scripts/activate" ]]; then
        source .venv/Scripts/activate
        print_success "Virtual environment activated ✓"
    else
        print_error "Failed to find virtual environment activation script"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    print_success "Dependencies installed ✓"
}

# Install development dependencies
install_dev_dependencies() {
    print_status "Installing development dependencies..."
    
    pip install -e ".[dev]"
    
    print_success "Development dependencies installed ✓"
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    python tests/test_engine.py -q
    
    if [[ $? -eq 0 ]]; then
        print_success "All tests passed ✓"
    else
        print_error "Some tests failed ✗"
        exit 1
    fi
}

# Run demo
run_demo() {
    print_status "Running demo..."
    
    python demo.py
    
    print_success "Demo completed ✓"
}

# Verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    python -c "
import sys
sys.path.append('src')
from engine import SimulationEngine
engine = SimulationEngine()
print(f'Available models: {list(engine.models.keys())}')
print('Installation verified successfully!')
"
    
    print_success "Installation verified ✓"
}

# Main setup function
main() {
    echo ""
    print_status "Starting setup process..."
    echo ""
    
    # Check if we're in the right directory
    if [[ ! -f "requirements.txt" ]] || [[ ! -f "setup.py" ]]; then
        print_error "Please run this script from the jinn-core project directory"
        exit 1
    fi
    
    # Run setup steps
    check_python
    create_venv
    activate_venv
    install_dependencies
    
    # Ask user if they want development setup
    echo ""
    read -p "Install development dependencies? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_dev_dependencies
    fi
    
    # Run verification
    run_tests
    verify_installation
    
    # Ask user if they want to run demo
    echo ""
    read -p "Run the demo? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_demo
    fi
    
    echo ""
    print_success "🎉 Setup complete!"
    echo ""
    echo "To get started:"
    echo "  1. Activate virtual environment: source .venv/bin/activate"
    echo "  2. Run demo: python demo.py"
    echo "  3. Run tests: python tests/test_engine.py"
    echo "  4. Explore examples: ls examples/"
    echo ""
    echo "For more information, see README.md"
    echo ""
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "Jinn-Core Setup Script"
        echo ""
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --quick, -q    Quick setup (no prompts)"
        echo "  --dev, -d      Development setup with all dependencies"
        echo ""
        echo "Without options, runs interactive setup"
        exit 0
        ;;
    --quick|-q)
        echo "Running quick setup..."
        check_python
        create_venv
        activate_venv
        install_dependencies
        run_tests
        verify_installation
        print_success "Quick setup complete!"
        ;;
    --dev|-d)
        echo "Running development setup..."
        check_python
        create_venv
        activate_venv
        install_dependencies
        install_dev_dependencies
        run_tests
        verify_installation
        print_success "Development setup complete!"
        ;;
    *)
        main
        ;;
esac 