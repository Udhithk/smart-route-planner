import streamlit as st
import osmnx as ox
import networkx as nx
import folium
from streamlit.components.v1 import html
from math import radians, cos, sin, asin, sqrt
import time

st.set_page_config(page_title="Smart Route Planner", layout="wide")

st.title("🌍 Smart Route Planner (Optimized)")
st.markdown("Compare **Dijkstra vs A*** with high performance 🚀")

col1, col2 = st.columns(2)

with col1:
    start_location = st.text_input("Start Location", "Indiranagar metro station")

with col2:
    end_location = st.text_input("End Location", "Domlur")

fast_mode = st.checkbox("⚡ Fast Mode (smaller map area)", value=True)

# -------- HEURISTIC --------
def heuristic(u, v, G):
    lat1, lon1 = G.nodes[u]['y'], G.nodes[u]['x']
    lat2, lon2 = G.nodes[v]['y'], G.nodes[v]['x']

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    return 6371000 * c

# -------- CACHE --------
@st.cache_data
def get_location(place):
    return ox.geocode(place)

@st.cache_resource
def load_graph(lat, lon, dist):
    G = ox.graph_from_point((lat, lon), dist=dist, network_type="drive")

    for u, v, data in G.edges(data=True):
        data["weight"] = data.get("length", 1)

    return G

# -------- NO CACHE HERE --------
def compute_routes(G, start_node, end_node):
    t1 = time.time()
    route_dijkstra = nx.shortest_path(G, start_node, end_node, weight="weight")
    t2 = time.time()

    t3 = time.time()
    route_astar = nx.astar_path(
        G,
        start_node,
        end_node,
        heuristic=lambda u, v: heuristic(u, v, G),
        weight="weight"
    )
    t4 = time.time()

    dist_dijkstra = nx.shortest_path_length(G, start_node, end_node, weight="weight")
    dist_astar = nx.shortest_path_length(G, start_node, end_node, weight="weight")

    return route_dijkstra, route_astar, dist_dijkstra, dist_astar, (t2 - t1), (t4 - t3)

# -------- MAIN --------
if st.button("🚀 Find Route"):

    try:
        st.info("First load may take a few seconds. Subsequent runs are faster ⚡")

        with st.spinner("📍 Getting locations..."):
            start_point = get_location(start_location)
            end_point = get_location(end_location)

        dist = 2000 if fast_mode else 5000

        with st.spinner("🗺 Loading map..."):
            G = load_graph(start_point[0], start_point[1], dist)

        st.success(f"Graph loaded with {len(G.nodes)} nodes")

        with st.spinner("🔍 Finding nodes..."):
            start_node = ox.distance.nearest_nodes(G, start_point[1], start_point[0])
            end_node = ox.distance.nearest_nodes(G, end_point[1], end_point[0])

        with st.spinner("🧠 Computing routes..."):
            route_dijkstra, route_astar, dist_d, dist_a, time_d, time_a = compute_routes(
                G, start_node, end_node
            )

        st.markdown("## 📊 Results")

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Dijkstra")
            st.metric("Distance (km)", f"{dist_d/1000:.2f}")
            st.metric("Time (sec)", f"{time_d:.6f}")

        with c2:
            st.subheader("A*")
            st.metric("Distance (km)", f"{dist_a/1000:.2f}")
            st.metric("Time (sec)", f"{time_a:.6f}")

        st.markdown("## 🗺 Map")

        m = folium.Map(
            location=[G.nodes[start_node]['y'], G.nodes[start_node]['x']],
            zoom_start=14
        )

        def draw(route, color):
            coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]
            folium.PolyLine(coords, color=color, weight=5).add_to(m)

        draw(route_dijkstra, "blue")
        draw(route_astar, "green")

        folium.Marker(
            [G.nodes[start_node]['y'], G.nodes[start_node]['x']],
            tooltip="Start"
        ).add_to(m)

        folium.Marker(
            [G.nodes[end_node]['y'], G.nodes[end_node]['x']],
            tooltip="End"
        ).add_to(m)

        html(m._repr_html_(), height=600)

    except Exception as e:
        st.error(f"Error: {e}")
        st.warning("Try simpler location names like 'MG Road Bangalore'")