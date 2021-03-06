from data import Document
from typing import List, Set
import time


def get_subprofiles(I_u: List[Document]) -> List[Set[int]]:
    ts = time.time()
    subprofiles = {}
    to_be_pruned = {}
    I_u_item_id_set = set([item.id for item in I_u])

    for item in I_u:
        to_be_pruned[item.id] = False

        for _id in item.knn:
            if _id not in I_u_item_id_set:
                continue

            if _id in subprofiles:
                subprofiles[_id].add(item.id)
            else:
                subprofiles[_id] = {item.id, _id}

    subprofiles = list(subprofiles.values())
    subprofiles.sort(key=lambda S: len(S))

    # prune
    # for i in range(len(I_u)):
    #     doc_i = I_u[i]
    #     sub_i = subprofiles[doc_i.id]
    #
    #     for j in range(i + 1, len(I_u)):
    #         doc_j = I_u[j]
    #         sub_j = subprofiles[doc_j.id]
    #
    #         if to_be_pruned[doc_i.id] and to_be_pruned[doc_j.id]:
    #             continue
    #
    #         inters = sub_j.intersection(sub_i)
    #
    #         if len(inters) >= len(sub_j):
    #             to_be_pruned[doc_j.id] = True
    #         elif len(inters) >= len(sub_i):
    #             to_be_pruned[doc_i.id] = True

    # return [subprofiles[_id] for _id in subprofiles.keys() if not to_be_pruned[_id]]

    for i in range(len(subprofiles)):
        for j in range(i + 1, len(subprofiles)):
            if subprofiles[i].issubset(subprofiles[j]):
                subprofiles[i] = None
                break

    print("get subprofile used ", (time.time() - ts) * 1000, "ms")
    return [S for S in subprofiles if S is not None]


