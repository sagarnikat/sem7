/*
 * PROBLEM STATEMENT : Email Header Analysis (Cyber Security & Digital Forensics)
 *
 * An email travels through several mail servers, and each hop stamps a
 * "Received:" header on top of the message. Incidence responders read these
 * headers to reconstruct the TRUE delivery path and unmask a spoofed
 * sender - the From/Subject lines are trivially forgeable, but the Received
 * chain written by the receiving servers is far harder to fake.
 *
 * HOW THIS PROGRAM WORKS:
 *   1. The sample header (several fields plus two Received hops) is embedded
 *      in the program.
 *   2. Parsing rule: a header field starts on a fresh line at a non-blank
 *      character with a "Name:" pattern; every following line indented with
 *      whitespace is a CONTINUATION of the same field (that is how the
 *      multi-line Received headers are folded).
 *   3. Display the identity fields - From, To, Subject, Date, Message-ID.
 *   4. For every Received header, print it and extract IPv4 addresses with a
 *      regex \b(d{1,3}.){3}d{1,3}\b. Each hop shows the machine the server
 *      received the mail from and the server that did the receiving, so the
 *      address chain tells the delivery route.
 *
 * COMPLEXITY:
 *   O(lines + matches) - one pass to fold fields, regex scans per field.
 *
 * NOTES / INFO:
 *   - Headers are read BOTTOM-UP in real analysis: the LAST Received header
 *     added (the last one in the file) is the FIRST hop of the journey.
 *   - The IPv4 regex deliberately does not validate octet ranges; the lab
 *     keeps it simple. RFC 4408-style checks would tighten it.
 *   - Try spotting the spoof: From says example.com, but the hop chain starts
 *     at 203.0.113.25 through mail.sender.com.
 */

#include <iostream>
#include <regex>
#include <string>
#include <vector>

using namespace std;

// The sample email header analysed by this exercise (same one as the lab).
const string SAMPLE_HEADER = R"(From: sender@example.com
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
)";

// Fold raw header text into "name", "folded value" pairs:
// a line starting with whitespace continues the previous field.
vector<pair<string, string>> parseHeader(const string& raw) {
    vector<pair<string, string>> fields;
    size_t pos = 0;

    while (pos < raw.size()) {
        size_t lineEnd = raw.find('\n', pos);
        if (lineEnd == string::npos) lineEnd = raw.size();
        string line = raw.substr(pos, lineEnd - pos);
        pos = lineEnd + 1;
        if (!line.empty() && line.back() == '\r') line.pop_back();

        if (line.empty()) continue;

        if (isspace(static_cast<unsigned char>(line[0]))) {
            // Continuation: append (unfolded) to the most recent field.
            if (!fields.empty()) fields.back().second += "\n" + line;
        } else {
            // New field: split at the first colon "Name: value".
            size_t colon = line.find(':');
            if (colon != string::npos)
                fields.emplace_back(line.substr(0, colon),
                                    line.substr(colon + 2));
        }
    }
    return fields;
}

// Pull the value of one specific field from the parsed list.
string getField(const vector<pair<string, string>>& fields, const string& name) {
    for (const auto& [fieldName, value] : fields)
        if (fieldName == name) return value;
    return "";
}

// All IPv4 literals inside one folded header string (regex per lab).
vector<string> extractIpv4(const string& text) {
    static const regex IPV4_PATTERN(R"(\b(?:\d{1,3}\.){3}\d{1,3}\b)");
    vector<string> ips;
    auto begin = sregex_iterator(text.begin(), text.end(), IPV4_PATTERN);
    auto end = sregex_iterator();
    for (auto match = begin; match != end; ++match) ips.push_back(match->str());
    return ips;
}

// Show the identity fields and dissect every Received hop in order.
void analyzeHeader(const vector<pair<string, string>>& fields) {
    cout << "----- EMAIL HEADER ANALYSIS -----\n\n";
    cout << "From        : " << getField(fields, "From") << "\n";
    cout << "To          : " << getField(fields, "To") << "\n";
    cout << "Subject     : " << getField(fields, "Subject") << "\n";
    cout << "Date        : " << getField(fields, "Date") << "\n";
    cout << "Message-ID  : " << getField(fields, "Message-ID") << "\n";

    cout << "\n----- EMAIL ROUTING INFORMATION -----\n";
    int hop = 0;
    for (const auto& [name, value] : fields) {
        if (name != "Received") continue;
        ++hop;
        cout << "\nReceived Header " << hop << ":\n" << value << "\n";

        vector<string> ips = extractIpv4(value);
        if (ips.empty()) {
            cout << "No IP address found.\n";
        } else {
            cout << "IP Address(es): ";
            for (size_t i = 0; i < ips.size(); ++i)
                cout << (i ? ", " : "") << ips[i];
            cout << "\n";
        }
    }
    if (hop == 0) cout << "No Received header found.\n";

    cout << "\n----- ANALYSIS COMPLETE -----\n";
}

// Drives the whole practical; main() only calls this.
void run() {
    vector<pair<string, string>> fields = parseHeader(SAMPLE_HEADER);
    analyzeHeader(fields);
}

int main() {
    run();
    return 0;
}
