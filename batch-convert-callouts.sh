#!/bin/bash
# Batch convert callouts to definition lists in multiple AsciiDoc files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONVERTER="$SCRIPT_DIR/convert-callouts-to-deflist.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS] <directory|file...>

Batch convert AsciiDoc callouts to definition list format.

OPTIONS:
    -h, --help      Show this help message
    -n, --dry-run   Preview changes without modifying files
    -v, --verbose   Enable verbose output
    -r, --recursive Process directories recursively

EXAMPLES:
    # Convert all .adoc files in current directory
    $(basename "$0") .

    # Dry run on specific files
    $(basename "$0") --dry-run file1.adoc file2.adoc

    # Recursively process a directory tree
    $(basename "$0") --recursive docs/

    # Verbose mode for debugging
    $(basename "$0") --verbose --dry-run modules/
EOF
    exit 0
}

# Parse arguments
DRY_RUN=""
VERBOSE=""
RECURSIVE=""
FILES=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        -n|--dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -r|--recursive)
            RECURSIVE="yes"
            shift
            ;;
        *)
            FILES+=("$1")
            shift
            ;;
    esac
done

if [ ${#FILES[@]} -eq 0 ]; then
    echo -e "${RED}Error: No files or directories specified${NC}"
    usage
fi

if [ ! -f "$CONVERTER" ]; then
    echo -e "${RED}Error: Converter script not found at $CONVERTER${NC}"
    exit 1
fi

# Function to process a single file
process_file() {
    local file="$1"

    if [ ! -f "$file" ]; then
        echo -e "${YELLOW}Skipping: $file (not a file)${NC}"
        return
    fi

    if [[ ! "$file" =~ \.adoc$ ]]; then
        [ -n "$VERBOSE" ] && echo -e "${YELLOW}Skipping: $file (not .adoc)${NC}"
        return
    fi

    echo "Processing: $file"

    if python3 "$CONVERTER" $DRY_RUN $VERBOSE "$file"; then
        echo -e "${GREEN}✓ Success: $file${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed: $file${NC}"
        return 1
    fi
}

# Function to process directory
process_directory() {
    local dir="$1"

    if [ ! -d "$dir" ]; then
        echo -e "${YELLOW}Warning: $dir is not a directory${NC}"
        return
    fi

    local find_args="-maxdepth 1"
    [ -n "$RECURSIVE" ] && find_args=""

    while IFS= read -r -d '' file; do
        process_file "$file"
    done < <(find "$dir" $find_args -name "*.adoc" -type f -print0 | sort -z)
}

# Main processing
TOTAL=0
SUCCESS=0
FAILED=0

for target in "${FILES[@]}"; do
    if [ -f "$target" ]; then
        ((TOTAL++))
        if process_file "$target"; then
            ((SUCCESS++))
        else
            ((FAILED++))
        fi
    elif [ -d "$target" ]; then
        echo -e "\n${GREEN}Processing directory: $target${NC}"
        while IFS= read -r -d '' file; do
            ((TOTAL++))
            if process_file "$file"; then
                ((SUCCESS++))
            else
                ((FAILED++))
            fi
        done < <(find "$target" $([ -z "$RECURSIVE" ] && echo "-maxdepth 1") -name "*.adoc" -type f -print0 | sort -z)
    else
        echo -e "${RED}Error: $target does not exist${NC}"
        ((FAILED++))
    fi
done

# Summary
echo ""
echo "=========================================="
echo "Summary:"
echo "  Total files:     $TOTAL"
echo -e "  ${GREEN}Successful:      $SUCCESS${NC}"
[ $FAILED -gt 0 ] && echo -e "  ${RED}Failed:          $FAILED${NC}" || echo "  Failed:          $FAILED"
echo "=========================================="

[ -n "$DRY_RUN" ] && echo -e "\n${YELLOW}DRY RUN - No files were modified${NC}"

exit $([ $FAILED -eq 0 ] && echo 0 || echo 1)
