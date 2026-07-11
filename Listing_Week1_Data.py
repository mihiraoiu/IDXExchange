import pandas as pd
file_path = "/Users/mihir/Desktop/internshipcrmls/csv/"



listing202401 = pd.read_csv(file_path + "CRMLSListing202401.csv", encoding = "ISO-8859-1")
listing202402 = pd.read_csv(file_path + "CRMLSListing202402.csv", encoding = "ISO-8859-1")
listing202403 = pd.read_csv(file_path + "CRMLSListing202403.csv", encoding = "ISO-8859-1")
listing202404 = pd.read_csv(file_path + "CRMLSListing202404.csv", encoding = "ISO-8859-1")
listing202405 = pd.read_csv(file_path + "CRMLSListing202405.csv", encoding = "ISO-8859-1")
listing202406 = pd.read_csv(file_path + "CRMLSListing202406.csv", encoding = "ISO-8859-1")
listing202407 = pd.read_csv(file_path + "CRMLSListing202407.csv", encoding = "ISO-8859-1")
listing202408 = pd.read_csv(file_path + "CRMLSListing202408.csv", encoding = "ISO-8859-1")
listing202409 = pd.read_csv(file_path + "CRMLSListing202409.csv", encoding = "ISO-8859-1")
listing202410 = pd.read_csv(file_path + "CRMLSListing202410.csv", encoding = "ISO-8859-1")
listing202411 = pd.read_csv(file_path + "CRMLSListing202411.csv", encoding = "ISO-8859-1")
listing202412 = pd.read_csv(file_path + "CRMLSListing202412.csv", encoding = "ISO-8859-1")


listing202501 = pd.read_csv(file_path + "CRMLSListing202501.csv", encoding = "ISO-8859-1")
listing202502 = pd.read_csv(file_path + "CRMLSListing202502.csv", encoding = "ISO-8859-1")
listing202503 = pd.read_csv(file_path + "CRMLSListing202503.csv", encoding = "ISO-8859-1")
listing202504 = pd.read_csv(file_path + "CRMLSListing202504.csv", encoding = "ISO-8859-1")
listing202505 = pd.read_csv(file_path + "CRMLSListing202505.csv", encoding = "ISO-8859-1")
listing202506 = pd.read_csv(file_path + "CRMLSListing202506.csv", encoding = "ISO-8859-1")
listing202507 = pd.read_csv(file_path + "CRMLSListing202507.csv", encoding = "ISO-8859-1")
listing202508 = pd.read_csv(file_path + "CRMLSListing202508.csv", encoding = "ISO-8859-1")
listing202509 = pd.read_csv(file_path + "CRMLSListing202509.csv", encoding = "ISO-8859-1")
listing202510 = pd.read_csv(file_path + "CRMLSListing202510.csv", encoding = "ISO-8859-1")
listing202511 = pd.read_csv(file_path + "CRMLSListing202511.csv", encoding = "ISO-8859-1")
listing202512 = pd.read_csv(file_path + "CRMLSListing202512.csv", encoding = "ISO-8859-1")


listing202601 = pd.read_csv(file_path + "CRMLSListing202601.csv", encoding = "ISO-8859-1")
listing202602 = pd.read_csv(file_path + "CRMLSListing202602.csv", encoding = "ISO-8859-1")
listing202603 = pd.read_csv(file_path + "CRMLSListing202603.csv", encoding = "ISO-8859-1")
listing202604 = pd.read_csv(file_path + "CRMLSListing202604.csv", encoding = "ISO-8859-1")


listinglist = [listing202401, listing202402, listing202403, listing202404, listing202405, listing202405, listing202406, listing202407, listing202408, listing202409, listing202410, listing202411,  listing202412,  listing202501, listing202502, listing202503, listing202504, listing202505, listing202506, listing202507, listing202508,listing202509, listing202510, listing202511, listing202512, listing202601, listing202602, listing202603, listing202604]

#Row count confirmation

for dataset in listinglist:
    print(len(dataset))

#Concat Data    
concatlisting = pd.concat(listinglist)
concatlisting.reset_index(drop=True, inplace=True)
print(len(concatlisting))

#Remove duplicate rows
rem_duplicate_listing = concatlisting.drop_duplicates(
    keep="first"
    )
print(f"Rows after removing duplicates: {len(rem_duplicate_listing)}")


#Filter to residential only
filteredlisting = rem_duplicate_listing[rem_duplicate_listing["PropertyType"] == "Residential"]
print(len(filteredlisting))

#Copy
Final_Listing = filteredlisting.copy()

#Export to CSV
Final_Listing.to_csv('/Users/mihir/Desktop/internshipcrmls/csv/CRMLSListing.csv', index=False)
