import heapq
import copy

class LinkMap:
    link_list = {}
    def __init__(self, link_path = "../data/maps/links_new_format.txt", weight_path = "../data/maps/link_weights.txt"):
        self.link_list = {}
        num_lines = 0
        with open(weight_path, "r") as f:
            for line in f:
                num_lines += 1
                if num_lines > 1:
                    arr = line.split(',')
                    self.addWeight(arr[0], arr[1], int(arr[2]))
                    self.addWeight(arr[1], arr[0], int(arr[2]))
                

        num_lines = 0
        with open(link_path, "r" ) as f:
            for line in f:
                num_lines += 1
                if num_lines > 2:
                    arr = line.split(',')
                    self.addLink(arr[0], arr[2], float(arr[4]), float(arr[5].strip()))
                    self.addLink(arr[2], arr[0], float(arr[4]), float(arr[5].strip()))

    def __del__(self):
        del self.link_list

    def addLink(self, router1, router2, time_create, time_destroy):
        val = (time_create, time_destroy)
        if router1 in self.link_list:
            if router2 in self.link_list[router1]:
                if 'time' in self.link_list[router1][router2]:
                    self.link_list[router1][router2]['time'].append(val)
                else:
                    self.link_list[router1][router2]['time'] = [val]
            else:
                self.link_list[router1][router2] = {'weight': 0, 'time': [val]}
        else:
            self.link_list[router1] = {router2: {'weight': 0, 'time': [val]}}

    def addWeight(self, router1, router2, weight):
        if "" == router1 or "" == router2:
            pass
        elif router1 in self.link_list:
            if router2 in self.link_list[router1]:
                self.link_list[router1][router2]['weight'] = weight
            else:
                self.link_list[router1][router2] = {'weight': weight, 'time': []}
        else:
            self.link_list[router1] = {router2: {'weight': weight, 'time': []}}

    def hasLink1(self, router1, router2, timestamp):
        if router1 in self.link_list and router2 in self.link_list[router1] and 'time' in self.link_list[router1][router2]:
            timerange_list = self.link_list[router1][router2]['time']
            for timerange in timerange_list:
                if timestamp > timerange[0] and timestamp < timerange[1]:
                    return True
        if router2 in self.link_list and router1 in self.link_list[router2] and 'time' in self.link_list[router2][router1]:
            timerange_list = self.link_list[router2][router1]['time']
            for timerange in timerange_list:
                if timestamp > timerange[0] and timestamp < timerange[1]:
                    return True
        return False

    def hasLink2(self, router1, router2, time_start, time_end):
        if router1 in self.link_list and router2 in self.link_list[router1] and 'time' in self.link_list[router1][router2]:
            timerange_list = self.link_list[router1][router2]
            for timerange in timerange_list:
                if time_start > timerange[0] and time_end < timerange[1]:
                    return True
        if router2 in self.link_list and router1 in self.link_list[router2] and 'time' in self.link_list[router2][router1]:
            timerange_list = self.link_list[router2][router1]
            for timerange in timerange_list:
                if time_start > timerange[0] and time_end < timerange[1]:
                    return True
        return False

    def getLinks(self, router, timestamp):
        temp_link_list = {}
        if router in self.link_list:
            for item in self.link_list[router]:
                if not item in temp_link_list:
                    temp_link_list[item] = {'time': [], 'weight': 0}
                if 'weight' in self.link_list[router][item]:
                    temp_link_list[item]['weight'] = self.link_list[router][item]['weight']
                if 'time' in self.link_list[router][item]:
                    for timerange in self.link_list[router][item]['time']:
                        if timestamp > timerange[0] and timestamp < timerange[1]:
                            temp_link_list[item]['time'].append(timerange)
        return temp_link_list

    def getLinks2(self, router):
        if router in self.link_list:
            return self.link_list[router]

    def getWeight(self, router1, router2):
        if router1 in self.link_list and router2 in self.link_list[router1] and 'weight' in self.link_list[router1][router2]:
            return self.link_list[router1][router2]['weight']
        else:
            return 0

    def getShortestPath(self, source, dest):
        shortest_path = {source: float('-inf')}
        rest_nodes = {}
        reachable = {}
        path = {source: [source]}
        for router in self.link_list:
            rest_nodes[router] = 0
        del rest_nodes[source]
        for router in self.link_list[source]:
            reachable[router] = self.link_list[source][router]['weight']
            path[router] = [source, router]
            del rest_nodes[router]
        
        while len(reachable) > 0:
            node = min(reachable, key = lambda x : reachable[x])
            length = reachable[node]
            del reachable[node]
            if node == dest:
                return path[dest], length
            shortest_path[node] = length
            for router in self.link_list[node]:
                if router in shortest_path:
                    continue
                elif router in reachable:
                    if length + self.link_list[node][router]['weight'] < reachable[router]:
                        reachable[router] = length + self.link_list[node][router]['weight']
                        path[router] = copy.deepcopy(path[node])
                        path[router].append(router)
                else:
                    del rest_nodes[router]
                    reachable[router] = length + self.link_list[node][router]['weight']
                    path[router] = copy.deepcopy(path[node])
                    path[router].append(router)
        if dest in shortest_path:
            return path[dest], shortest_path[dest]
        else:
            return None
            

p = LinkMap()
##for r1 in p.link_list:
##    for r2 in p.link_list[r1]:
##        if len(p.link_list[r1][r2]['time']) == 0:
##            print 'timerange = 0', r1, r2
##        elif p.link_list[r1][r2]['weight'] == 0:
##            print 'weight = 0', r1, r2
print p.getShortestPath('lax-core2', 'cj-usd-ASR9001')
