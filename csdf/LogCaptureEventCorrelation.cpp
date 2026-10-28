/*
 * PROBLEM STATEMENT : Log Capturing & Event Correlation (CSDF)
 *
 * Build a miniature host-security monitor: capture events from a log file,
 * group them by the source IP address, and correlate the events to flag
 * brute-force-style behaviour (a burst of failed logins from the same IP
 * followed by quiet or continued activity is the classic pre-attack sign).
 *
 * HOW THIS PROGRAM WORKS:
 *   1. CREATE SAMPLE LOG  - writes the embedded sample events to system.log so
 *      the demonstration is self-contained (same lines the lab uses).
 *      Every line: "<timestamp> EVENT user=<name> ip=<address>".
 *   2. CAPTURE - a regex pulls the timestamp, event name, user and IP out of
 *      every well-formed line, converting the timestamp to structured
 *      fields - raw text is unqueryable; parsed events are not.
 *   3. CORRELATE - bucket the events by IP, then per IP:
 *        - total event count,
 *        - how many are LOGIN_FAILED,
 *        - STATUS: SUSPICIOUS (>= 3 failed logins, the lab threshold)
 *          or STATUS: Normal Activity.
 *      Correlation is the key forensic idea: a single failed login is noise;
 *      three failures from one IP is a pattern.
 *
 * COMPLEXITY:
 *   O(lines) to capture, O(lines) to bucket and report = linear.
 *
 * NOTES / INFO:
 *   - system.log is overwritten each run (same behaviour as the lab file);
 *     move it aside if you have your own copy there.
 *   - Log file paths relative to the CURRENT directory, not the binary's.
 *   - Real tools (fail2ban, SIEM systems) do the same buckets across many
 *     sources, at much larger scale and with time-window heuristics.
 */

#include <ctime>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

const string LOG_FILE = "system.log";

// One parsed audit event.
struct Event {
    string time;     // original timestamp text, e.g. "2026-10-04 10:01:12"
    string event;    // LOGIN_SUCCESS / LOGIN_FAILED / FILE_ACCESS
    string user;     // user=<name> field
    string ip;       // ip=<address> field
};

// The demonstration log content (identical lines to the lab script).
const string SAMPLE_LOGS =
    "2026-10-04 10:00:01 LOGIN_SUCCESS user=admin ip=192.168.1.10\n"
    "2026-10-04 10:01:12 LOGIN_FAILED user=admin ip=192.168.1.20\n"
    "2026-10-04 10:01:45 LOGIN_FAILED user=admin ip=192.168.1.20\n"
    "2026-10-04 10:02:10 LOGIN_FAILED user=admin ip=192.168.1.20\n"
    "2026-10-04 10:03:05 LOGIN_SUCCESS user=user1 ip=192.168.1.15\n"
    "2026-10-04 10:04:20 FILE_ACCESS user=user1 ip=192.168.1.15\n"
    "2026-10-04 10:05:30 LOGIN_FAILED user=guest ip=192.168.1.30\n";

// Step 1: (re)write the sample log so the demo has data to parse.
void createSampleLog() {
    ofstream file(LOG_FILE);
    file << SAMPLE_LOGS;
}

// Step 2: parse every well-formed line into an Event (regex-free: split on
// spaces, the format is fixed "time time event user=... ip=...").
vector<Event> captureLogs() {
    vector<Event> events;
    ifstream file(LOG_FILE);

    string time, timeOnly, event, userField, ipField;
    while (file >> time >> timeOnly >> event >> userField >> ipField) {
        // The timestamp is written as two whitespace-separated tokens:
        // "<date> <clock>"; join them back into one field.
        Event e;
        e.time = time + " " + timeOnly;
        e.event = event;
        e.user = userField.substr(userField.find('=') + 1);  // strip "user="
        e.ip = ipField.substr(ipField.find('=') + 1);        // strip "ip="
        events.push_back(e);
    }
    return events;
}

// Step 3: group by IP, count failures, flag suspicious sources.
void correlateEvents(const vector<Event>& events) {
    // Events bucketed per IP (std::map keeps the IPs sorted for clean output).
    map<string, vector<Event>> ipEvents;
    for (const Event& e : events) ipEvents[e.ip].push_back(e);

    cout << "\n----- EVENT CORRELATION -----\n";
    for (const auto& [ip, records] : ipEvents) {
        int failedCount = 0;
        for (const Event& e : records)
            if (e.event == "LOGIN_FAILED") ++failedCount;

        cout << "\nIP Address: " << ip << "\n";
        cout << "Total Events: " << records.size() << "\n";
        cout << "Failed Login Attempts: " << failedCount << "\n";

        for (const Event& e : records)
            cout << e.time << " | " << e.event << " | User: " << e.user << "\n";

        // The lab threshold: 3+ failed logins from one IP = suspicious.
        if (failedCount >= 3)
            cout << "STATUS: SUSPICIOUS ACTIVITY DETECTED\n";
        else
            cout << "STATUS: Normal Activity\n";
    }
}

// Print every captured event, one per line, in capture order.
void printCapturedLogs(const vector<Event>& events) {
    cout << "\n----- CAPTURED LOGS -----\n";
    for (const Event& e : events)
        cout << e.time << " | " << e.event << " | User: " << e.user
             << " | IP: " << e.ip << "\n";
}

// Drives the whole practical; main() only calls this.
void run() {
    cout << "==============================\n";
    cout << " LOG CAPTURING TOOL\n";
    cout << "==============================\n";

    cout << "\nCapturing logs...\n";
    createSampleLog();

    vector<Event> events = captureLogs();
    cout << "Total log events captured: " << events.size() << "\n";
    printCapturedLogs(events);
    correlateEvents(events);
}

int main() {
    run();
    return 0;
}
