/*
 * PROBLEM STATEMENT : Topic-Sensitive (Personalized) PageRank (IR)
 *
 * Regular PageRank scores a page by the whole link structure of the web, so
 * every user sees the same ranking. Topic-sensitive PageRank produces a DIFFERENT
 * ranking per topic: during each iteration the "random surfer" no longer jumps
 * to a uniform random page but prefers pages of the chosen topic.
 *
 * THE ALGORITHM (personalized power iteration):
 *   The lab data is a small web described in XML, where each page carries a
 *   topic attribute; the exercise personalizes the ranking to the topic "AI".
 *   1. Parse the XML into (a) a directed graph of pages and (b) a map
 *      page -> topic.
 *   2. Build the personalization vector p: pages whose topic equals the
 *      selected topic get 1, others get 0; normalise so sum(p) = 1.
 *   3. Iterate the PageRank recurrence with bias p:
 *          score[j = (1 - a + a * danglingMass) * p[j]
 *                + a * sum over predecessors i of score[i]/outDeg(i)]
 *      (a = 0.85 damping, as in the standard algorithm.)
 *   4. The extra term  a * danglingMass * p[j]  redistributes the mass of
 *      "dangling" pages (pages with no outgoing links, who would otherwise
 *      leak rank): their mass is re-injected through the preference vector.
 *      The (1 - a) teleport term ALSO uses p instead of 1/n, which is the
 *      actual personalization.
 *   5. Iterate until the total score change falls under a small tolerance
 *      (early exit is better than a fixed count of iterations).
 *
 * COMPLEXITY:
 *   O(iterations * E) for E edges (list-based graph), + O(n) per iteration for
 *   the dangling/convergence checks. Converges in a few dozen iterations on
 *   small graphs; tolerance-based early exit usually fires sooner.
 *
 * NOTES / INFO:
 *   - XML parsing is done with a small hand-rolled scanner, because this
 *     lab only needs <page id topic> plus <link> children - a scripting
 *     language would use its XML library instead.
 *   - Ranking an "AI" query then favours AI-labelled hubs even if a sports
 *     page receives more raw links.
 */

#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;

// The same web description the lab embeds in its script.
const string XML_DATA = R"(
<web>
    <page id="A" topic="AI">
        <link>B</link>
        <link>C</link>
    </page>

    <page id="B" topic="AI">
        <link>C</link>
        <link>D</link>
    </page>

    <page id="C" topic="Sports">
        <link>A</link>
        <link>D</link>
    </page>

    <page id="D" topic="AI">
        <link>A</link>
    </page>
</web>
)";

// A tiny directed graph over named pages (adjacency list, insertion order).
class DiGraph {
   public:
    void addNode(const string& node) { outEdges_.emplace(node, vector<string>{}); }

    void addEdge(const string& source, const string& target) {
        addNode(source);
        addNode(target);
        for (const string& existing : outEdges_[source])
            if (existing == target) return;   // no duplicate edges
        outEdges_[source].push_back(target);
    }

    const map<string, vector<string>>& edges() const { return outEdges_; }
    vector<string> nodes() const {
        vector<string> names;
        for (const auto& [node, _] : outEdges_) names.push_back(node);
        return names;
    }

   private:
    map<string, vector<string>> outEdges_;   // sorted = stable iteration order
};

// Read one attribute value ("id" or "topic") out of a "<page ...>" tag.
string readAttribute(const string& tag, const string& attributeName) {
    size_t at = tag.find(attributeName);
    if (at == string::npos) return "";
    at = tag.find('"', at);
    size_t end = tag.find('"', at + 1);
    return (at == string::npos || end == string::npos) ? ""
                                                       : tag.substr(at + 1, end - at - 1);
}

