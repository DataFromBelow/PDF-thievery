"""
Created on Monday Feb 23 2026

@author yorl
"""

import os
import os.path
import wget
import pandas as pd
import numpy as np
import requests
import glob



dwn_url = ""


# This is the input file path for the excel file containing the url's 
input_path = "C:/Users/SPAC-49/Documents/Specialisterne/Softwareudvikling/Uge 4/test data/test-data.xlsx"

# This is the output file path 
output_path = "C:/Users/SPAC-49/Documents/Specialisterne/Softwareudvikling/Uge 4/test data/output"

ID = "BRnum"

try:
    df = pd.read_excel(input_path, sheet_name=0)
    #print(df)
    #print(df["Pdf_URL"][2])
except:
    print("GODDAMNIT")
finally:
    print("test ended")





for j in range(len(df)):
    
    try:
        file_name = df["BRnum"][j]
        url_link = df["Pdf_URL"][j]
        #print(file_name + ".pdf")
    except:
        print("critical failure")
    finally:
        pass
    
    if type(url_link) is float:
        print("Nan")
        pass
    elif type(url_link) is str and os.path.exists(f"{output_path}/{file_name}.pdf") == False:
        #print(url_link)
        try: #I know what i need to do. Use os to scan if the file is there already
            #if :
            #else:
            response = requests.get(url_link, allow_redirects=True)
            mime_type = str(response.headers.get("Content-Type"))
            if response.status_code == 200 and mime_type == "application/pdf":
                #os.path and os goes here
                # this is where you'd take data and store as a pdf in output path
                #print("200")
                print(f"200 : {file_name} / ({mime_type}): Success")
                #grab the contents
                save_file = str(file_name + ".pdf")
                save_dest = os.path.join(output_path, save_file)
                #save response.content
                try:
                    with open(save_dest, "wb") as file: 
                        file.write(response.content)
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
    

# function for filtering rows with no url's
# function goes here

# we gotta check if it has already been downloaded
# duplicate check
# not sure how to check that
duplicate_check = ""







