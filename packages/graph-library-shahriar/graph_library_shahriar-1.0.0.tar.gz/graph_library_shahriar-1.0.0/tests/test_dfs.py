from graph_library.dfs import * 

def test_dfs():
    n = 6  

    adj = [[] for _ in range(n)]

    add_edge_dfs(adj, 0, 1)
    add_edge_dfs(adj, 0, 2)
    add_edge_dfs(adj, 1, 3)
    add_edge_dfs(adj, 1, 4)
    add_edge_dfs(adj, 2, 5)

    print("Testing DFS Traversal:")
    print("Expected Output: 0 1 3 4 2 5 (or any valid DFS order)")
    print("Actual Output: ", end="")
    dfs(adj, 0)  
    print("\nTest Complete!")


test_dfs()