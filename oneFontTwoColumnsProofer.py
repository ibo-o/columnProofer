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
fontSize = 24
leftColumnAlignment = "left"
rightColumnAlignment = "left"

# Open Type Features
SyncOTFeatures = True

# Left Column OpenType Features
leftOTFea = dict(
    ss01=False
)


# Right Column OpenType Features
rightOTFea = dict(
    ss01=True
)


# Artboard Settings
pageDimensions = "A4Landscape"
columns = 2
border = 15
gutter = 2


AutoOpen = True

# --------------------Variables--------------------

# Open Type Features condition
if SyncOTFeatures:
    rightOTFea = leftOTFea
else:
    leftOTFea = leftOTFea
    rightOTFea = rightOTFea





# Paths to the input text files
leftTextPath = "leftColumn.txt"
rightTextPath = "rightColumn.txt"

# Load left and right text from the input files
with open(leftTextPath, "r", encoding="utf-8") as leftFile:
    leftText = leftFile.read()

with open(rightTextPath, "r", encoding="utf-8") as rightFile:
    rightText = rightFile.read()

# Convert text to FormattedString
leftFormattedText = FormattedString(leftText, font=fontFile, fontSize=fontSize, align=leftColumnAlignment, openTypeFeatures=rightOTFea)
rightFormattedText = FormattedString(rightText, font=fontFile, fontSize=fontSize, align=rightColumnAlignment, openTypeFeatures=leftOTFea)

# Function to create a new page with columns and return the remaining text
def create_new_page_with_columns(left_text, right_text):
    newPage(pageDimensions)
    totalGutterWidth = (columns - 1) * gutter
    textColumnWidth = (width() / 2 - border * 2 - totalGutterWidth) / columns
    
    left_overflow = FormattedString()
    right_overflow = FormattedString()
    
    for i in range(columns):
        font(fontFile, fontSize)
        
        if i == 0:
            left_text_overflow = left_text
            right_text_overflow = right_text
        else:
            left_text_overflow = left_overflow
            right_text_overflow = right_overflow
        
        left_overflow = textBox(left_text_overflow, (border + i * (textColumnWidth + gutter), border, textColumnWidth, height() - border * 2))
        right_overflow = textBox(right_text_overflow, (width() / 2 + border + i * (textColumnWidth + gutter), border, textColumnWidth, height() - border * 2))
    
    return left_overflow, right_overflow

while leftFormattedText or rightFormattedText:
    leftFormattedText, rightFormattedText = create_new_page_with_columns(leftFormattedText, rightFormattedText)

# Save the PDF to a file
saveTo = f'./proofs/{fontFileName}-{NOW:%Y%m%d}-oneFont.pdf'

saveImage(saveTo)

# Open the PDF
if AutoOpen:
    subprocess.call(["open", saveTo])
