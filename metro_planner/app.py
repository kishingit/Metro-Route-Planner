from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from ds.graph import MetroGraph, StationNode
from ds.linked_list import RouteLinkedList
from ds.stack_queue import SearchHistoryStack, BookingQueue
from ds.bst import StationBST
from ds.search_sort import linear_search_by_name, binary_search_by_id, merge_sort
import db

app = Flask(__name__)
app.secret_key = "metro_planner_secret_key_2026"

# Initialize Data Structures in Memory
metro_graph = MetroGraph()
station_bst = StationBST()
search_stack = SearchHistoryStack(capacity=20)
booking_queue = BookingQueue()

def reload_metro_network():
    """Reloads graph and BST from database/in-memory data source."""
    global metro_graph, station_bst
    metro_graph = MetroGraph()
    station_bst = StationBST()

    stations_data, connections_data = db.load_initial_data_from_db()

    for s in stations_data:
        st_obj = StationNode(
            station_id=int(s['id']),
            name=s['name'],
            line=s['line'],
            x=s.get('x_pos', 0),
            y=s.get('y_pos', 0)
        )
        metro_graph.add_station(st_obj)
        station_bst.insert(st_obj)

    for c in connections_data:
        metro_graph.add_edge(c['station_a'], c['station_b'], float(c['distance']), c['line'])

# Initial Load
reload_metro_network()

@app.route("/")
def index():
    """1. Home Page: Route Search Form + Vis Network Overview."""
    station_names = sorted(list(metro_graph.stations.keys()))
    
    # Format graph nodes and edges for vis-network graph visualization
    nodes = []
    for name, st in metro_graph.stations.items():
        color_map = {
            "Purple": "#9333ea",
            "Green": "#16a34a",
            "Yellow": "#eab308",
            "Interchange": "#ef4444"
        }
        nodes.append({
            "id": name,
            "label": name,
            "group": st.line,
            "color": color_map.get(st.line, "#3b82f6")
        })

    edges = []
    seen_edges = set()
    for u, edge_list in metro_graph.adj.items():
        for edge in edge_list:
            v = edge['node']
            pair = tuple(sorted([u, v]))
            if pair not in seen_edges:
                seen_edges.add(pair)
                line_colors = {
                    "Purple": "#a855f7",
                    "Green": "#22c55e",
                    "Yellow": "#facc15"
                }
                edges.append({
                    "from": u,
                    "to": v,
                    "label": f"{edge['dist']} km",
                    "color": {"color": line_colors.get(edge['line'], "#94a3b8")},
                    "width": 3
                })

    return render_template(
        "index.html",
        stations=station_names,
        graph_nodes=nodes,
        graph_edges=edges,
        total_stations=len(metro_graph.stations)
    )

@app.route("/find_route", methods=["POST"])
def find_route():
    """Processes route query (Dijkstra or BFS) and pushes to history stack."""
    source = request.form.get("source")
    destination = request.form.get("destination")
    algorithm = request.form.get("algorithm", "dijkstra")

    if not source or not destination:
        flash("Please select both source and destination stations.", "danger")
        return redirect(url_for("index"))

    if source == destination:
        flash("Source and Destination stations cannot be the same!", "warning")
        return redirect(url_for("index"))

    if algorithm == "bfs":
        path, distance, stops, interchanges = metro_graph.bfs(source, destination)
        algo_name = "BFS (Minimum Stops)"
    else:
        path, distance, stops, interchanges = metro_graph.dijkstra(source, destination)
        algo_name = "Dijkstra's (Shortest Distance)"

    if not path:
        flash("No route could be found between selected stations.", "danger")
        return redirect(url_for("index"))

    # Push query into Search History Stack (LIFO)
    search_stack.push(source, destination, algo_name, distance, stops)

    # Save to DB
    db.save_search_to_db(source, destination, algo_name, distance, stops)

    # Build Route Linked List
    rll = RouteLinkedList.from_path_and_graph(path, metro_graph)
    route_steps = rll.to_list()

    # Calculate estimated travel time (~2 mins per stop + distance time)
    est_time = round((stops * 2.5) + (distance * 1.5))

    return render_template(
        "result.html",
        source=source,
        destination=destination,
        algorithm=algo_name,
        path=path,
        distance=distance,
        stops=stops,
        interchanges=interchanges,
        est_time=est_time,
        route_steps=route_steps
    )

