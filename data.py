import random
import numpy as np


class Document:
    def __init__(self, id: int, attributes: list, rel_score: float, knn=[]):
        self.id = id
        self.attributes = attributes
        self.rel_score = rel_score
        self.knn = knn

    def update_knn(self, knn):
        self.knn = knn


def jaccard_similarity(a: Document, b: Document):
    a_set = set(a.attributes)
    b_set = set(b.attributes)
    inter_set = a_set.intersection(b_set)

    return len(inter_set) / (len(a_set) + len(b_set) - len(inter_set))


def get_fake_candidates():
    """
    generate 100 documents with less than 5 attributes each, and attributes are integer ids in range [0, 20]
    relevant score for each document is generated randomly in range [0, 1)
    knn's are calculated by jaccard sim with attributes
    :return:
    """
    docs = []
    for i in range(100):
        id = i
        attr = []
        for j in range(5):
            rand_attr = random.randint(0, 40)
            if rand_attr <= 20:
                attr.append(rand_attr)

        rel_score = random.random()

        docs.append(Document(id, attr, rel_score))

    sim_mat = np.ones((100, 100))
    for i in range(100):
        for j in range(100):
            if i == j:
                continue
            if i > j:
                sim_mat[i, j] = sim_mat[j, i]
            else:
                sim_mat[i, j] = jaccard_similarity(docs[i], docs[j])

    for i in range(100):
        knn = np.argsort(sim_mat)[:6].tolist()
        knn = list(filter(lambda: id != i, knn))
        docs[i].update_knn(knn[:5])

    return docs