# 🌐 Graphs in Coding Interviews

Graphs are versatile data structures that represent **connections** or **relationships** between entities. In coding problems, they are often represented using **nodes (vertices)** and **edges (connections)**.

---

## 🛠️ Graph Representation: Adjacency List

An **adjacency list** is the most common and efficient way to represent graphs in programming interviews.

### ✍️ How to Construct (Undirected Graph)

```java
Map<Integer, List<Integer>> graph = new HashMap<>();

for (int[] edge : edges) {
    int u = edge[0], v = edge[1];
    graph.computeIfAbsent(u, x -> new ArrayList<>()).add(v);
    graph.computeIfAbsent(v, x -> new ArrayList<>()).add(u); // For undirected
}
```
### ✍️ How to Construct (Directed Graph)

```java
Map<Integer, List<Integer>> graph = new HashMap<>();
for (int[] edge : edges) {
    int u = edge[0], v = edge[1];
    graph.computeIfAbsent(u, x -> new ArrayList<>()).add(v);
    // No need to add the reverse edge for directed graphs
}
```
## 🔍 BFS vs DFS

| Strategy | Data Structure     | Traversal Order     | Common Use Cases                                    |
|----------|--------------------|----------------------|-----------------------------------------------------|
| **DFS**  | Stack (or Recursion) | Deep before wide     | Pathfinding, Topological Sort, Connected Components |
| **BFS**  | Queue               | Wide before deep     | Shortest Path, Level Order, Minimum Steps           |

# When to Use DFS vs BFS

| Use Case                     | Use                          |
|------------------------------|------------------------------|
| Shortest Path (unweighted)   | BFS                          |
| Topological Sort             | DFS                          |
| Detect Cycle in Undirected Graph | DFS                      |
| Level Order Traversal        | BFS                          |
| Flood Fill / Island Counting | DFS or BFS                   |
| Finding Path Exists          | DFS (faster for early exits) |
| Minimum Steps / Moves        | BFS                          |
## 🧠 Key Takeaways
- **BFS** is ideal for finding the shortest path in unweighted graphs.
- **DFS** is useful for exploring all paths, detecting cycles, and topological sorting.
- Both algorithms can be implemented using recursion or iterative methods with stacks/queues.

## Graph Traversal Tips
- Always keep track of **visited** nodes to avoid infinite loops.
- Use recursion stack or iterative stack carefully in DFS to manage backtracking.
- BFS naturally gives shortest paths in unweighted graphs, making it ideal for distance or level problems.

## Common Graph Problem Categories
- **Connectivity:** Number of connected components, checking if a graph is connected
- **Path Finding:** Shortest path, existence of path
- **Cycle Problems:** Detecting cycles, finding strongly connected components
- **Graph Coloring:** Bipartite checking, scheduling problems
- **Network Flow:** Max flow, min cut problems (advanced)

---

## Practice Suggestions

- Implement graph construction from edge list input.
- Practice both recursive and iterative DFS.
- Solve BFS shortest path problems.
- Explore problems involving cycle detection and topological sort.

---

**Tip:** Choose adjacency list for most problems unless graph is dense or edge lookup speed is critical.

