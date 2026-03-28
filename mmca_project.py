import networkx as nx
import matplotlib.pyplot as plt

# Create directed graph
G = nx.DiGraph()

# ---- USER INPUT ----
n = int(input("Enter number of referrals: "))

referrals = []
print("Enter referrals in format: DoctorA DoctorB (means A refers to B)\n")

for i in range(n):
    src, dst = input(f"Referral {i+1}: ").split()
    referrals.append((src, dst))

# Add edges
G.add_edges_from(referrals)

# ---- CENTRALITY CALCULATIONS ----
in_degree = dict(G.in_degree())
out_degree = dict(G.out_degree())
betweenness = nx.betweenness_centrality(G)
closeness = nx.closeness_centrality(G)

# ---- PRINT RESULTS ----
print("\n===== CENTRALITY RESULTS =====")
print("In-Degree:", in_degree)
print("Out-Degree:", out_degree)
print("Betweenness:", betweenness)
print("Closeness:", closeness)

# ---- CONCLUSION ----
print("\n===== CONCLUSION =====")

# Hub doctor
max_in = max(in_degree, key=in_degree.get)
print(f"Most Referred Doctor (Hub): {max_in}")

# Most referring doctor
max_out = max(out_degree, key=out_degree.get)
print(f"Doctor Referring Most Patients: {max_out}")

# Bridge doctor
max_between = max(betweenness, key=betweenness.get)
print(f"Bridge Doctor (High Betweenness): {max_between}")

# Network type
if in_degree[max_in] >= len(G.nodes()) - 1:
    print("Network Type: Highly Centralized")
    print("Observation: One doctor is overloaded.")
else:
    print("Network Type: Distributed")
    print("Observation: Load is balanced among doctors.")

# Final summary
print("\nOverall Conclusion:")
print("This model helps identify key doctors and referral patterns.")
print("It can improve hospital efficiency and reduce overload.")

# ---- GRAPH ----
plt.figure(figsize=(8,6))
pos = nx.spring_layout(G)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3000,
    node_color='lightblue',
    font_size=10,
    arrows=True
)

plt.title("Hospital Referral Network")
plt.show()
