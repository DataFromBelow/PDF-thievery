"""
Created on Monday Feb 23 2026

@author yorl
"""

import os
import os.path
import pandas as pd
import requests


# This is the input file path for the excel file containing the url's 
input_path = "C:/Users/Spac-43/Documents/GitHub/PDF-thievery/test data/test-data.xlsx"

# This is the output file path 
output_path = "C:/Users/Spac-43/Documents/GitHub/PDF-thievery/test data/output"

# ID = "BRnum"

try: # Checks if the list has even loaded
    df = pd.read_excel(input_path, sheet_name=0)
except:
    print("GODDAMNIT")
finally:
    print("test ended")


for j in range(len(df)):
    file_name = df["BRnum"][j]
    url_link = df["Pdf_URL"][j]
    if type(url_link) is float: # Solves NaN as a problem
        print("NaN")
        pass
    elif type(url_link) is str and os.path.exists(f"{output_path}/{file_name}.pdf") == False: # checks for url_link and the file not existing, does not overwrite files
        #print(url_link) # error checking
        try: 
            response = requests.get(url_link, allow_redirects=True)
            mime_type = str(response.headers.get("Content-Type"))
            if response.status_code == 200 and mime_type == "application/pdf": # checks for response code 200 and mime type application/pdf 
                print(f"200 : {file_name} / ({mime_type}): Success")
                save_file = str(file_name + ".pdf")
                save_dest = os.path.join(output_path, save_file)
                try:
                    with open(save_dest, "wb") as file: #grab the contents
                        file.write(response.content) #save response.content
                except:
                    print(f"Unknown Failure: {save_file}")
            elif response.status_code == 404:
                print(f"404 : {file_name} : {url_link}")
                #write in excel file that link is 404
            else:
                print(f"Failure / Not PDF")
                pass
            pass
        except:
            print(f"exception: {url_link} invalid url")
            pass
    else:
        pass
        # print("fail")
    
