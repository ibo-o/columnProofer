import datetime
import os
import subprocess
from vanilla.dialogs import getFile
from drawBot import *

# just now
NOW = datetime.datetime.now()

leftFontFile = getFile(fileTypes=["ttf", "otf"])
rightFontFile = getFile(fileTypes=["ttf", "otf"])

# Get the selected font file paths for left and right
if leftFontFile:
    leftFontFile = leftFontFile[0]
if rightFontFile:
    rightFontFile = rightFontFile[0]

# Get font names without extension
leftFontFileName = os.path.splitext(os.path.basename(leftFontFile))[0]
rightFontFileName = os.path.splitext(os.path.basename(rightFontFile))[0]



# --------------------Variables--------------------
    
# Type Setting 
fontSize = 14
leftColumnAlignment = "left"
rightColumnAlignment = "left"

# Open Type Features
SyncOTFeatures = True

# Left Column OpenType Features
leftOTFea = dict(
    #ss01=False
)


# Right Column OpenType Features
rightOTFea = dict(
    #ss01=True
)


# Artboard Settings
pageDimensions = "A4Landscape"
columns = 1
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
leftFormattedText = FormattedString(leftText, font=leftFontFile, fontSize=fontSize, align=leftColumnAlignment, openTypeFeatures=rightOTFea)
rightFormattedText = FormattedString(rightText, font=rightFontFile, fontSize=fontSize, align=rightColumnAlignment, openTypeFeatures=leftOTFea)

# Function to create a new page with columns and return the remaining text
def create_new_page_with_columns(left_text, right_text):
    newPage(pageDimensions)
    totalGutterWidth = (columns - 1) * gutter
    textColumnWidth = (width() / 2 - border * 2 - totalGutterWidth) / columns
    
    left_overflow = FormattedString()
    right_overflow = FormattedString()
    
    for i in range(columns):
        if i == 0:
            left_text_overflow = left_text
            right_text_overflow = right_text
        else:
            left_text_overflow = left_overflow
            right_text_overflow = right_overflow
        
        # Left side text box
        font(leftFontFile, fontSize)
        left_overflow = textBox(left_text_overflow, (border + i * (textColumnWidth + gutter), border, textColumnWidth, height() - border * 2))
        
        # Right side text box
        font(rightFontFile, fontSize)
        right_overflow = textBox(right_text_overflow, (width() / 2 + border + i * (textColumnWidth + gutter), border, textColumnWidth, height() - border * 2))
    
    return left_overflow, right_overflow

while leftFormattedText or rightFormattedText:
    leftFormattedText, rightFormattedText = create_new_page_with_columns(leftFormattedText, rightFormattedText)

# Save the PDF to a file
saveTo = f'./proofs/{leftFontFileName}-{rightFontFileName}-{NOW:%Y%m%d}-twoFonts.pdf'

saveImage(saveTo)

# Open the PDF
if AutoOpen:
    subprocess.call(["open", saveTo])

# Display a message indicating the PDF generation is complete
print("Yooo!")
