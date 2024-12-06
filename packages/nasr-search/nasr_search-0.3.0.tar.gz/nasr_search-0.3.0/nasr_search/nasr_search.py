def search_xlsx(column_heading, value, directory):
    results = []

    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return
    
    for file in os.listdir(directory):
        if file.endswith(".xlsx"):
            filepath = os.path.join(directory, file)
            try:
                # Read the Excel file, using the first row (after skipping the first few rows if needed) as headers
                df = pd.read_excel(filepath, header=None)  # Don't use the first row as header initially
                
                # Search for the column heading in the first row (adjust for the first value in the column being used as the heading)
                column_heading_index = None
                for col in df.columns:
                    if str(df.iloc[0, col]) == column_heading:
                        column_heading_index = col
                        break

                if column_heading_index is None:
                    print(f"Warning: Column '{column_heading}' not found in file '{file}'.")
                    continue

                # After identifying the column heading, update the column names
                df.columns = df.iloc[0]  # Set the first row as the column headers
                df = df.drop(0)  # Remove the first row from the data
                
                # Now search for the value in the identified column
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
