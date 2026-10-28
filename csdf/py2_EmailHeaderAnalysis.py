"""
QUESTION 2 (CSDF):
Write a program to analyze an email header: print the main fields and
extract the routing IP addresses from the Received headers.

HOW IT WORKS:
1. PARSE - Python's email parser handles the folding rule automatically:
   a field starts at a non-blank character with "Name:", and every line
   indented by whitespace CONTINUES the previous field (that is why the
   Received headers span three lines each).
2. Print the identity fields: From, To, Subject, Date, Message-ID.
3. ROUTING ANALYSIS - for every Received header, print it and extract
   IPv4 addresses with the regex  \\b(\\d{1,3}\\.){3}\\d{1,3}\\b . Each hop
   records which machine sent the mail and which server received it, so
   the chain reveals the true delivery path.

FORENSICS POINT: From/Subject are trivially forgeable, but the Received
chain is stamped by receiving servers hop by hop - read it BOTTOM-UP (the
last Received header added is the FIRST hop of the journey) to unmask a
spoofed sender. Spoof giveaway here: From says example.com, but the hop
chain starts at 203.0.113.25 via smtp.example.com.

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 csdf/py2_EmailHeaderAnalysis.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import re
from email import policy
from email.parser import Parser


# ============================================================
# STEP 2 : HARDCODED DATA - the sample email header (the "file"
#          content here; no external file is needed)
# ============================================================
SAMPLE_HEADER = """From: sender@example.com
To: receiver@example.com
Subject: Important Account Update
Date: Tue, 08 Sep 2026 09:15:00 +0530
Message-ID: <12345@example.com>
Received: from mail.sender.com (192.168.1.10)
 by mail.receiver.com with ESMTP;
 Tue, 08 Sep 2026 09:15:00 +0530
Received: from smtp.example.com (203.0.113.25)
 by mail.sender.com with ESMTP;
 Tue, 08 Sep 2026 09:14:30 +0530
"""

IPV4_PATTERN = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"


# ============================================================
# STEP 3 : USE THE DATA - parse the header and analyze it
# ============================================================
def parse_header(header):
    """Parse the raw header text into a message object (folding-aware)."""
    return Parser(policy=policy.default).parsestr(header)


def print_identity_fields(msg):
    """Display the spoofable identity fields."""
    print("----- EMAIL HEADER ANALYSIS -----\n")
    print("From :", msg.get("From"))
    print("To :", msg.get("To"))
    print("Subject :", msg.get("Subject"))
    print("Date :", msg.get("Date"))
    print("Message-ID :", msg.get("Message-ID"))


def analyze_routing(msg):
    """Print every Received hop with the IPv4 addresses found inside."""
    print("\n----- EMAIL ROUTING INFORMATION -----")

    received = msg.get_all("Received", [])
    if not received:
        print("No Received header found.")
        return

    for hop, route in enumerate(received, start=1):
        print(f"\nReceived Header {hop}:")
        print(route)

        ips = re.findall(IPV4_PATTERN, str(route))   # per-hop IP extraction
        if ips:
            print("IP Address(es):", ", ".join(ips))
        else:
            print("No IP address found.")


# ============================================================
# STEP 4 : DRIVER - parse the sample header and run both analyses
# ============================================================
def run():
    msg = parse_header(SAMPLE_HEADER)

    print_identity_fields(msg)
    analyze_routing(msg)
    print("\n----- ANALYSIS COMPLETE -----")


if __name__ == "__main__":
    run()