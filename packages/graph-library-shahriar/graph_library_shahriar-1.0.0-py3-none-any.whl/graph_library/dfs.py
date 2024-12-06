def add_edge_dfs(adj, u, v):
    adj[u].append(v)
    adj[v].append(u)


def dfs_util(node, visited, adj):
    visited[node] = True
    print(node, end=" ")

    for neighbor in adj[node]:
        if not visited[neighbor]:
            dfs_util(neighbor, visited, adj)

def dfs(adj, start_node):
    visited = [False] * len(adj)

    dfs_util(start_node, visited, adj)