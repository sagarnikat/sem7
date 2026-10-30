"""
QUESTION 1 (CSDF):
Write a program to generate a CAPTCHA (image with distorted text), display
it, and verify the text entered by the user.

HOW IT WORKS (NO PIL - PURE STANDARD LIBRARY):
1. GENERATE - a random 6-character secret is drawn from UPPERCASE letters
   + digits (like real CAPTCHAs; verification is case-insensitive).
2. RENDER  - the secret is rasterized from a built-in 5x7 BITMAP FONT
   (the hardcoded dataset in STEP 2). Every font pixel becomes a 4x4
   block, each character gets a random vertical jitter, and 8 random gray
   noise lines + salt-and-pepper pixels destroy the outlines. That noise
   is what defeats simple OCR while humans still read it.
3. SAVE/SHOW - the pixel grid is written as a REAL PNG file by hand
   (zlib compress + struct headers - no image library needed) as
   captcha.png, an ASCII preview is printed in the terminal (works even
   over SSH), and the file is opened in the system viewer.
4. VERIFY  - the user's answer is compared with the secret, ignoring
   case, exactly like real CAPTCHA validation.

WHY NO PIL: the original lab version used Pillow to draw the image. This
version avoids that dependency completely - the PNG format is written
manually (magic bytes + IHDR + IDAT + IEND chunks, CRC-checked).

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 csdf/py1_Captcha.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import random
import string
import struct
import subprocess
import zlib


# ============================================================
# STEP 2 : HARDCODED DATA - built-in 5x7 bitmap font for
#          A-Z and 0-9 (the "dataset" this program draws from)
# ============================================================
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
}

CAPTCHA_CHARS = string.ascii_uppercase + string.digits  # A-Z, 0-9
SCALE = 4          # each font pixel becomes a 4x4 block
MARGIN = 12        # white border in pixels
NOISE_LINES = 8    # number of gray noise lines drawn across the text


# ============================================================
# STEP 3 : CREATE THE FILE - render the secret into a pixel grid
#          and write it out as a real PNG (captcha.png)
# ============================================================
def generate_captcha_text(length=6):
    """The secret: `length` random uppercase letters/digits."""
    return "".join(random.choice(CAPTCHA_CHARS) for _ in range(length))


def draw_line(grid, x1, y1, x2, y2, color=150):
    """Bresenham line - used for the noise lines that cut the glyphs."""
    dx, dy = abs(x2 - x1), -abs(y2 - y1)
    step_x, step_y = (1 if x1 < x2 else -1), (1 if y1 < y2 else -1)
    error = dx + dy
    while True:
        if 0 <= y1 < len(grid) and 0 <= x1 < len(grid[0]):
            grid[y1][x1] = color
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * error
        if e2 >= dy:
            error += dy
            x1 += step_x
        if e2 <= dx:
            error += dx
            y1 += step_y


def render_captcha(secret):
    """Rasterize the secret + jitter + noise into a 2-D grayscale grid."""
    glyph_w, glyph_h = 5 * SCALE, 7 * SCALE
    width = MARGIN * 2 + len(secret) * glyph_w + (len(secret) - 1) * SCALE
    height = MARGIN * 2 + glyph_h

    grid = [[255] * width for _ in range(height)]      # white background

    for i, char in enumerate(secret):
        glyph = FONT[char]
        x0 = MARGIN + i * (glyph_w + SCALE)
        y0 = MARGIN + random.randint(-SCALE, SCALE)    # vertical jitter
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit == "1":                         # fill a SCALE x SCALE block
                    for dy in range(SCALE):
                        for dx in range(SCALE):
                            grid[y0 + row * SCALE + dy][x0 + col * SCALE + dx] = 0

    # Distortion: random gray lines cutting across the glyphs.
    for _ in range(NOISE_LINES):
        draw_line(grid,
                  random.randint(0, width - 1), random.randint(0, height - 1),
                  random.randint(0, width - 1), random.randint(0, height - 1))

    # Salt-and-pepper noise: a few random dark specks.
    for _ in range(width * height // 100):
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        grid[y][x] = random.randint(80, 160)
    return grid


def write_png(filename, grid):
    """Minimal pure-stdlib PNG writer (8-bit grayscale, no filter tricks)."""
    raw = b"".join(b"\x00" + bytes(row) for row in grid)  # 0 = no filter/row

    def chunk(tag, data):
        payload = tag + data
        crc = zlib.crc32(payload) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + payload + struct.pack(">I", crc)

    header = struct.pack(">IIBBBBB", len(grid[0]), len(grid), 8, 0, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", header)
           + chunk(b"IDAT", zlib.compress(raw))
           + chunk(b"IEND", b""))
    with open(filename, "wb") as file:
        file.write(png)


def print_ascii_preview(grid):
    """Terminal preview of the image (useful on headless/SSH machines)."""
    print("\nCAPTCHA preview (terminal):")
    for y in range(0, len(grid), SCALE):
        line = "".join("#" if grid[y][x] < 200 else " "
                       for x in range(0, len(grid[0]), SCALE))
        print("  " + line)


def create_captcha_file():
    """Generate secret, render it, save captcha.png, show both previews."""
    secret = generate_captcha_text()
    grid = render_captcha(secret)
    write_png("captcha.png", grid)                # the file created here
    print("CAPTCHA image saved as captcha.png")
    print_ascii_preview(grid)
    return secret


# ============================================================
# STEP 4 : USE THE FILE - open it in the viewer and verify input
# ============================================================
def open_image(filename):
    """Try to open the PNG in the system viewer (skip silently on headless)."""
    try:
        subprocess.run(["xdg-open", filename],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=3)
    except Exception:
        pass   # no viewer / headless machine: the ASCII preview already shown


def verify_user_answer(captcha_text):
    """Case-insensitive check - exactly how real CAPTCHAs compare."""
    user_input = input("\nEnter the CAPTCHA shown in the image: ")
    return user_input.strip().upper() == captcha_text


# ============================================================
# STEP 5 : DRIVER - create file -> open -> verify
# ============================================================
def run():
    secret = create_captcha_file()          # STEP 3 (creates captcha.png)
    open_image("captcha.png")               # STEP 4 (best effort)
    if verify_user_answer(secret):
        print("CAPTCHA Verified Successfully!")
    else:
        print("Incorrect CAPTCHA. Verification Failed.")


if __name__ == "__main__":
    run()