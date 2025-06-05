class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        
    def find(self, i):
        if self.parent[i] == i:
            return i
        else:
            self.parent[i] = self.find(self.parent[i])
            return self.parent[i]
        
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i != root_j:
            if self.size[root_i] > self.size[root_j]:
                root_i, root_j = root_j, root_i
                
            self.parent[root_i] = root_j
            self.size[root_j] += self.size[root_i]
            return True
        else:
            return False