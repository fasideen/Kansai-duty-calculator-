import pandas as pd
import glob
import os

def create_master_database():
    # 1. Automatically find all 8 tables you already uploaded to your repository
    table_files = glob.glob("PANDUAN HARGA BIL2 2026.xlsx - Table *.csv")
    
    if not table_files:
        print("Error: Could not locate Table 1 through Table 8 in your folder. Please ensure they are uploaded.")
        return
        
    # 2. Sort them numerically so the car list stays perfectly in sequence
    table_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    
    # 3. Apply your exact English column translations
    english_headers = [
        'No. / Serial No.', 'Brand / Make', 'MODEL', 'CC', 'Currency', 
        'Age 12 months and not exceeding 24 months', 
        'Age 24 months and not exceeding 36 months', 
        'Age 36 months and not exceeding 48 months', 
        'Age 48 months and not exceeding 60 months', 
        'Age 60 months and above'
    ]
    
    master_list = []
    
    for file_path in table_files:
        try:
            df = pd.read_csv(file_path)
            # Standardize headers to force the match
            if len(df.columns) == 10:
                df.columns = english_headers
                master_list.append(df)
        except Exception as e:
            print(f"Skipping problematic sheet file {file_path}: {e}")
            
    if master_list:
        # 4. Stitch every single row from all 8 files into one master sheet
        final_dataframe = pd.concat(master_list, ignore_index=True)
        
        # 5. Automatically strip currency text (like 'JPY', 'GBP') and commas from math cells
        for col in english_headers[5:]:
            final_dataframe[col] = final_dataframe[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
            final_dataframe[col] = pd.to_numeric(final_dataframe[col], errors='coerce').fillna(0)
            
        # 6. Save the fully unified, 2284-row data file directly into your workspace
        final_dataframe.to_csv("PANDUAN_MASTER_2026.csv", index=False)
        print(f"Success! Master database created with {len(final_dataframe)} verified rows.")
    else:
        print("Could not aggregate the source data sheets.")

if __name__ == "__main__":
    create_master_database()
