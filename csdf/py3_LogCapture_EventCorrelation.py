"""
QUESTION 3 (CSDF):
Write a program to capture log events from a log file and correlate them:
group events by IP address and flag repeated failed login attempts
(brute-force detection).

HOW IT WORKS:
1. CREATE SAMPLE LOG - writes the embedded sample events to system.log so
   the demo is self-contained. Line format:
       "<date> <time> EVENT user=<name> ip=<address>"
2. CAPTURE - parse every line with a regex capturing timestamp, event
   name, user and IP; convert the timestamp with strptime so events are
   structured data (queryable), not raw text.
3. CORRELATE - bucket events per IP, then per IP report:
       - total event count,
       - failed login count,
       - STATUS: SUSPICIOUS ACTIVITY DETECTED (>= 3 failed logins)
         or STATUS: Normal Activity.
   The forensic idea: one failed login is noise, three failures from the
   SAME IP is a pattern - correlation turns events into evidence.

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 csdf/py3_LogCapture_EventCorrelation.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import re
from collections import defaultdict
from datetime import datetime


# ============================================================
# STEP 2 : CREATE THE FILE - hardcoded sample log data written
#          to system.log (the file used by the next steps)
# ============================================================
LOG_FILE = "system.log"

SAMPLE_LOGS = """2026-10-04 10:00:01 LOGIN_SUCCESS user=admin ip=192.168.1.10
2026-10-04 10:01:12 LOGIN_FAILED user=admin ip=192.168.1.20
2026-10-04 10:01:45 LOGIN_FAILED user=admin ip=192.168.1.20
2026-10-04 10:02:10 LOGIN_FAILED user=admin ip=192.168.1.20
2026-10-04 10:03:05 LOGIN_SUCCESS user=user1 ip=192.168.1.15
2026-10-04 10:04:20 FILE_ACCESS user=user1 ip=192.168.1.15
2026-10-04 10:05:30 LOGIN_FAILED user=guest ip=192.168.1.30
"""

LINE_PATTERN = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "   # group 1: timestamp
    r"(\S+) user=(\S+) ip=(\S+)"                # groups 2,3,4: event/user/ip
)


def create_sample_log():
    """(Re)write the sample log so the next steps have a file to parse."""
    with open(LOG_FILE, "w") as file:
        file.write(SAMPLE_LOGS)


# ============================================================
# STEP 3 : USE THE FILE - capture (parse) the log events
# ============================================================
def capture_logs():
    """Parse every well-formed line into an event dict."""
    events = []
    with open(LOG_FILE) as file:
        for line in file:
            match = LINE_PATTERN.match(line.strip())
            if match:
                events.append({
                    "time": datetime.strptime(match.group(1),
                                              "%Y-%m-%d %H:%M:%S"),
                    "event": match.group(2),
                    "user": match.group(3),
                    "ip": match.group(4),
                })
    return events


# ============================================================
# STEP 4 : CORRELATE - group by IP, count failures, flag sources
# ============================================================
def correlate_events(events):
    """Group events per IP, count failures, flag suspicious sources."""
    ip_events = defaultdict(list)
    for event in events:
        ip_events[event["ip"]].append(event)

    print("\n----- EVENT CORRELATION -----")
    for ip, records in ip_events.items():
        failed_count = sum(1 for e in records if e["event"] == "LOGIN_FAILED")

        print("\nIP Address:", ip)
        print("Total Events:", len(records))
        print("Failed Login Attempts:", failed_count)

        for e in records:
            print(e["time"], "|", e["event"], "| User:", e["user"])

        if failed_count >= 3:                     # the lab threshold
            print("STATUS: SUSPICIOUS ACTIVITY DETECTED")
        else:
            print("STATUS: Normal Activity")


# ============================================================
# STEP 5 : DRIVER - create file -> capture -> print -> correlate
# ============================================================
def run():
    print("==============================")
    print(" LOG CAPTURING TOOL")
    print("==============================")

    print("\nCapturing logs...")
    create_sample_log()                            # STEP 2 action
    events = capture_logs()                        # STEP 3 action
    print("Total log events captured:", len(events))

    print("\n----- CAPTURED LOGS -----")
    for e in events:
        print(e["time"], "|", e["event"], "| User:", e["user"], "| IP:", e["ip"])

    correlate_events(events)                       # STEP 4 action


if __name__ == "__main__":
    run()