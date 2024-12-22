#TESSERACT - TUTORIAL LEARNING - WILL NOT BE USED FOR FINAL WORKS
import pytesseract
from pytesseract import Output
import PIL.Image
import cv2

"""tesseract --help-psm
Page segmentation modes (PSM):
  0|osd_only                Orientation and script detection (OSD) only.
  1|auto_osd                Automatic page segmentation with OSD.
  2|auto_only               Automatic page segmentation, but no OSD, or OCR. (not implemented)
  3|auto                    Fully automatic page segmentation, but no OSD. (Default)
  4|single_column           Assume a single column of text of variable sizes.
  5|single_block_vert_text  Assume a single uniform block of vertically aligned text.
  6|single_block            Assume a single uniform block of text.
  7|single_line             Treat the image as a single text line.
  8|single_word             Treat the image as a single word.
  9|circle_word             Treat the image as a single word in a circle.
 10|single_char             Treat the image as a single character.
 11|sparse_text             Sparse text. Find as much text as possible in no particular order.
 12|sparse_text_osd         Sparse text with OSD.
 13|raw_line                Raw line. Treat the image as a single text line,
                            bypassing hacks that are Tesseract-specific."""

"""tesseract --help-oem
OCR Engine modes (OEM):
  0|tesseract_only          Legacy engine only.
  1|lstm_only               Neural nets LSTM engine only.
  2|tesseract_lstm_combined Legacy + LSTM engines.
  3|default                 Default, based on what is available."""

myconfig = r"--psm 11 --oem 3"

"""
text=pytesseract.image_to_string(PIL.Image.open("test2.png"),config=myconfig)
print(text)
"""

img = cv2.imread("example.jpg")
height, width, _ =img.shape

"""
boxes = pytesseract.image_to_boxes(img, config=myconfig)
print(boxes)
for box in boxes.splitlines():
    box=box.split(" ")
    img = cv2.rectangle(img,(int(box[1]),height-int(box[2])), (int(box[3]),height-int(box[4])), (0,255,0), 2)

"""
data = pytesseract.image_to_data(img, config=myconfig, output_type=Output.DICT)

"""
print(data.keys())
print(data['text'])
"""
amount_boxes= len(data['text'])
for i in range(amount_boxes):
    if float(data['conf'][i])>75:
        (x,y,width,height)=(data['left'][i],data['top'][i],data['width'][i],data['height'][i])
        img=cv2.rectangle(img,(x,y),(x+width,y+height),(0,255,0),2)
        #img=cv2.putText(img,data['text'][i],(x,y+height+20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2,cv2.LINE_AA)
        
cv2.imshow("img",img)
cv2.waitKey(0)