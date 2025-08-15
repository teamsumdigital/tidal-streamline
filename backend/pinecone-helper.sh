#!/bin/bash
# Pinecone Helper Script for Tidal Streamline
# Provides easy access to common Pinecone operations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  Tidal Streamline - Pinecone Helper${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory
check_directory() {
    if [[ ! -f "populate_pinecone_historical.py" ]]; then
        print_error "Please run this script from the backend directory"
        exit 1
    fi
}

# Show usage
show_usage() {
    print_header
    echo ""
    echo "Usage: ./pinecone-helper.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  status         - Show current system status"
    echo "  test          - Run system connectivity tests"
    echo "  setup         - Create Pinecone index"
    echo "  populate      - Populate index with historical data"
    echo "  populate-dry  - Dry run population (safe test)"
    echo "  verify        - Verify existing data"
    echo "  info          - Show index information"
    echo "  clean         - Delete and recreate index (DANGEROUS)"
    echo ""
    echo "Examples:"
    echo "  ./pinecone-helper.sh status"
    echo "  ./pinecone-helper.sh populate-dry"
    echo "  ./pinecone-helper.sh populate"
    echo ""
}

# Main commands
cmd_status() {
    print_header
    print_info "Checking system status..."
    python manage_pinecone_data.py status
}

cmd_test() {
    print_header
    print_info "Running system tests..."
    python manage_pinecone_data.py test
}

cmd_setup() {
    print_header
    print_info "Creating Pinecone index..."
    python scripts/setup_pinecone_index.py --create
    
    if [[ $? -eq 0 ]]; then
        print_success "Index created successfully!"
        print_info "Next step: Run './pinecone-helper.sh populate-dry' to test"
    else
        print_error "Index creation failed"
        exit 1
    fi
}

cmd_populate() {
    print_header
    print_info "Starting historical data population..."
    print_warning "This may take a long time for large datasets"
    
    # Ask for confirmation
    echo -n "Continue with population? (y/N): "
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_info "Population cancelled"
        exit 0
    fi
    
    python populate_pinecone_historical.py --verify
    
    if [[ $? -eq 0 ]]; then
        print_success "Population completed successfully!"
    else
        print_error "Population failed - check logs for details"
        exit 1
    fi
}

cmd_populate_dry() {
    print_header
    print_info "Running dry run population (no data will be uploaded)..."
    python populate_pinecone_historical.py --dry-run
}

cmd_verify() {
    print_header
    print_info "Verifying index data..."
    python scripts/setup_pinecone_index.py --verify
}

cmd_info() {
    print_header
    print_info "Getting index information..."
    python scripts/setup_pinecone_index.py --info
}

cmd_clean() {
    print_header
    print_warning "This will DELETE the entire Pinecone index and recreate it!"
    print_warning "ALL VECTOR DATA WILL BE LOST!"
    echo ""
    echo -n "Type 'DELETE' to confirm: "
    read -r response
    
    if [[ "$response" == "DELETE" ]]; then
        print_info "Deleting and recreating index..."
        python scripts/setup_pinecone_index.py --force-recreate
        
        if [[ $? -eq 0 ]]; then
            print_success "Index recreated successfully!"
            print_info "Run './pinecone-helper.sh populate' to repopulate data"
        else
            print_error "Index recreation failed"
            exit 1
        fi
    else
        print_info "Operation cancelled"
    fi
}

# Main script
check_directory

# Handle commands
case "${1:-}" in
    "status")
        cmd_status
        ;;
    "test")
        cmd_test
        ;;
    "setup")
        cmd_setup
        ;;
    "populate")
        cmd_populate
        ;;
    "populate-dry")
        cmd_populate_dry
        ;;
    "verify")
        cmd_verify
        ;;
    "info")
        cmd_info
        ;;
    "clean")
        cmd_clean
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    "")
        show_usage
        ;;
    *)
        print_error "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac