# Makes a phone-photo-quality copy of a sample folder: rotate, blur, noise, low JPEG quality.
import glob, os, sys
import numpy as np
from PIL import Image, ImageFilter

src = sys.argv[1]
dst = src + "_degraded"
os.makedirs(dst, exist_ok=True)
rng = np.random.default_rng(0)
for p in glob.glob(os.path.join(src, "*.png")):
    img = Image.open(p).convert("L").rotate(2.5, expand=True, fillcolor=255)
    img = img.filter(ImageFilter.GaussianBlur(1.1))
    a = np.asarray(img, dtype=float) + rng.normal(0, 14, (img.height, img.width))
    a = (a * 0.85 + 20).clip(0, 255).astype("uint8")  # dim, low contrast
    Image.fromarray(a).save(os.path.join(dst, os.path.basename(p)[:-4] + ".jpg"), quality=35)
print("wrote", dst)
