import pandas as pd # library for reading and converting csv files
import sys # library for taking cmd arguments

# function that reads both files, merges them and converts the data into an html table
def readcsvs():
  fileOne = pd.read_csv(sys.argv[1])
  fileTwo = pd.read_csv(sys.argv[2])
  
  # Change the values of column End Date to "datetime" so it can be sorted later
  fileOne['End Date'] = pd.to_datetime(fileOne['End Date'])
  
  # Colums that will not be displayed in the table
  columnsToHide = [
    'Opportunity Type',
    'Asset (custom): Asset Name',
    'Close Date','Quote Line Item',
    'Product Name','Product Code_y',
    'Opportunity Name']
  
  # merge the files and sort the table by End Date
  merged = fileOne.merge(fileTwo, on='Auth Code', how="left").sort_values('End Date', ignore_index=True)
  
  # format the End Date column
  merged['End Date'] = merged['End Date'].dt.strftime('%d/%m/%Y')
  
  # hide unwaqnted columns and convert the table object into a string with html style table
  merged = merged.style.hide_columns(columnsToHide).to_html()
  
  return merged

# function that takes the html table string and create an html file with the table included
def createOutput(mergedFiles):
  html_template ="""<html>
<head>
<title>Client device table</title>
<link rel="stylesheet" href="main.css">
</head>
<body>
<div class="container">
{}
</div>
</body>
</html>
  """.format(mergedFiles)
  
  # create the html file
  with open("file.html", "w") as file:
      file.write(html_template)

# call all functions
if __name__ == "__main__":
  mergedFiles = readcsvs()
  createOutput(mergedFiles)
