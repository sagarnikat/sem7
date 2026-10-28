"""
PROBLEM STATEMENT : CAPTCHA Generation & Verification (CSDF)

A CAPTCHA ("Completely Automated Public Turing test to tell Computers and
Humans Apart") blocks automated abuse of web form sign-ins/sign-ups by
requiring the user to read distorted text that OCR bots find hard to parse.

HOW THIS PROGRAM WORKS:
1. GENERATE - a random 6-character secret is drawn from letters + digits.
2. DRAW    - Pillow renders the secret as black text on a 250x80 white
             canvas, then overdraws 8 random gray lines (the noise). The
             noise breaks up the letter outline so simple template/OCR
             matching fails, but a human still reads it easily.
3. SAVE/SHOW - the image is written to captcha.png and opened in the
             system viewer so the user can look at it.
4. VERIFY  - the program asks the user to type what they see. The answer
             is compared EXACTLY with the generated secret (case-sensitive).
             Correct  -> "CAPTCHA Verified Successfully!"
             Wrong    -> "Incorrect CAPTCHA. Verification Failed."

WHY NOT C++ FOR THIS PRACTICAL:
Generating and displaying images without third-party GUI libraries would
mean hand-writing a PNG encoder plus rasterizer. Python's Pillow does that
in one call, so the practical stays in Python by design.

NOTES / INFO:
- Needs Pillow:  sudo apt install python3-pil   (or: pip install pillow)
- Run:           python3 "csdf/Captcha.py"
- captcha.png is saved in the CURRENT working directory (overwrites an
  existing file of the same name).
- Real CAPTCHAs add per-character rotation/random jitter, wavy warping and
  colour backgrounds - the distortion shown here is the textbook minimum.
- Verification should always happen on the SERVER (like this script); a
  client-side check is trivially bypassed.
"""

import random  # character choice + noise-line coordinates
import string  # ascii_letters + digits character pool

from PIL import Image, ImageDraw, ImageFont  # rendering


def generate_captcha_text(length=6):
    """Random secret of `length` letters/digits; the expected answer."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def draw_captcha_image(captcha_text, width=250, height=80):
    """Render the secret text with random noise lines and return the image."""
    image = Image.new("RGB", (width, height), "white")  # blank white canvas
    draw = ImageDraw.Draw(image)

    # A TrueType font gives clean large glyphs; fall back to the tiny
    # built-in bitmap font if DejaVu Sans is not installed.
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40
        )
    except OSError:
        font = ImageFont.load_default()

    # The secret digits themselves (drawn every time).
    draw.text((50, 20), captcha_text, font=font, fill="black")

    # Distortion: 8 random gray lines that cut across the glyphs.
    for _ in range(8):
        x1 = random.randint(0, width - 1)
        y1 = random.randint(0, height - 1)
        x2 = random.randint(0, width - 1)
        y2 = random.randint(0, height - 1)
        draw.line((x1, y1, x2, y2), fill="gray", width=2)

    return image


def verify_user_answer(captcha_text):
    """Exactly-once interactive check; True = human passed the test."""
    user_input = input("Enter the CAPTCHA shown in the image: ")
    return user_input == captcha_text


def run():
    """Steps 1-4 above; main() only calls this."""
    captcha_text = generate_captcha_text()
    image = draw_captcha_image(captcha_text)

    image.save("captcha.png")  # keep on disk for reference/verification
    image.show()               # open in the system image viewer

    if verify_user_answer(captcha_text):
        print("CAPTCHA Verified Successfully!")
    else:
        print("Incorrect CAPTCHA. Verification Failed.")


if __name__ == "__main__":
    run()
