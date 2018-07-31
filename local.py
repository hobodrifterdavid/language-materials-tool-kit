import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import classes

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Copy of LP MASTER for Comments").sheet1
 
# Extract and print all of the values
# list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)

texts = {}

def download(id):
    existingIDs = sheet.row_values(1)
    if id in existingIDs:
        if id not in texts:
            # Good to go.
            col = sheet.col_values(existingIDs.index(id)+1)
            newText = classes.Text()
            newText.fromRawCells(col)
            texts[id] = newText
            return newText
        else:
            raise NameError("local text with this ID exists")
    else:
        raise NameError("ID not found in spreadsheet")

def upload(id):
    existingIDs = sheet.row_values(1)
    if id not in existingIDs:
        if id in texts:
            # Good to go.
            col = sheet.col_values(existingIDs.index(id)+1)
            newText = classes.Text()
            newText.fromRawCells(col)
            texts[id] = newText
            return newText
        else:
            raise NameError("local text with this ID exists")
    else:
        raise NameError("ID not found in spreadsheet")


# values = sheet.get_all_values()

#with open('data.txt', 'w') as outfile:  
#    json.dump(values, outfile)

def newText(id):
    newText = classes.Text()
    newText.id = id
    texts[id] = newText

    return newText

def register(text):
    texts[text.id] = text

