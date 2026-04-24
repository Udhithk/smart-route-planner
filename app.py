import streamlit as st
from smart_route_planner import Graph, dijkstra, a_star, apply_traffic
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Smart Route Planner", layout="wide")

# -------------------------------
# Init Graph (SESSION)
# -------------------------------
if "graph" not in st.session_state:
    g = Graph()
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "C", 5)
    g.add_edge("B", "D", 10)
    g.add_edge("C", "E", 3)
    g.add_edge("E", "D", 4)
    g.add_edge("D", "F", 11)
    st.session_state.graph = g

g = st.session_state.graph

# Track traffic edges
if "traffic_edges" not in st.session_state:
    st.session_state.traffic_edges = set()

# -------------------------------
# Coordinates (for A*)
# -------------------------------
coordinates = {
    "A": (0, 0),
    "B": (2, 2),
    "C": (1, 1),
    "D": (5, 3),
    "E": (3, 2),
    "F": (6, 4)
}

# -------------------------------
# Graph Visualization
# -------------------------------
def draw_graph(graph, path=None):
    G = nx.Graph()

    for node in graph.graph:
        for neighbor, weight in graph.graph[node]:
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(12, 7))

    # Node colors
    node_colors = []
    for node in G.nodes():
        if path and node == path[0]:
            node_colors.append('green')   # Start
        elif path and node == path[-1]:
            node_colors.append('red')     # End
        else:
            node_colors.append('lightblue')

    nx.draw(G, pos,
            with_labels=True,
            node_size=2200,
            node_color=node_colors,
            font_weight='bold',
            ax=ax)

    # Edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    # 🔴 Traffic edges
    traffic_edges = st.session_state.get("traffic_edges", set())
    traffic_edge_list = [edge for edge in G.edges() if edge in traffic_edges]

    nx.draw_networkx_edges(
        G, pos,
        edgelist=traffic_edge_list,
        width=4,
        edge_color='red',
        ax=ax
    )

    # 🟢 Shortest path
    if path and len(path) > 1:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(
            G, pos,
            edgelist=path_edges,
            width=4,
            edge_color='green',
            ax=ax
        )

    return fig


# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("⚙️ Controls")

start = st.sidebar.selectbox("Start Node", list(g.graph.keys()))
end = st.sidebar.selectbox("End Node", list(g.graph.keys()))

algorithm = st.sidebar.radio("Algorithm", ["Dijkstra", "A*"])

st.sidebar.markdown("---")
st.sidebar.subheader("🚦 Traffic Simulation")

u = st.sidebar.selectbox("From", list(g.graph.keys()), key="u")
v = st.sidebar.selectbox("To", list(g.graph.keys()), key="v")

traffic_level = st.sidebar.selectbox(
    "Traffic Level",
    ["Low", "Medium", "High"]
)

st.sidebar.caption("Higher traffic increases edge cost")
st.sidebar.info("🚦 Low = Normal | Medium = Slow | High = Heavy Traffic")

# Apply traffic
if st.sidebar.button("Apply Traffic"):
    current_weight = None
    for neighbor, weight in g.graph[u]:
        if neighbor == v:
            current_weight = weight
            break

    if current_weight is not None:
        if traffic_level == "Low":
            new_weight = current_weight
        elif traffic_level == "Medium":
            new_weight = current_weight * 2
        else:
            new_weight = current_weight * 10  # strong effect

        apply_traffic(g, u, v, new_weight)
        st.session_state.graph = g

        # Track traffic edges
        st.session_state.traffic_edges.add((u, v))
        st.session_state.traffic_edges.add((v, u))

        st.sidebar.success(f"{traffic_level} traffic applied on {u} → {v}")
    else:
        st.sidebar.error("Invalid edge selected")

# Reset button
if st.sidebar.button("Reset Graph"):
    st.session_state.clear()
    st.rerun()

# -------------------------------
# Main UI
# -------------------------------
st.title("🚀 Smart Route Planner")
st.markdown("Find shortest paths using **Dijkstra** and **A\\*** algorithms")

# Demo Mode (quick showcase)
if st.button("🎬 Demo Mode"):
    apply_traffic(g, "C", "E", 50)
    st.session_state.traffic_edges.add(("C", "E"))
    st.session_state.traffic_edges.add(("E", "C"))
    st.success("Demo traffic applied on C → E")

# Validate input
if start == end:
    st.warning("Start and End cannot be the same")

# -------------------------------
# Find Route
# -------------------------------
if st.button("🔍 Find Route") and start != end:
    if algorithm == "Dijkstra":
        path, dist = dijkstra(g, start, end)
    else:
        path, dist = a_star(g, start, end, coordinates)

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("📍 Path Length", len(path))
    col2.metric("📏 Distance", dist)
    col3.metric("⚡ Algorithm", algorithm)

    st.markdown("### 🗺️ Route Visualization")
    fig = draw_graph(g, path)
    st.pyplot(fig)

    # Legend
    st.markdown("""
    ### 🚦 Legend
    - 🟢 Shortest Path  
    - 🔴 Traffic Edge  
    - 🔵 Normal Nodes  
    """)

    # Graph info
    st.markdown("### 📊 Graph Info")
    st.write(f"Nodes: {len(g.graph)}")
    st.write(f"Edges: {sum(len(v) for v in g.graph.values()) // 2}")

    # Explanation
    st.markdown("### 🧠 How it works")
    st.write("""
    - Algorithm explores nodes based on minimum distance  
    - Updates shortest path dynamically  
    - Avoids high-cost (traffic) edges  
    """)

else:
    st.info("Select nodes and click **Find Route** to visualize.")