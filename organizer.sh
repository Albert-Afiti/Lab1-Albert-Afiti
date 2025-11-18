#!/bin/bash

# organizer.sh - CSV File Archiver with Logging
# BSE Year 1 Trimester 2 - Lab 1

# Function to generate timestamp
generate_timestamp() {
    date +"%Y%m%d-%H%M%S"
}

# Function to log messages and file contents
log_action() {
    local message="$1"
    local file="$2"
    
    echo "==========================================" >> organizer.log
    echo "TIMESTAMP: $(date)" >> organizer.log
    echo "ACTION: $message" >> organizer.log
    if [[ -f "$file" ]]; then
        echo "FILE: $file" >> organizer.log
        echo "CONTENTS:" >> organizer.log
        cat "$file" >> organizer.log
    else
        echo "FILE: $file (not found)" >> organizer.log
    fi
    echo "" >> organizer.log
}

# Main script execution
main() {
    echo "Starting CSV Organizer..."
    
    # Step 1: Check/Create Archive Directory
    if [[ ! -d "archive" ]]; then
        echo "Creating archive directory..."
        mkdir archive
        if [[ $? -eq 0 ]]; then
            echo "Archive directory created successfully."
        else
            echo "Error: Failed to create archive directory." >&2
            exit 1
        fi
    else
        echo "Archive directory already exists."
    fi
    
    # Step 2: Find CSV files in current directory
    echo "Searching for CSV files..."
    csv_files=$(find . -maxdepth 1 -name "*.csv" -type f | grep -v "./archive/")
    
    if [[ -z "$csv_files" ]]; then
        echo "No CSV files found in current directory."
        exit 0
    fi
    
    # Count CSV files found
    file_count=$(echo "$csv_files" | wc -l)
    echo "Found $file_count CSV file(s) to process."
    
    # Step 3: Process each CSV file
    echo "$csv_files" | while read -r file; do
        # Remove leading ./
        filename=$(basename "$file")
        
        # Skip if file is in archive directory
        if [[ "$filename" == "./archive/"* ]]; then
            continue
        fi
        
        echo "Processing: $filename"
        
        # Generate timestamp and new filename
        timestamp=$(generate_timestamp)
        base_name="${filename%.*}"
        extension="${filename##*.}"
        new_filename="${base_name}-${timestamp}.${extension}"
        
        # Log the archiving action with file contents
        log_action "Archiving $filename to archive/$new_filename" "$filename"
        
        # Move and rename the file
        if mv "$filename" "archive/$new_filename"; then
            echo "Successfully archived: $filename -> archive/$new_filename"
        else
            echo "Error: Failed to move $filename" >&2
            log_action "FAILED to archive $filename" "$filename"
        fi
    done
    
    echo "CSV organization completed."
    echo "Check organizer.log for details."
}

# Run main function
main "$@"
