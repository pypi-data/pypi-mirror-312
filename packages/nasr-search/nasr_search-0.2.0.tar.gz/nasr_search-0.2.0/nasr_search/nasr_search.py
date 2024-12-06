import os
import sys
import pandas as pd

def create_default_directory():
    """Create the default directory C:\\nasr_search if it doesn't exist."""
    default_dir = "C:\\nasr_search"
    if not os.path.exists(default_dir):
        os.makedirs(default_dir)
        print(f"Created directory: {default_dir}")
    else:
        print(f"Directory already exists: {default_dir}")
    return default_dir

def search_xlsx(column_heading, value, directory):
    results = []

    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return
    
    for file in os.listdir(directory):
        if file.endswith(".xlsx"):
            filepath = os.path.join(directory, file)
            try:
                df = pd.read_excel(filepath)

                if column_heading not in df.columns:
                    print(f"Warning: Column '{column_heading}' not found in file '{file}'.")
                    continue

                matches = df[df[column_heading].astype(str) == value]
                if not matches.empty:
                    for idx in matches.index:
                        results.append(f"{file} : Row {idx + 1}")  # Adjust for 1-based indexing
                
            except Exception as e:
                print(f"Error processing file '{file}': {e}")
    
    if results:
        print(f"Found {len(results)} match{'es' if len(results) > 1 else ''}:")
        for result in results:
            print(result)
    else:
        print("No match found.")

def main():
    create_default_directory()  # Ensure the directory is created

    if len(sys.argv) != 3:
        print("Usage: nasr_search <column heading> <value>")
        print("Example: nasr_search 'Name' 'John'")
        return

    column_heading = sys.argv[1]
    value = sys.argv[2]
    directory = "C:\\nasr_search"

    search_xlsx(column_heading, value, directory)

if __name__ == "__main__":
    main()
