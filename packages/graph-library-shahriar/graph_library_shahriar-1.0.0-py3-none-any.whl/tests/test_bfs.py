from graph_library.bfs import bfs, add_edge

def test_bfs():
    V = 5  
    edges = [(0, 1), (0, 2), (1, 3), (1, 4)] 
    start_vertex = 0  

    adj = [[] for _ in range(V)]
    for u, v in edges:
        add_edge(adj, u, v)

    result = bfs(adj, start_vertex)
    expected = [0, 1, 2, 3, 4]  

    print("BFS Result:", result)
    assert result == expected, f"Test failed! Expected {expected}, got {result}"
    print("Test passed!")


print("Running BFS test...")
test_bfs()