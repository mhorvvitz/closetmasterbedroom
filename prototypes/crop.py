from PIL import Image
import sys
src = r'C:\projects\MasterBedRoomClosetDesign\Screenshots\Screenshot 2026-08-15 213613.png'
out = r'C:\Users\mhorv\AppData\Local\Temp\claude\C--projects-MasterBedRoomClosetDesign\efbed5a2-caa8-4e16-b351-fd93944dae12\scratchpad'
im = Image.open(src).convert('RGB')
W, H = im.size
crops = {
    'full':      (0, 0, W, H),
    'closet':    (110, 0, 470, 300),
    'diagonal':  (110, 20, 320, 240),
    'rightside': (280, 0, 470, 330),
    'bottom':    (150, 180, 420, 365),
}
for name, box in crops.items():
    c = im.crop(box)
    f = 5 if name != 'full' else 3
    c = c.resize((c.width * f, c.height * f), Image.LANCZOS)
    c.save(f'{out}\\z_{name}.png')
    print(name, box, '->', c.size)
