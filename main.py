# This is a sample Python script.
import math
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def colored_maze (color_map, graph,s, t):
    augmented_graph = create_color_graph(graph, s, t,color_map)
    return shortest_path_bfs(augmented_graph)


def create_color_graph(graph, s , t,color_map):
    augmented_graph = {}

    for u in graph:
        u_red = u + "_red"
        u_yellow = u + "_yellow"
        u_blue = u + "_blue"
        augmented_graph[u_red] = []
        augmented_graph[u_yellow] = []
        augmented_graph[u_blue] = []

    for color in color_map.keys:
        for edge in color_map[color]:
            if color == "red":
                u = edge[0]+"_blue"
                v = edge[1]+"_red"
                augmented_graph[v].append(u)
                augmented_graph[u].append(v)
            if color == "blue":
                u = edge[0] + "_yellow"
                v = edge[1] + "_blue"
                augmented_graph[v].append(u)
                augmented_graph[u].append(v)
            if color == "yellow":
                u = edge[0] + "_red"
                v = edge[1] + "_yellow"
                augmented_graph[v].append(u)
                augmented_graph[u].append(v)
    augmented_graph[s] = [s+"_blue"]
    augmented_graph[t] = [t+"_yellow"]
    return augmented_graph

def shortest_path_bfs(graph,s,t):
    queue = []
    visited = {}
    queue.append(s)
    visited.add(s)
    dist = {node: -math.inf for node in graph}
    i = 0
    dist[s] = 0
    while queue:
        node = queue.pop()
        dist[node] = i
        i = i + 1
        if node == t:
            return dist[t]
        for i in graph[node]:
            if i not in visited:
                queue.append(i)
                visited.add(i)
    return dist[t] - 2 # because of the 0 weight edges between s and s_col, and t  and t_col

def pick_your_courses(graph):
    sort = topological_sort(graph)
    length = longest_path(sort, graph)
    return length

def topological_sort(graph):
    visited = []
    for u in graph.keys():
        if u not in visited:
            top_sort_DFS(graph, u,visited)
    visited.reverse()
    return visited

def top_sort_DFS(graph, u,visited):
    visited.append(u)
    for v in graph[u]:
        if v not in visited:
            top_sort_DFS(v,graph, visited)

def longest_path(topsort, graph):
    dp = {node: 0 for node in graph}
    for u in topsort:
        for v in graph[u]:
            dp[v] = max(dp[v],dp[u]+1)
    return max(dp.values())

def new_roads(graph):
    visited = {}
    num_SCC = dfs(graph, visited)
    return num_SCC - 1

def dfs(graph, visited):
    i = 0
    for u in graph.keys():
        if u not in visited:
            i = i + 1
        dfs_search(graph, visited, u)
    return i

def dfs_search(graph, visited, node):
    if node not in visited:
        visited.add(node)
        for neighbor in graph[node]:
            dfs(graph,visited, neighbor)


def fix_it_up(graph):
    order = get_finish_times(graph)
    g_T = transpose(graph)
    components = scc(g_T, order)
    comp_graph = componnet_graph(graph, components)
    sink = sink_list(comp_graph)
    source = source_list(comp_graph)

    if len(sink) != 1 or len(source) != 1:
        return False

    if sink[0] not in graph[source[0]]:
        return False

    return second_path(source,sink,comp_graph)


def sink_list(graph):
    sinks = []
    for u in graph.keys():
        if not graph[u]:
            sink_list.apppend(u)
    return sinks

def source_list(graph):
    sources = []
    in_deg = [0]*len(graph)
    for u in graph.keys():
        for v in graph[u]:
            in_deg[v] += 1
    for i,u in enumerate(graph.keys()):
        if in_deg[i] == 0:
            sources.append(u)
    return sources

def second_path(s, t, graph):
    if t in graph[s]:
        graph[s].remove(t)

    queue = []
    visited = {}
    queue.append(s)
    visited.add(s)
    while queue:
        node = queue.pop()
        if node == t:
            return True
        for i in graph[node]:
            if i not in visited:
                queue.append(i)
                visited.add(i)
    return False

def componnet_graph(graph, components):
    component_graph = {}
    for i, component in enumerate(components):
        component_graph[i] = []

    scc_map = {}
    for u in graph.keys():
        scc_map[u] = None

    for i, component in enumerate(components):
        for u in component:
            scc_map[u] = i

    for u in graph.keys():
        for v in graph[u]:
            if scc_map[u] != scc_map[v]:
                component_graph[scc_map[u]].append(scc_map[v])

    return component_graph

def scc(graph, order):
    components = []
    visited = {}
    while order:
        node = order.pop()
        if node not in visited:
            component = []
            scc_util(graph, visited, node, component)
            components.append(component)
    return components

def scc_util(graph, visited, node ,component):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited, component)
    component.append(node)

def get_finish_times(graph):
    order = []
    visited = {}
    for u in graph.keys():
        if u not in visited:
            finish_times_util(graph, visited, u,order)
    return order
def finish_times_util(graph, visited, node ,order):
    if node not in visited:
        order.append(node)
        visited.add(node)
        for neighbor in graph[node]:
            finish_times_util(graph, visited, neighbor,order)
def transpose(graph):
    transpose = {}
    for i in graph.keys():
        transpose[i] = []
    for i in graph.keys():
        list = graph[i]
        for j in list:
            transpose[j].append(i)
    return transpose


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print()