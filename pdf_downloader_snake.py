"""
Created on Monday Feb 23 2026
@author yorl
"""
import os
import os.path
import pandas as pd
import requests

# File paths
input_path = "C:/Users/Spac-43/Documents/GitHub/PDF-thievery/test data/test-data.xlsx"
output_path = "C:/Users/Spac-43/Documents/GitHub/PDF-thievery/test data/output"

# Column names
ID_COL = "BRnum"
URL_COL = "Pdf_URL"

def main():
    # Load Excel file
    try:
        df = pd.read_excel(input_path, sheet_name=0)
        print("Excel file loaded successfully")
    except FileNotFoundError:
        print(f"Excel file not found: {input_path}")
        return
    except Exception as e:
        print(f"Failed to load Excel file: {e}")
        return

    # Loop through each row
    for j in range(len(df)):
        file_name = df[ID_COL][j]
        url_link = df[URL_COL][j]

        # Skip rows with no URL
        if type(url_link) is float:
            print(f"Skipping {file_name}: no URL")
            continue

        # Skip if file already exists
        if os.path.exists(f"{output_path}/{file_name}.pdf"):
            print(f"Skipping {file_name}: already downloaded")
            continue

        # Attempt download
        try:
            response = requests.get(url_link, allow_redirects=True)
            mime_type = response.headers.get("Content-Type", "")

            if response.status_code == 200 and mime_type == "application/pdf":
                save_dest = os.path.join(output_path, file_name + ".pdf")
                try:
                    with open(save_dest, "wb") as file:
                        file.write(response.content)
                    print(f"Success: {file_name}")
                except Exception as e:
                    print(f"Failed to save {file_name}: {e}")
            elif response.status_code == 404:
                print(f"404 Not Found: {file_name} - {url_link}")
            else:
                print(f"Failed - status {response.status_code}, type {mime_type}: {file_name}")

        except Exception as e:
            print(f"Exception for {url_link}: {e}")

if __name__ == "__main__":
    main()
