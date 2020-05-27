#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:55:47 2019
anthony2owaru@gmail.com
Scrapes tabular data from United States Geological Survey (https://waterdata.usgs.gov)
More info: https://help.waterdata.usgs.gov/faq/about-tab-delimited-output
"""

# library modules
import requests
from datetime import datetime
import pandas as pd
import os

"""
**STEP 1**
Pull text from url, feel free to change this URL!"""

url="https://waterdata.usgs.gov/nwis/dv?cb_00065=on&format=rdb&site_no=02247222&referred_module=sw&period=&begin_date=1950-01-01&end_date=2019-11-21"
doc=requests.get(url).text
print("\t \t******First 15 lines of page requested: below:****** \n",doc.split("\n")[0:15],"\n END OF PREVIEW, parsing doc now…")

"""
**STEP 2**
Clean the comments section by stripping up to last hashtag
"""
doc = doc[doc.rfind("# ")+1:]

"""
**STEP 3**
Split cells by \t from rows split from doc by \n
"""
cells=[row.split("\t") for row in doc.split("\n") if len(row.split("\t")) == 5]

"""
**STEP 4**
Construct dict that stores column names and indices
"""
column_indices = dict((column_name, cells[0].index(column_name)) for column_name in cells[0])

"""
**STEP 5**
Create output_object which is dict constructed from column_indices and list comprehensions.
The list comps loop through each row splitting them into columns by index from the column_indices dict
We turn that into a dataframe and then export to csv.
"""
output_object = dict((key,[row[value] for row in cells[1:]]) for key,value in column_indices.items())
print("Document parsed, exporting…")
output_df = pd.DataFrame(output_object)
output_df.to_csv(str(os.getcwd())+"/"+str(datetime.now())+"_site_no_"+output_object["site_no"][0]+".csv")
print("csv exported to ",str(os.getcwd()))
