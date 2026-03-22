from PIL import Image

img = Image.open("utility/uncleaned_sprite-Photoroom.png")
# sprite = img.resize((64, 16), resample=Image.NEAREST)
sprite = img.resize((64, 112), resample=Image.NEAREST)
sprite.save("vendor_4.png")