@app.route("/stations", methods=["GET", "POST"])
def stations():
    """3. Stations Page: List, Search (Linear / Binary BST), Sort (Merge Sort), Add & Delete."""
    search_query = request.args.get("q", "").strip()
    search_by_id_val = request.args.get("id_q", "").strip()
    sort_by = request.args.get("sort", "name")
    
    all_stations = list(metro_graph.stations.values())

    # Handle Search
    if search_query:
        # Linear Search by station name
        station_list = linear_search_by_name(all_stations, search_query)
        search_mode = f"Linear Search results for '{search_query}'"
    elif search_by_id_val and search_by_id_val.isdigit():
        target_id = int(search_by_id_val)
        # Binary Search Tree (BST) Lookup
        found_st = station_bst.search_by_id(target_id)
        station_list = [found_st] if found_st else []
        search_mode = f"BST / Binary Search result for Station ID: {target_id}"
    else:
        station_list = all_stations
        search_mode = None

    # Handle Sorting (Merge Sort)
    if sort_by == "id":
        station_list = merge_sort(station_list, key_func=lambda s: s.station_id)
    elif sort_by == "line":
        station_list = merge_sort(station_list, key_func=lambda s: s.line)
    else:
        station_list = merge_sort(station_list, key_func=lambda s: s.name)

    return render_template(
        "stations.html",
        stations=station_list,
        search_mode=search_mode,
        current_sort=sort_by
    )

@app.route("/add_station", methods=["POST"])
def add_station():
    """Adds a new station to memory graph, BST, and MySQL."""
    try:
        station_id = int(request.form.get("station_id"))
        name = request.form.get("name").strip()
        line = request.form.get("line")

        if not name or station_id <= 0:
            flash("Invalid Station ID or Name.", "danger")
            return redirect(url_for("stations"))

        if name in metro_graph.stations:
            flash("Station with this name already exists!", "danger")
            return redirect(url_for("stations"))

        # Add to memory data structures
        new_st = StationNode(station_id, name, line)
        metro_graph.add_station(new_st)
        station_bst.insert(new_st)

        # Add to DB
        db.add_station_to_db(station_id, name, line)

        flash(f"Station '{name}' (ID: {station_id}) successfully added!", "success")
    except ValueError:
        flash("Station ID must be an integer.", "danger")

    return redirect(url_for("stations"))

@app.route("/delete_station/<int:station_id>", methods=["POST"])
def delete_station(station_id):
    """Deletes a station from database and reloads network graph."""
    db.delete_station_from_db(station_id)
    reload_metro_network()
    flash(f"Station ID {station_id} removed successfully.", "info")
    return redirect(url_for("stations"))

@app.route("/history")
def history():
    """4. History Page: Shows recent searches from LIFO Stack."""
    recent_searches = search_stack.get_all_reversed()
    return render_template("history.html", history=recent_searches)

@app.route("/clear_history", methods=["POST"])
def clear_history():
    search_stack.clear()
    flash("Search history stack cleared.", "info")
    return redirect(url_for("history"))

@app.route("/traversal")
def traversal():
    """DFS Traversal view of the entire network."""
    start_node = request.args.get("start", "Majestic")
    if start_node not in metro_graph.stations:
        start_node = list(metro_graph.stations.keys())[0] if metro_graph.stations else "Majestic"
    
    dfs_order = metro_graph.dfs(start_node)
    return render_template("traversal.html", dfs_order=dfs_order, start_node=start_node, stations=sorted(list(metro_graph.stations.keys())))

if __name__ == "__main__":
    print("==========================================================")
    print(" Starting Metro Route Planner Flask Application...")
    print(" Access URL: http://127.0.0.1:5000")
    print("==========================================================")
    app.run(debug=True, port=5000)
