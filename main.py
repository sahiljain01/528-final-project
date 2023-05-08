import random

class Graph:
    def __init__(self, adj_list=None):
        self.adj_list = adj_list if adj_list else {}
    
    def add_edge(self, u, v):
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)
    
    def remove_edge(self, u, v):
        if u in self.adj_list and v in self.adj_list[u]:
            self.adj_list[u].remove(v)
            self.adj_list[v].remove(u)
    
    def get_neighbors(self, u):
        if u in self.adj_list:
            return self.adj_list[u]
        else:
            return []
    
    def has_edge(self, u, v):
        return u in self.adj_list and v in self.adj_list[u]
    
    def get_vertices(self):
        return list(self.adj_list.keys())



def find_aug_path(g, matching, root=-1):
    
    # 0. find an unmatched node, and set it as the root
    matched = set()
    matched_dict = {}
    for (x,y) in matching:
        matched.add(x)
        matched.add(y)
        matched_dict[x] = y
        matched_dict[y] = x

    if root == -1:
        # get a set of the vertices
        verts = set(g.get_vertices())

        # set difference
        unmatched = verts - matched

        # pick random root from unmatched using rand
        root = random.choice(list(unmatched))

    po = {}
    pe = {}
    num = {}
    i = 0
    num[root] = i
    po[root] = -1
    pe[root] = root
    s1 = [(i, False)]
    s2 = []
    u = root
    examined_edges = set()
    path_exists = True
    backtrace = []

    def get_rand_unexamined(n):
        edges = g.get_neighbors(n)
        edges = [(n, x) for x in edges]
        unexamined = set(edges) - examined_edges
        if len(unexamined) == 0:
            return None
        return random.choice(list(unexamined))


    # 8.
    def handle_empty(i):
        if len(s2) != 0:
            (u, flagU) = s2[-1]
            s1.append((u, True))
            expand_subgraph(u, i)
        elif len(s1) != 0:
            (u, flagU) = s1[-1]
            expand_subgraph(u, i)
        else:
            # we are done! this matching is good
            path_exists = False
            return



    # 6. 
    def handle_blossom(z, v, i):
        x = z
        if len(s1) < 2:
            # go to 8
            handle_empty(i)
            return
        (y, flagY) = s1[-1]
        (z, flagZ) = s1[-2]
        if num[y] <= num[v]:
            # go to 8
            handle_empty(i)
        elif not flagY:
            po[y] = x
            pe[z] = y
            s2.append(s1.pop())
            s2.append(s1.pop())
            # repeat 6
            handle_blossom(z, v, i)
        else:
            s1.pop()
            # 7. 
            if num[z] > num[v]:
                po[z] = (x, y)
                z = matched_dict[z]
                handle_blossom(z, v, i)
            else:
                # go to 8
                handle_empty(i)


    # 3.
    def examine_edge(e, i):
        # check if we've found a path
        (u, v) = e
        examined_edges.add((u,v))
        examined_edges.add((v,u))
        if v != root and v not in matched:
            # we've found an aug path
            # TODO: backtracing, look for tuples
            backtrace.append(v)
            parity = "odd"
            curr = u
            while curr != root:
                if parity == "odd":
                    curr = po[curr]
                    parity = "even"
                else:
                    curr = pe[curr]
                    parity = "odd"
                backtrace.append(curr)
            return
        elif v in num:
            # 5.
            if pe[v] == -1:
                expand_subgraph(u, i)
            else:
                # 5. blossom created
                z = v
                handle_blossom(z, v, i)
        else:
            # 4. 
            i += 1
            num[v] = i
            po[v] = u
            pe[v] = -1
            s1.append((i, False))
            mv = matched_dict[v]
            pe[mv] = v
            i += 1
            num[mv] = i
            po[mv] = -1
            s1.append((i, False))
            u = mv
            expand_subgraph(u, i)

    # 1. check if there is an unexamined edge
    def expand_subgraph(u, i):
        e = get_rand_unexamined(u)
        print(e)
        if e == None:
            # 2. if u has marker, delete u from both stacks and go to 8
            #    otherwise, del top 2 of S1 and go to 1
            oldU = u
            (u, flagU) = s1[-1]
            assert(u==oldU)
            if flagU:
                s1.pop()
                s2.pop()
                handle_empty(i)
            else:
                s1.pop()
                s1.pop()
                expand_subgraph(u, i)
        else:
            examine_edge(e, i)

    expand_subgraph(u, i)

    if not path_exists:
        return "no augmenting path"
    else:
        return list(reversed(backtrace))


    

adj_list = {
    1: [2, 3],
    2: [1, 3, 4],
    3: [1, 2],
    4: [2, 5],
    5: [4]
}


g = Graph(adj_list)
matching = [(1,2)]
print()
print(find_aug_path(g, matching))


