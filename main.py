import random

EVEN = "even"
ODD = "odd"

class Graph:
    def __init__(self, adj_list=None):
        self.adj_list = adj_list if adj_list else {}
    
    def get_neighbors(self, u):
        if u in self.adj_list:
            return self.adj_list[u]
        else:
            return []
    
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
    # stacks contain tuples with flags
    s1 = [(root, False)]
    s2 = []
    u = root
    examined_edges = set()
    # set to false if no augmenting path found
    path_exists = True
    # built out when augmenting path is found
    backtrace = []
    print("root is " + str(root))

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
            # if p0[y] is not a tuple
            if type(po[y]) != tuple:
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

    # the backtrace
    def build_aug_path(v, u):
        backtrace.append(v)
        parity = EVEN
        curr = u
        while curr != root:
            backtrace.append(curr)
            if parity == ODD:
                old = curr
                curr = po[curr]
                parity = EVEN

                # check if curr is tuple start*(mid), if so do a backtrace of blossom
                if type(curr) == tuple:
                    (start, mid) = curr
                    curr = mid
                    trace = [start]
                    blossomParity = ODD if pe[start] == mid else EVEN
                    # where the rest of the backtrace should continue
                    res = po[start] if pe[start] == mid else pe[start]
                    while curr != old:
                        trace.append(curr)
                        if blossomParity == ODD:
                            curr = po[curr]
                            blossomParity = EVEN
                        else:
                            curr = pe[curr]
                            blossomParity = ODD
                    trace = list(reversed(trace))
                    for x in trace:
                        backtrace.append(x)
                    if start == root:
                        # backtrace is finished
                        return
                    curr = res

            else:
                curr = pe[curr]
                parity = ODD
        backtrace.append(root)


    # 3.
    def examine_edge(e, i):
        # check if we've found a path
        (u, v) = e
        examined_edges.add((u,v))
        examined_edges.add((v,u))
        if v != root and v not in matched:
            # we've found an aug path
            build_aug_path(v, u)
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
            s1.append((v, False))
            mv = matched_dict[v]
            pe[mv] = v
            i += 1
            num[mv] = i
            po[mv] = -1
            s1.append((mv, False))
            u = mv
            examined_edges.add((mv,v))
            examined_edges.add((v,mv))
            print("traversing edge " + str((v,mv)))
            expand_subgraph(u, i)

    # 1. check if there is an unexamined edge
    def expand_subgraph(u, i):
        (u, flagU) = s1[-1]
        e = get_rand_unexamined(u)
        print("traversing edge " + str(e))
        if e == None:
            # 2. if u has marker, delete u from both stacks and go to 8
            #    otherwise, del top 2 of S1 and go to 1
            if flagU:
                s1.pop()
                s2.pop()
                handle_empty(i)
            else:
                s1.pop()
                if (len(s1) < 2):
                    path_exists = False
                    return
                s1.pop()
                expand_subgraph(u, i)
        else:
            examine_edge(e, i)

    expand_subgraph(u, i)

    if not path_exists or len(backtrace) == 0:
        return "no augmenting path"
    else:
        return list(reversed(backtrace))


adj_list = {
    1: [2, 3],
    2: [1, 3, 5],
    3: [1, 2, 4],
    4: [3, 5, 6],
    5: [2, 4],
    6: [4]
}

g = Graph(adj_list)
matching = [(2,3), (4,5)]
print(find_aug_path(g, matching))
