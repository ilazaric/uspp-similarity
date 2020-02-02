import numpy as np

with open("words", 'rb') as wordsFile:
    wordList = [l.decode('utf8', 'ignore') for l in wordsFile.readlines()]
wordList = [word[0:-1] for word in wordList]

with open("edges", "r") as edgesFile:
    edgeList = [tuple(map(int, line.split())) for line in edgesFile.readlines()]

maximumFrequency = 800

frequencies = [0]*len(wordList)
for (u, v) in edgeList:
    frequencies[v-1] += 1
unwantedWordsIndices = {index for index in range(len(wordList))
                        if frequencies[index] >= maximumFrequency}
# unwantedWords = [wordList[i] for i in unwantedWordsIndices]

query = input("Find synonims for word: ")
try:
    queryNum = wordList.index(query, 0) + 1
except:
    print("Word " + query + " does not appear in the dictionary.")
    exit()


def makeNeighboursGraph(index):
    nodesPointedBy = []
    nodesPointingTo = []
    for (a, b) in edgeList:
        if a == index and (b-1) not in unwantedWordsIndices:
            nodesPointedBy.append(b)
        if b == index and (a-1) not in unwantedWordsIndices:
            nodesPointingTo.append(a)
    nodes = list(set(nodesPointedBy + nodesPointingTo))
    graph = np.zeros((len(nodes), len(nodes)))
    for (a, b) in edgeList:
        if a in nodes and b in nodes:
            graph[nodes.index(a, 0), nodes.index(b, 0)] = 1
    return nodes, graph


(neighbours, neighboursGraph) = makeNeighboursGraph(queryNum)
# print([wordList[index-1] for index in neighbours])

def graphFromEdges(listOfEdges, size):
    graph = np.zeros((size, size))
    for (i, j) in listOfEdges:
        graph[i, j] = 1
    return graph


def SimilarityWith123(graph, num_steps=10000):
    A = graphFromEdges([(0, 1), (1, 2)], 3)
    z = np.ones(((graph.shape)[0], 3))
    for i in range(num_steps):
        for j in range(2):
            z = (graph @ z @ A.T) + (graph.T @ z @ A)
            z = z / np.linalg.norm(z)
    return z[:, [1]].flatten()


def centralScore(graph):
    matrix = graph @ graph.T + graph.T @ graph
    z = np.ones(((graph.shape)[0], 1))
    for i in range(10000):
        z = matrix @ z
        z = z / np.linalg.norm(z)
    return z.flatten()


similarity = centralScore(neighboursGraph)

topN = 10
best = np.argpartition(similarity, -topN)[-topN:]
sortedBest = np.flip(best[np.argsort(similarity[best])])
print(similarity[sortedBest])

synonims = [wordList[neighbours[index]-1] for index in sortedBest]
print(synonims)


