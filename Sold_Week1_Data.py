import pandas as pd
file_path = "/Users/mihir/Desktop/internshipcrmls/csv/"



sold202401 = pd.read_csv(file_path + "CRMLSSold202401_filled.csv", encoding = "ISO-8859-1")
sold202402 = pd.read_csv(file_path + "CRMLSSold202402.csv", encoding = "ISO-8859-1")
sold202403 = pd.read_csv(file_path + "CRMLSSold202403_filled.csv", encoding = "ISO-8859-1")
sold202404 = pd.read_csv(file_path + "CRMLSSold202404_filled.csv", encoding = "ISO-8859-1")
sold202405 = pd.read_csv(file_path + "CRMLSSold202405_filled.csv", encoding = "ISO-8859-1")
sold202406 = pd.read_csv(file_path + "CRMLSSold202406_filled.csv", encoding = "ISO-8859-1")
sold202407 = pd.read_csv(file_path + "CRMLSSold202407_filled.csv", encoding = "ISO-8859-1")
sold202408 = pd.read_csv(file_path + "CRMLSSold202408.csv", encoding = "ISO-8859-1")
sold202409 = pd.read_csv(file_path + "CRMLSSold202409.csv", encoding = "ISO-8859-1")
sold202410 = pd.read_csv(file_path + "CRMLSSold202410.csv", encoding = "ISO-8859-1")
sold202411 = pd.read_csv(file_path + "CRMLSSold202411.csv", encoding = "ISO-8859-1")
sold202412 = pd.read_csv(file_path + "CRMLSSold202412.csv", encoding = "ISO-8859-1")


sold202501 = pd.read_csv(file_path + "CRMLSSold202501_filled.csv", encoding = "ISO-8859-1")
sold202502 = pd.read_csv(file_path + "CRMLSSold202502.csv", encoding = "ISO-8859-1")
sold202503 = pd.read_csv(file_path + "CRMLSSold202503.csv", encoding = "ISO-8859-1")
sold202504 = pd.read_csv(file_path + "CRMLSSold202504.csv", encoding = "ISO-8859-1")
sold202505 = pd.read_csv(file_path + "CRMLSSold202505.csv", encoding = "ISO-8859-1")
sold202506 = pd.read_csv(file_path + "CRMLSSold202506.csv", encoding = "ISO-8859-1")
sold202507 = pd.read_csv(file_path + "CRMLSSold202507.csv", encoding = "ISO-8859-1")
sold202508 = pd.read_csv(file_path + "CRMLSSold202508.csv", encoding = "ISO-8859-1")
sold202509 = pd.read_csv(file_path + "CRMLSSold202509.csv", encoding = "ISO-8859-1")
sold202510 = pd.read_csv(file_path + "CRMLSSold202510.csv", encoding = "ISO-8859-1")
sold202511 = pd.read_csv(file_path + "CRMLSSold202511.csv", encoding = "ISO-8859-1")
sold202512 = pd.read_csv(file_path + "CRMLSSold202512.csv", encoding = "ISO-8859-1")


sold202601 = pd.read_csv(file_path + "CRMLSSold202601.csv", encoding = "ISO-8859-1")
sold202502 = pd.read_csv(file_path + "CRMLSSold202602.csv", encoding = "ISO-8859-1")
sold202503 = pd.read_csv(file_path + "CRMLSSold202603.csv", encoding = "ISO-8859-1")
sold202504 = pd.read_csv(file_path + "CRMLSSold202604.csv", encoding = "ISO-8859-1")


soldlist = [sold202401, sold202402, sold202403, sold202404, sold202405, sold202405, sold202406, sold202407, sold202408, sold202409, sold202410, sold202411,  sold202412,  sold202501, sold202502, sold202503, sold202504, sold202505, sold202506, sold202507, sold202508,sold202509, sold202510, sold202511, sold202512, sold202601, sold202502, sold202503, sold202504]

#Row count confirmation

for dataset in soldlist:
    print(len(dataset))

#Concat Data    
concatsold = pd.concat(soldlist)
concatsold.reset_index(drop=True, inplace=True)
print(len(concatsold))

#Remove duplicate rows
rem_duplicate_sold = concatsold.drop_duplicates(
    keep="first"
    )
print(f"Rows after removing duplicates: {len(rem_duplicate_sold)}")

#Drop blank columns
dropped_columns = ["latfilled", "lonfilled"]
column_dropped_data = rem_duplicate_sold.drop(columns = dropped_columns)

#Filter to residential only
filteredsold = column_dropped_data[column_dropped_data["PropertyType"] == "Residential"]
print(len(filteredsold))

#Copy
Final_Sold = filteredsold.copy()

#Export to CSV
Final_Sold.to_csv('/Users/mihir/Desktop/internshipcrmls/csv/CRMLSSold.csv', index=False)