import math
import heapq
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


class getGraph:
    def __init__(self, edge_file):
        self.edge_file = edge_file

    def get_connections(self):
        edge_list = []
        edges = defaultdict(list)

        with open(self.edge_file, "r") as e_file:
            edge_list = e_file.readlines()

        for edge in edge_list:
            from_, to_ = edge.split("\t")
            from_, to_ = int(from_), int(to_[:-1])
            edges[from_].append(to_)
        from itertools import islice
        return edges


class plotGraph:
    def __init__(self, edges, interval=5000):
        self.edges = edges
        self.interval = interval

    def get_KMaxRankNodes(self, number_of_nodes, rank_vector):
        heaped_ranks = [(rank, node) for (node, rank) in enumerate(rank_vector)]
        heapq._heapify_max(heaped_ranks)
        topK = [heapq._heappop_max(heaped_ranks) for _ in range(number_of_nodes)]

        return topK

    def get_edgesConnectedToTopK(self, rank_vector, topK, ranks):
        weighed_edges = defaultdict(list)

        for couple in topK:
            weighed_edges[(couple[1], couple[0])] = [
                (node, ranks[node]) for node in self.edges[couple[1]]
            ]

        return weighed_edges

    def get_EdgesToDrawWithRanks(self, drawing_list, ranks):
        edge_list = []
        to_draw_node_set = set()
        for (node, rank) in drawing_list:
            to_draw_node_set.add(node)
            for child in drawing_list[(node, rank)]:
                to_draw_node_set.add(child[0])
                edge_list.append((node, child[0]))

        nodes_to_draw = [(node, ranks[node]) for node in to_draw_node_set]
        return (edge_list, nodes_to_draw)

    def draw(self, edge_list, nodes_to_draw):
        Graph = nx.DiGraph()
        Graph.add_edges_from(sorted(edge_list))

        fig = plt.figure()
        timer = fig.canvas.new_timer(self.interval)
        timer.add_callback(plt.close)

        pos = nx.shell_layout(Graph)
        try:
            nx.draw_networkx_nodes(
                Graph,
                pos,
                cmap=plt.get_cmap("jet"),
                node_size=[node[1] * 10000 for node in nodes_to_draw],
            )
            nx.draw_networkx_labels(
                Graph, pos, labels={node[0]: node[0] for node in nodes_to_draw}
            )
            nx.draw_networkx_edges(Graph, pos, arrows=True)
            timer.start()
            plt.show()
        except:
            pass

    def plot(self, number_of_nodes, rank_vector):
        ranks = {node: rank for (node, rank) in enumerate(rank_vector)}
        topK = self.get_KMaxRankNodes(number_of_nodes, rank_vector)
        drawing_list = self.get_edgesConnectedToTopK(rank_vector, topK, ranks)
        (edge_list, nodes_to_draw) = self.get_EdgesToDrawWithRanks(drawing_list, ranks)
        self.draw(edge_list, nodes_to_draw)


class TrustRank:
    def __init__(self, beta, edges, epsilon, max_iterations, node_num, PageRank_vector):
        self.beta = beta
        self.edges = edges
        self.epsilon = epsilon
        self.node_num = node_num
        self.PageRank_vector = PageRank_vector
        self.MAX_ITERATIONS = max_iterations

    def get_trustedPages(self, node_number_threshold=100):
        if self.node_num < node_number_threshold:
            ratio = 0.2
        else:
            ratio = 0.0002
        trusted_set_size = int(math.ceil(self.node_num * ratio))

        heaped_ranks = [
            (rank, node) for (node, rank) in enumerate(self.PageRank_vector)
        ]
        heapq._heapify_max(heaped_ranks)
        trusted_pages = [
            heapq._heappop_max(heaped_ranks)[1] for _ in range(trusted_set_size)
        ]

        return trusted_pages

    def get_topicSpecificRank(self, teleport_set):
        diff = math.inf
        iterations = 0
        teleport_set_size = len(teleport_set)

        pg = plotGraph(self.edges, interval=3000)

        final_rank_vector = np.zeros(self.node_num)
        initial_rank_vector = np.fromiter(
            [
                1 / teleport_set_size if node in teleport_set else 0
                for node in range(self.node_num)
            ],
            dtype="float",
        )

        while iterations < self.MAX_ITERATIONS and diff > self.epsilon:
            new_rank_vector = np.zeros(self.node_num)
            for parent in self.edges:
                for child in self.edges[parent]:
                    new_rank_vector[child] += initial_rank_vector[parent] / len(
                        self.edges[parent]
                    )

            leaked_rank = (1 - sum(new_rank_vector)) / teleport_set_size
            leaked_rank_vector = np.array(
                [
                    leaked_rank if node in teleport_set else 0
                    for node in range(self.node_num)
                ]
            )

            final_rank_vector = new_rank_vector + leaked_rank_vector
            diff = sum(abs(final_rank_vector - initial_rank_vector))
            initial_rank_vector = final_rank_vector

            iterations += 1
            print("TrustRank iteration: " + str(iterations))
            pg.plot(8298, final_rank_vector)

        return final_rank_vector

    def trustRank(self):
        trusted_pages = self.get_trustedPages()
        final_rank_vector = self.get_topicSpecificRank(trusted_pages)
        return final_rank_vector


class PageRank:
    def __init__(self, beta, edges, epsilon, max_iterations, node_num):
        self.beta = beta
        self.edges = edges
        self.epsilon = epsilon
        self.node_num = node_num
        self.MAX_ITERATIONS = max_iterations

    def pageRank(self):
        final_rank_vector = np.zeros(self.node_num)
        initial_rank_vector = np.fromiter(
            [1 / self.node_num for _ in range(self.node_num)], dtype="float"
        )

        iterations = 0
        diff = math.inf

        while iterations < self.MAX_ITERATIONS and diff > self.epsilon:
            new_rank_vector = np.zeros(self.node_num)
            for parent in self.edges:
                for child in self.edges[parent]:
                    new_rank_vector[child] += initial_rank_vector[parent] / len(
                        self.edges[parent]
                    )

            leaked_rank = (1 - sum(new_rank_vector)) / self.node_num
            final_rank_vector = new_rank_vector + leaked_rank
            diff = sum(abs(final_rank_vector - initial_rank_vector))
            initial_rank_vector = final_rank_vector
            iterations += 1

        return final_rank_vector
 

node_num = 2394385
beta = 0.85
epsilon = 1e-6
max_iterations = 20

gg = getGraph("data.txt")
edges = gg.get_connections()

pr = PageRank(beta, edges, epsilon, max_iterations, node_num)
tr = TrustRank(beta, edges, epsilon, max_iterations, node_num, pr.pageRank())
TrustRank_vector = tr.trustRank()
print(TrustRank_vector, sum(TrustRank_vector))
