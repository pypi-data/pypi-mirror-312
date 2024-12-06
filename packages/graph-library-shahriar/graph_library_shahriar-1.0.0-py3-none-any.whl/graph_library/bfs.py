from collections import deque


def add_edge(adj, u, v):
    adj[u].append(v)
    adj[v].append(u)


def bfs(adj, s):
    q = deque()
    visited = [False] * len(adj)
    visited[s] = True
    q.append(s)
    
    visited_node = []
    
    while q:
        current = q.popleft()
        visited_node.append(current)
        
        for i in adj[current]:
            if not visited[i]:
                visited[i] = True
                q.append(i)
                
    return visited_node


# def main():
#     V = int(input("Please enter the number of vertices: "))
    
#     adj = [[] for _ in range(V)]
    
#     E = int(input("Please enter the number of edges: "))
    
#     for _ in range(E):
#         u, v = map(int, input("Enter an edge (u v): ").split())
#         add_edge(adj, u, v)
        
#     start = int(input("Please enter the starting vertex: "))
    
#     print("BFS starting from vertex", start, ":")
    
#     result = bfs(adj, start)
#     print("Visited nodes in BFS order:", result)


# if __name__ == '__main__':
#     main()