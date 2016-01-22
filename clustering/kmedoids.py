# -*- coding: utf-8 -*-
from math import sqrt
import random

__author__ = 'goran'

# friends = {1: set([2, 3]), 2: set([3]), 3: set([1]), 4: set([5]), 5: set([4, 6]), 6: set([5])}
friends = {1: set([3]), 2: set([3]), 3: set([1, 2]), 4: set([1, 2]), 5: set([3])}

def jaccard_sim(set1, set2):
    return 1.0 * len(set1 & set2) / len(set1 | set2)


def paper_sim(set1, set2):
    return 1.0 * len(set1 & set2) / (sqrt(len(set1)) * sqrt(len(set2)))


def random_medoids(data, k=2):
    medoids = set()
    user_ids = data.keys()
    num_users = len(user_ids)

    while len(medoids) < k:
        new_medoid_idx = random.randint(0, num_users - 1)
        if new_medoid_idx not in medoids:
            medoids.add(user_ids[new_medoid_idx])

    return medoids


def init_clusters(data, k, sim=jaccard_sim):
    cluster_users = {}
    medoids = random_medoids(data,k)
    for clust in medoids:
        cluster_users[clust] = set([clust])
    user_clusters = {}

    for user in data:
        best_sim = -1
        best_medoid = -1
        for medoid in medoids:
            similarity = sim(data[medoid], data[user])
            if similarity > best_sim:
                best_sim = similarity
                best_medoid = medoid
        user_clusters[user] = best_medoid
        cluster_users[best_medoid].add(user)
    return cluster_users, user_clusters


def within_sim(data, medoid, users, sim=jaccard_sim):
    return sum([sim(data[medoid], data[user]) for user in users])


def replace_empty_cluster(used_medians, all_users):
    all_users = list(all_users - used_medians)

    if len(all_users) == 0:
        return -1

    return all_users[random.randint(0, len(all_users) - 1)]



def kmedoids(data, k=2, max_iter=100, sim=jaccard_sim):
    all_users = set(data.keys())
    tried_medoids = set()

    # cluster_users, user_cluster = init_clusters(data, k)
    medoids = random_medoids(data, k)
    tried_medoids = medoids
    cluster_users = {}
    user_clusters = {}
    new_cluster_users = {}
    for m in medoids:
        new_cluster_users[m] = {}

    medoids_to_try = True
    for i in xrange(max_iter):
        cluster_users = new_cluster_users
        print 'Clusters1\t', cluster_users
        # print user_cluster
        # Assign users to clusters
        for user in data:
            # old_cluster = user_cluster[user]
            best_clust = -1
            best_sim = -1
            for cluster in cluster_users:
                similarity = sim(data[cluster], data[user])
                # print cluster, user, sim(data[cluster], data[user])
                if similarity > best_sim:
                    best_sim = similarity
                    best_clust = cluster

            cluster_users[best_clust][user] = best_sim

        clusters = cluster_users.keys()
        for clust in clusters:
            if len(cluster_users[clust]) == 0:
                new_medoid = replace_empty_cluster(medoids, all_users)
                if new_medoid == -1:
                    medoids_to_try = False
                    break
                cluster_users[new_medoid] = {}
                del cluster_users[clust]

        new_cluster_users = {}
        # Update medoids

        change = False
        for clust, users in cluster_users.iteritems():
            # print 'users', users
            best_sim = sum(users.values())
            best_median = clust
            for user in users:
                similarity = 1.0 * within_sim(data, user, users, sim) / len(users)
                # print 'sim', similarity
                if similarity > best_sim:
                    best_sim = similarity
                    best_median = user
                    change = True
            new_cluster_users[best_median] = {}

        if not change and not medoids_to_try:
            return cluster_users

            # for user in users:
            #     user_cluster[user] = best_median

        # cluster_users = new_cluster_users
        print cluster_users
    return cluster_users

print kmedoids(friends)