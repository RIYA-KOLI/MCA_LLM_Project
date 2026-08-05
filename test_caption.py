from vision.caption import analyze_image
import os

image = r"C:\Users\user\Downloads\test.png"

print("Using image:", image)
print("Exists:", os.path.exists(image))

result = analyze_image(...)

print(result)