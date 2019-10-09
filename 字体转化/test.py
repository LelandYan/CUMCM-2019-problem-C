from PIL import Image
import pytesseract

text = pytesseract.image_to_string(Image.open("2.png"))
print(text)