# 🌍 Smart Route Planner (Multi-Page App)

A professional, interactive route planning web app that demonstrates both **graph-based shortest path algorithms** and **real-world map routing**.

Built using **Streamlit, NetworkX, OSMnx, and Folium**, this project showcases how classical algorithms like **Dijkstra** and **A*** work in both simulated and real environments.

---

## 🚀 Live Demo

👉 https://smart-route-planner-udhith.streamlit.app/

---

## ✨ Features

### 📊 1. Basic Graph Planner

* Visual representation of a custom graph
* Implements:

  * Dijkstra Algorithm
  * A* Algorithm
* Displays:

  * Shortest path
  * Distance
* Traffic simulation (edge weight updates)

---

### 🗺️ 2. Real Map Route Planner

* Uses **OpenStreetMap data**
* Finds real-world routes between locations
* Interactive map visualization
* Compares:

  * Dijkstra vs A* performance
* Shows:

  * Distance (km)
  * Execution time (seconds)

---

## 🧠 Key Concepts

* Graph Theory
* Shortest Path Algorithms
* Heuristic Search (A*)
* Real-world network modeling
* Performance optimization using caching

---

## ⚡ Performance Optimizations

* Fast Mode (smaller map area)
* Graph caching using Streamlit
* Reduced API calls
* Efficient nearest-node lookup

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **Graph Algorithms:** NetworkX
* **Map Data:** OSMnx (OpenStreetMap)
* **Visualization:** Folium
* **Language:** Python

---

## 📁 Project Structure

```
smart-route-planner/
│
├── app.py                     # Main entry (multi-page navigation)
├── pages/
│   ├── 1_Basic_Graph.py
│   └── 2_Real_Map.py
│
├── smart_route_planner.py     # Core algorithms
├── requirements.txt
├── .gitignore
```

---

## ⚙️ Installation (Run Locally)

```bash
git clone https://github.com/Udhithk/smart-route-planner.git
cd smart-route-planner

pip install -r requirements.txt

streamlit run app.py
```

---

## 📦 Requirements

```
streamlit
networkx
matplotlib
osmnx
folium
scikit-learn
```

---

## 📸 Screenshots

> Add screenshots of:
>
> * Basic Graph Output
> * Real Map Routing
> * Comparison Results

---

## ⚠️ Known Issues

* First load may take time (OSM data fetch)
* Some locations may fail due to API limits
* Internet connection required

---

## 📈 Future Enhancements

* 🚦 Real-time traffic integration
* 📱 Mobile-friendly UI
* 🧭 Turn-by-turn directions
* 🗺️ Multiple route suggestions
* 📍 User location detection

---

## 👨‍💻 Author

**Udhith K**

* GitHub: https://github.com/Udhithk

---

## ⭐ Support

If you found this useful, consider giving it a ⭐ on GitHub!

---


