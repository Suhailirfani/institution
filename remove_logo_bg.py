"""
Remove white background from the Adabiyya logo and save as transparent PNG.
Uses only Pillow (no numpy needed).
"""
from PIL import Image

img = Image.open(r'd:\work\adabiyya\static\img\adabiyya_logo_new.png').convert('RGBA')
datas = img.getdata()

newData = []
for item in datas:
    r, g, b, a = item
    # Make near-white pixels transparent
    if r > 240 and g > 240 and b > 240:
        newData.append((r, g, b, 0))
    else:
        newData.append(item)

img.putdata(newData)
img.save(r'd:\work\adabiyya\static\img\ADABIYYA_LOGO.png', 'PNG')
img.save(r'd:\work\adabiyya\static\img\ADABIYYA_FAVICON.png', 'PNG')

print("Done! White background removed.")
print(f"Size: {img.size}")
