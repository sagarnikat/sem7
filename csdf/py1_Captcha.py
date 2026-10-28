"""
QUESTION 1 (CSDF):
Write a program to generate a CAPTCHA (image with distorted text), display
it, and verify the text entered by the user.

HOW IT WORKS:
1. GENERATE - a random 6-character secret is drawn from letters + digits.
2. DRAW    - Pillow renders the secret as black text on a 250x80 white
             canvas, then overdraws 8 random gray lines. The noise breaks
             the glyph outlines so simple OCR fails, but humans still read
             it easily - the whole point of a CAPTCHA.
3. SAVE/SHOW - write captcha.png (current working directory) and open the
             system image viewer.
4. VERIFY  - compare the user's typed answer EXACTLY (case-sensitive) with
             the generated secret.

COMMANDS (run from the repository root):
    install dependencies : sudo apt install python3-pil  (or pip install pillow)
    run the program      : python3 csdf/py1_Captcha.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import random
import string

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# STEP 2 : CREATE THE FILE - generate the secret text and draw
#          the CAPTCHA image, then save it as captcha.png
#          (hardcoded canvas size + noise count; no dataset needed)
# ============================================================
def generate_captcha_text(length=6):
    """The secret: `length` random letters/digits (the expected answer)."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def draw_captcha_image(captcha_text, width=250, height=80):
    """Render the secret text plus random noise lines onto an image."""
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Prefer a large TrueType font; fall back to the tiny default bitmap font.
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40
        )
    except OSError:
        font = ImageFont.load_default()

    draw.text((50, 20), captcha_text, font=font, fill="black")

    # Distortion: 8 random gray lines cutting across the glyphs.
    for _ in range(8):
        x1, y1 = random.randint(0, width - 1), random.randint(0, height - 1)
        x2, y2 = random.randint(0, width - 1), random.randint(0, height - 1)
        draw.line((x1, y1, x2, y2), fill="gray", width=2)
    return image


def create_captcha_file():
    """Generate secret + image, save captcha.png, return the secret."""
    captcha_text = generate_captcha_text()
    image = draw_captcha_image(captcha_text)
    image.save("captcha.png")          # the file created in this step
    print("CAPTCHA image saved as captcha.png")
    return captcha_text


# ============================================================
# STEP 3 : USE THE FILE - show the image and verify the answer
# ============================================================
def verify_user_answer(captcha_text):
    """Ask the user and compare with the secret; True = passed."""
    user_input = input("Enter the CAPTCHA shown in the image: ")
    return user_input == captcha_text


# ============================================================
# STEP 4 : DRIVER - create file -> show -> verify
# ============================================================
def run():
    captcha_text = create_captcha_file()

    from PIL import Image as PILImage          # open the saved file again
    saved = PILImage.open("captcha.png")
    saved.show()                               # open in the system viewer

    if verify_user_answer(captcha_text):
        print("CAPTCHA Verified Successfully!")
    else:
        print("Incorrect CAPTCHA. Verification Failed.")


if __name__ == "__main__":
    run()