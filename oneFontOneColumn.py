import datetime
import os
import subprocess
from vanilla.dialogs import getFile
from drawBot import *

# just now
NOW = datetime.datetime.now()

fontFile = getFile(fileTypes=["ttf", "otf"])

# Get the selected font file path
if fontFile:
    fontFile = fontFile[0]  

# Get font name without extension
fontFileName = os.path.splitext(os.path.basename(fontFile))[0]



# --------------------Variables--------------------
    
# Type Setting 
fontSize = 50
OneColumnAlignment = "left"
textLeading = 55
textTracking = 0

# Left Column OpenType Features
oneOTFea = dict(
    kern=False
)

# Artboard Settings
pageDimensions = "A4Landscape"
columns = 1
border = 40
gutter = 5


AutoOpen = True

# --------------------Variables--------------------


# Paths to the input text files
oneColumnTextPath = "leftColumn.txt"

# Load oneColumn and LTR text from the input files
with open(oneColumnTextPath, "r", encoding="utf-8") as oneColumnFile:
    oneColumnText = oneColumnFile.read()


# Convert text to FormattedString
oneColumnFormattedText = FormattedString(oneColumnText, font=fontFile, fontSize=fontSize, align=OneColumnAlignment, lineHeight=textLeading, tracking=textTracking, openTypeFeatures=oneOTFea)

# Function to create a new page with columns and return the remaining text
def create_new_page_with_columns(oneColumn_text):
    newPage(pageDimensions)
    totalGutterWidth = (columns - 1) * gutter
    textColumnWidth = (width() - border * 2 - totalGutterWidth) / columns

    
    oneColumn_overflow = FormattedString()
    
    for i in range(columns):
        font(fontFile, fontSize)
        
        if i == 0:
            oneColumn_text_overflow = oneColumn_text
        else:
            oneColumn_text_overflow = oneColumn_overflow
        
        oneColumn_overflow = textBox(oneColumn_text_overflow, (border + i * (textColumnWidth + gutter), border, textColumnWidth, height() - border * 2))
        
    
    return oneColumn_overflow

while oneColumnFormattedText:
    oneColumnFormattedText = create_new_page_with_columns(oneColumnFormattedText)

# Save the PDF to a file
saveTo = f'./proofs/{fontFileName}-{NOW:%Y%m%d}-oneColumn.pdf'

saveImage(saveTo)

# Open the PDF
if AutoOpen:
    subprocess.call(["open", saveTo])
