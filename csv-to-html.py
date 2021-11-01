import pandas as pd # library for reading and converting csv files
import sys # library for taking cmd arguments

# function that reads both files, merges them and converts the data into an html table
def readcsvs():
  fileOne = pd.read_csv(sys.argv[1])
  fileTwo = pd.read_csv(sys.argv[2])
  
  fileOne['End Date'] = pd.to_datetime(fileOne['End Date'])
  
  fileOne['Auth Code'] = fileOne['Auth Code'].astype('string')
  fileTwo['Auth Code'] = fileTwo['Auth Code'].astype('string')
  
  # Colums that will not be displayed in the table
  columnsToHide = []
  
  # merge the files and sort the table by End Date
  merged = fileOne.merge(fileTwo, on='Auth Code', how="outer").sort_values('End Date',ignore_index=True)
  
  # format the End Date column
  list = [str((d-pd.Timestamp.today()).days+1) + " Days " + d.strftime('%d/%m/%Y') for d in fileOne['End Date']]
  list.sort(key=getDay)
  
  lessThenWeek = sum(int(i.split(" ")[0]) <= 7 for i in list)
  
  for x in range(len(merged.index)-len(list)):
    list.append(10000)
  
  merged['End Date'] = list
  
  mergedLessThenWeek = merged[:lessThenWeek]
  mergedMoreThenWeek = merged[lessThenWeek:]
  
  # hide unwanted columns and convert the table object into a string with html style table
  merged = merged.style.hide_columns(columnsToHide).to_html()
  
  mergedLessThenWeek = mergedLessThenWeek.style.hide_columns(columnsToHide).set_properties(subset=['End Date'], **{'width': '140px'}).to_html()
  mergedMoreThenWeek = mergedMoreThenWeek.style.hide_columns(columnsToHide).set_properties(subset=['End Date'], **{'width': '165px'}).to_html()
  
  return mergedLessThenWeek, mergedMoreThenWeek

# function that takes the html table string and create an html file with the table included
def createOutput(mergedLessThenWeek, mergedMoreThenWeek):
  html_template ="""<html>
<head>
<title>Client device table</title>
<link rel="stylesheet" href="main.css">
</head>
<body>
<div class="container">
<h2>Expire withing 1 week</h2>
{}
<br>
<h2>Expire after 1 week</h2>
{}
</div>
</body>w
</html>
  """.format(mergedLessThenWeek, mergedMoreThenWeek)
  
  # create the html file
  with open("file.html", "w") as file:
    file.write(html_template)

def getDay(elem):
  return int(elem.split(" ")[0])

def createCSS():
  css_template = """* {
  margin: 0;
  padding: 0;
}

.container {
  margin: auto;
  width: 90%;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin-top: 1rem;
}

th{
  padding-top: 5px;
  padding-bottom: 5px;
  text-align: center;
  font-size: 1.2rem;
  background-color: #047baa;
  color: white;
}

td{
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 5px;
  text-align: left;
  font-size: 1.1rem;
}

tr:nth-child(even) {
  background-color: #b8b8b8;
}

/* tr:nth-child(even) td{
  border-right: 2px solid white;
}

tr:nth-child(odd) td{
  border-right: 2px solid #b8b8b8;
} */
"""

  with open("main.css", "w") as file:
    file.write(css_template)

# call all functions
if __name__ == "__main__":
  mergedLessThenWeek, mergedMoreThenWeek = readcsvs()
  createOutput(mergedLessThenWeek, mergedMoreThenWeek)
  createCSS()
