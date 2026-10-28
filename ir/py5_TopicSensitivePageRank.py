"""
QUESTION 5 (IR):
Write a program for topic-specific (topic-sensitive) PageRank: parse an
XML web description, build the directed graph, and compute PageRank
personalized to a chosen topic ("AI" in the lab example).

HOW IT WORKS:
1. PARSE - the XML lists <page id topic> elements with <link> children;
   build (a) a directed graph over page names and (b) page -> topic map.
2. PERSONALIZATION VECTOR - pages of the selected topic get 1, others 0;
   normalize so the vector sums to 1. During every iteration the "random
   surfer" TELEPORTS to a topic page instead of a uniform random page -
   that bias is what makes the ranking topic-sensitive.
3. ITERATE with dangling-page handling:
       score[j] = (1 - a + a * danglingMass) * p[j]
                  + a * sum(score[i] / outDegree(i))  over predecessors i
   - p = the personalization vector (replaces 1/n of plain PageRank)
   - danglingMass = total rank on pages with NO outgoing links; without
     this term that mass would leak out of the system every iteration.
4. STOP when the total score change drops below a tolerance.

RESULT: AI-topic queries favour AI-labelled pages even when a Sports page
receives more raw links - personalized search in a nutshell.

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 ir/py5_TopicSensitivePageRank.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import xml.etree.ElementTree as ET


# ============================================================
# STEP 2 : HARDCODED DATA - the XML web description (the "file" here)
# ============================================================
XML_DATA = """
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
"""

SELECTED_TOPIC = "AI"
ALPHA = 0.85            # damping factor (same as plain PageRank)
MAX_ITER = 100
TOLERANCE = 1e-6


# ============================================================
# STEP 3 : USE THE DATA - parse the XML, then personalized PageRank
# ============================================================
def parse_web_graph(xml_data):
    """Parse the XML into (graph = page -> [targets], page -> topic map)."""
    root = ET.fromstring(xml_data)
    graph, topics = {}, {}

    for page in root.findall("page"):
        page_id = page.get("id")
        topics[page_id] = page.get("topic")
        graph[page_id] = [
            (link.text or "").strip()
            for link in page.findall("link")
            if (link.text or "").strip()
        ]
    return graph, topics


def topic_page_rank(graph, topics, topic, alpha=ALPHA):
    """Personalized PageRank with dangling-mass redistribution."""
    nodes = list(graph)

    # Personalization vector: 1 for the topic's pages, normalized to sum 1.
    hits = [node for node in nodes if topics[node] == topic]
    preference = {node: (1 / len(hits) if topics[node] == topic else 0.0)
                  for node in nodes}

    scores = {node: 1 / len(nodes) for node in nodes}   # uniform start

    for _ in range(MAX_ITER):
        # Mass stranded on pages with no outgoing links.
        dangling_mass = sum(scores[node] for node in nodes if not graph[node])

        updated = {
            node: (1 - alpha + alpha * dangling_mass) * preference[node]
            for node in nodes
        }
        for source in nodes:
            targets = graph[source]
            if not targets:
                continue
            share = alpha * scores[source] / len(targets)   # equal split
            for target in targets:
                updated[target] += share

        # Converged when the total change is tiny.
        change = sum(abs(updated[node] - scores[node]) for node in nodes)
        scores = updated
        if change < len(nodes) * TOLERANCE:
            break
    return scores


# ============================================================
# STEP 4 : DRIVER - parse, rank, and print the topic ranking
# ============================================================
def run():
    graph, topics = parse_web_graph(XML_DATA)

    print("Web Graph Edges:")
    print([(source, target) for source, targets in graph.items()
           for target in targets])

    scores = topic_page_rank(graph, topics, SELECTED_TOPIC)

    print("\nTopic:", SELECTED_TOPIC)
    print("\nTopic-Sensitive PageRank:")
    for page, score in sorted(scores.items(), key=lambda kv: kv[1], reverse=True):
        print(page, ":", round(score, 4))


if __name__ == "__main__":
    run()