// Minimal scan of the XML: walk it tag by tag, matching <page>/<link>.
DiGraph parseXml(const string& xml, map<string, string>& pageTopics) {
    DiGraph graph;
    size_t pos = 0;
    string currentPage;

    while ((pos = xml.find('<', pos)) != string::npos) {
        size_t close = xml.find('>', pos);
        if (close == string::npos) break;
        string tag = xml.substr(pos + 1, close - pos - 1);
        pos = close + 1;

        if (tag.rfind("/page", 0) == 0) {
            currentPage.clear();          // </page> - a page block ended
        } else if (tag.rfind("page", 0) == 0) {
            currentPage = readAttribute(tag, "id");          // <page id topic>
            string topic = readAttribute(tag, "topic");
            graph.addNode(currentPage);
            pageTopics[currentPage] = topic;
        } else if (tag.rfind("link", 0) == 0) {
            size_t end = xml.find("</link>", pos);           // <link>X</link>
            string target = xml.substr(pos, end - pos);
            // Trim whitespace/newlines around the target name.
            size_t first = target.find_first_not_of(" \t\r\n");
            size_t last = target.find_last_not_of(" \t\r\n");
            if (first != string::npos) graph.addEdge(currentPage, target.substr(first, last - first + 1));
            pos = end + 7;   // skip past "</link>"
        }
    }
    return graph;
}

// Normalise the preference vector so it sums to exactly 1.
void normalize(map<string, double>& preference) {
    double total = 0.0;
    for (const auto& [_, value] : preference) total += value;
    if (total == 0.0) return;
    for (auto& [_, value] : preference) value /= total;
}

// Personalized PageRank with dangling-node handling; iterates to convergence.
map<string, double> topicPageRank(const DiGraph& graph,
                                  const map<string, string>& pageTopics,
                                  double alpha) {
    const vector<string> nodes = graph.nodes();
    const int n = static_cast<int>(nodes.size());
    map<string, double> scores;

    // Personalization vector: 1 for the selected topic's pages, 0 elsewhere.
    map<string, double> preference;
    for (const string& node : nodes) preference[node] = (pageTopics.at(node) == "AI") ? 1.0 : 0.0;
    normalize(preference);

    for (const string& node : nodes) scores[node] = 1.0 / n;   // uniform start

    const double TOLERANCE = 1e-6 / n;   // convergence threshold
    for (int iteration = 0; iteration < 100; ++iteration) {
        // Mass stranded on pages with no outgoing links.
        double danglingMass = 0.0;
        for (const string& node : nodes)
            if (graph.edges().at(node).empty()) danglingMass += scores[node];

        map<string, double> updated;
        for (const string& node : nodes)
            updated[node] = (1.0 - alpha + alpha * danglingMass) * preference[node];

        // Hand each page's score to its targets, equally split.
        for (const string& source : nodes) {
            const vector<string>& targets = graph.edges().at(source);
            if (targets.empty()) continue;
            double share = alpha * scores[source] / targets.size();
            for (const string& target : targets) updated[target] += share;
        }

        // Converged when every score changed only a hair.
        double diff = 0.0;
        for (const string& node : nodes) diff += fabs(updated[node] - scores[node]);
        scores = updated;
        if (diff < n * TOLERANCE) break;
    }
    return scores;
}

// Print edges then the topic ranking, best score first.
void printResults(const DiGraph& graph, const map<string, double>& scores,
                  const string& selectedTopic) {
    cout << "Web Graph Edges:\n";
    bool firstEdge = true;
    cout << "[";
    for (const auto& [source, targets] : graph.edges()) {
        for (const string& target : targets) {
            if (!firstEdge) cout << ", ";
            cout << "(\'" << source << "\', \'" << target << "\')";
            firstEdge = false;
        }
    }
    cout << "]\n";

    cout << "\nTopic: " << selectedTopic << "\n";
    cout << "\nTopic-Sensitive PageRank:\n";
    cout << fixed << setprecision(4);
    // std::map stores pages alphabetically, so sort the pairs by rank value.
    vector<pair<string, double>> ranked(scores.begin(), scores.end());
    sort(ranked.begin(), ranked.end(),
         [](const auto& a, const auto& b) { return a.second > b.second; });
    for (const auto& [page, score] : ranked) cout << page << " : " << score << "\n";
}

// Drives the whole practical; main() only calls this.
void run() {
    map<string, string> pageTopics;
    DiGraph graph = parseXml(XML_DATA, pageTopics);

    const string selectedTopic = "AI";
    map<string, double> scores = topicPageRank(graph, pageTopics, 0.85);

    printResults(graph, scores, selectedTopic);
}

int main() {
    run();
    return 0;
}
