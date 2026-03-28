import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Hospital Referral Network", layout="wide")

st.title("🏥 Hospital Referral Network Analysis")

# ---- SESSION STATE ----
if "referrals" not in st.session_state:
    st.session_state.referrals = []

# ---- DOCTOR INPUT ----
st.sidebar.header("➕ Add Referral")

doctor_list = ["DrA", "DrB", "DrC", "DrD", "DrE", "DrF"]

src = st.sidebar.selectbox("Referring Doctor", doctor_list)
dst = st.sidebar.selectbox("Referred To", doctor_list)

if st.sidebar.button("Add Referral"):
    if src != dst:
        st.session_state.referrals.append((src, dst))
    else:
        st.sidebar.warning("Doctor cannot refer to themselves")

# ---- CLEAR BUTTON ----
if st.sidebar.button("Clear All"):
    st.session_state.referrals = []

# ---- DISPLAY CURRENT DATA ----
st.subheader("📋 Current Referrals")
st.write(st.session_state.referrals)

# ---- BUILD GRAPH ----
G = nx.DiGraph()
G.add_edges_from(st.session_state.referrals)

if len(G.nodes()) > 0:

    # ---- CENTRALITY ----
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)

    # ---- METRICS DISPLAY ----
    st.subheader("📊 Centrality Metrics")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**In-Degree**", in_degree)
        st.write("**Out-Degree**", out_degree)

    with col2:
        st.write("**Betweenness**", betweenness)
        st.write("**Closeness**", closeness)

    # ---- INSIGHTS ----
    st.subheader("🧠 Insights")

    max_in = max(in_degree, key=in_degree.get)
    max_out = max(out_degree, key=out_degree.get)
    max_between = max(betweenness, key=betweenness.get)

    st.success(f"🏆 Most Referred Doctor (Hub): {max_in}")
    st.info(f"📤 Most Referring Doctor: {max_out}")
    st.warning(f"🔗 Bridge Doctor: {max_between}")

    if in_degree[max_in] >= len(G.nodes()) - 1:
        st.error("⚠️ Network Type: Highly Centralized (Overload risk)")
    else:
        st.success("✅ Network Type: Distributed (Balanced load)")

    # ---- GRAPH VISUALIZATION ----
    st.subheader("📈 Network Visualization")

    fig, ax = plt.subplots(figsize=(7, 5))
    pos = nx.spring_layout(G, seed=42)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2500,
        node_color="lightblue",
        font_size=10,
        arrows=True,
        ax=ax
    )

    st.pyplot(fig)

else:
    st.info("Add referrals from the sidebar to begin analysis.")