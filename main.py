import tkinter as tk
from tkinter import ttk, messagebox
import heapq

# ----------- Bus Network Graph with Indian City Names -----------

graph = {
    'Delhi': {'Jaipur': 280, 'Lucknow': 500, 'Chandigarh': 250},
    'Jaipur': {'Delhi': 280, 'Ahmedabad': 670, 'Mumbai': 1140},
    'Mumbai': {'Ahmedabad': 530, 'Bengaluru': 980, 'Hyderabad': 710},
    'Hyderabad': {'Mumbai': 710, 'Bengaluru': 570, 'Chennai': 630},
    'Bengaluru': {'Mumbai': 980, 'Hyderabad': 570, 'Chennai': 350, 'Kochi': 550},
    'Chennai': {'Hyderabad': 630, 'Bengaluru': 350, 'Kolkata': 1670},
    'Kolkata': {'Chennai': 1670, 'Lucknow': 980},
    'Lucknow': {'Delhi': 500, 'Kolkata': 980},
    'Ahmedabad': {'Jaipur': 670, 'Mumbai': 530},
    'Chandigarh': {'Delhi': 250},
    'Kochi': {'Bengaluru': 550}
}

# ----------- Dijkstra's Algorithm Function -----------

def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        (cost, node, path) = heapq.heappop(queue)

        if node in visited:
            continue
        visited.add(node)
        path = path + [node]

        if node == end:
            return (cost, path)

        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))

    return (float("inf"), [])

# ----------- GUI Window Setup -----------

root = tk.Tk()
root.title("🚌 India Bus Route Planner")
root.geometry("700x500")
root.configure(bg="#eef7ff")

# ----------- Style Configuration -----------

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Segoe UI', 12, 'bold'), foreground='white', background='#007acc')
style.map('TButton', background=[('active', '#005f99')])
style.configure('TLabel', background='#eef7ff', font=('Segoe UI', 12))
style.configure('TCombobox', font=('Segoe UI', 12), padding=5)

# ----------- Heading Label -----------

heading = tk.Label(root, text="🚌 Indian Bus Route Finder using Dijkstra's Algorithm",
                   font=('Segoe UI', 16, 'bold'), bg="#eef7ff", fg="#003366")
heading.pack(pady=20)

# ----------- Dropdowns for Source & Destination -----------

stations = sorted(graph.keys())

tk.Label(root, text="Select Source Station:", font=('Segoe UI', 12, 'bold'), bg="#eef7ff").pack(pady=5)
src_combo = ttk.Combobox(root, values=stations, state="readonly", width=35)
src_combo.pack(pady=5)

tk.Label(root, text="Select Destination Station:", font=('Segoe UI', 12, 'bold'), bg="#eef7ff").pack(pady=10)
dest_combo = ttk.Combobox(root, values=stations, state="readonly", width=35)
dest_combo.pack(pady=5)

# ----------- Output Label -----------

output_frame = tk.Frame(root, bg="#eef7ff")
output_frame.pack(pady=20)

output_label = tk.Label(output_frame, text="", font=('Segoe UI', 12), bg="#eef7ff",
                        wraplength=600, justify="center", fg="#003366")
output_label.pack()

# ----------- Function to Find Route -----------

def find_route():
    source = src_combo.get()
    destination = dest_combo.get()

    if not source or not destination:
        messagebox.showwarning("Selection Error", "Please select both source and destination stations.")
        return

    if source == destination:
        messagebox.showinfo("Same Station", "Source and destination are the same. Distance is 0 km.")
        return

    distance, path = dijkstra(graph, source, destination)

    if distance == float("inf"):
        output_label.config(text="❌ No route found between selected cities.")
    else:
        path_str = " ➝ ".join(path)
        output = f"✅ Shortest path from {source} to {destination}:\n\n🛣️  {path_str}\n\n🧭 Total Distance: {distance} km"
        output_label.config(text=output)

# ----------- Find Route Button -----------

find_btn = ttk.Button(root, text="Find Shortest Route", command=find_route)
find_btn.pack(pady=10)

# ----------- Footer -----------

footer = tk.Label(root, text="Created with ❤️ using Python + Tkinter", font=('Segoe UI', 10, 'italic'),
                  bg="#eef7ff", fg="#555")
footer.pack(side='bottom', pady=10)

# ----------- Run Application -----------

root.mainloop()
