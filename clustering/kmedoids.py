# -*- coding: utf-8 -*-
from math import sqrt
import random
from db.Insert_users import get_connection
from db.get_utilities import get_friends
from get_utilities import get_followers

__author__ = 'goran'


def jaccard_sim(set1, set2):
    return 1.0 * len(set1 & set2) / len(set1 | set2)


def paper_sim(set1, set2):
    return 1.0 * len(set1 & set2) / (sqrt(len(set1)) * sqrt(len(set2)))


def random_medoids(user_ids, k=2):
    medoids = set()
    # user_ids = data.keys()
    num_users = len(user_ids)

    while len(medoids) < k:
        new_medoid_idx = random.randint(0, num_users - 1)
        if new_medoid_idx not in medoids:
            medoids.add(user_ids[new_medoid_idx])

    return medoids


def init_clusters(friends, followers, k, sim=jaccard_sim):
    cluster_users = {}
    user_ids = friends.keys()
    medoids = random_medoids(user_ids, k)
    for clust in medoids:
        cluster_users[clust] = set([clust])
    user_clusters = {}

    for user in user_ids:
        best_sim = -1
        best_medoid = -1
        for medoid in medoids:
            similarity = (sim(friends[medoid], friends[user]) + sim(followers[medoid], followers[user])) / 2.0;
            if similarity > best_sim:
                best_sim = similarity
                best_medoid = medoid
        user_clusters[user] = best_medoid
        cluster_users[best_medoid].add(user)
    return cluster_users, user_clusters


def within_sim(friends, followers, medoid, users, sim=jaccard_sim):
    return sum([(sim(friends[medoid], friends[user]) + sim(followers[medoid], followers[user])) / 2.0 for user in users])


def replace_empty_cluster(used_medians, all_users):
    all_users = list(all_users - used_medians)

    if len(all_users) == 0:
        return -1

    return all_users[random.randint(0, len(all_users) - 1)]


def kmedoids(friends, followers, k=2, max_iter=100, sim=jaccard_sim):
    all_users = set(friends.keys())

    # cluster_users, user_cluster = init_clusters(data, k)
    medoids = random_medoids(friends.keys(), k)
    cluster_users = {}
    new_cluster_users = {}
    for m in medoids:
        new_cluster_users[m] = {}

    medoids_to_try = True
    for i in xrange(max_iter):
        print i, 'iteration'
        cluster_users = new_cluster_users

        # Assign users to clusters
        for user in all_users:
            best_clust = -1
            best_sim = -1
            for cluster in cluster_users:
                similarity = (sim(friends[cluster], friends[user]) + sim(followers[cluster], followers[user])) / 2.0
                # print cluster, user, sim(data[cluster], data[user])
                if similarity > best_sim:
                    best_sim = similarity
                    best_clust = cluster

            cluster_users[best_clust][user] = best_sim

        print i, ' '.join([str((str(clust), len(cluster_users[clust]))) for clust in cluster_users])

        clusters = cluster_users.keys()
        for clust in clusters:
            if len(cluster_users[clust]) == 0:
                new_medoid = replace_empty_cluster(medoids, all_users)
                if new_medoid == -1:
                    medoids_to_try = False
                    break
                cluster_users[new_medoid] = {}
                medoids.add(new_medoid)
                del cluster_users[clust]

        new_cluster_users = {}

        # Update medoids
        change = False
        for clust, users in cluster_users.iteritems():
            # print 'users', users
            best_sim = 1.0 * within_sim(friends, followers, clust, users, sim) / len(users)
            best_median = clust
            for user in users:
                similarity = 1.0 * within_sim(friends, followers, user, users, sim) / len(users)
                # print 'sim', similarity
                if similarity > best_sim:
                    best_sim = similarity
                    best_median = user
                    change = True
            new_cluster_users[best_median] = {}

        # old_keys = set(cluster_users.keys())
        # new_keys = set(new_cluster_users.keys())
        # print 'old', old_keys
        # print 'new', new_keys
        # print old_keys == new_keys
        if set(new_cluster_users.keys()) == set(cluster_users.keys()) or (not change and not medoids_to_try):
            return cluster_users

    return cluster_users


def get_clusters(k=3):
    friends = get_friends()
    followers = get_followers()

    # red_f = {}
    # count = 200
    # for f in friends:
    #     red_f[f] = friends[f]
    #     count -= 1
    #     if count == 0:
    #         break

    return kmedoids(friends, followers, k)

# friends = get_friends()
# with open('friends.txt', 'w') as fout:
#     for f in friends:
#         fout.write(str(f) + '\t' + str(len(friends[f])) + '\n')


def update_clusters_in_db():
    clusters = get_clusters()
    db = get_connection()
    cursor = db.cursor()
    for cluster, users in clusters.iteritems():
        for user in users:
            cursor.execute("""update user set cluster=%s where iduser=%s""", (cluster, user))
            db.commit()
    cursor.close()
    db.close()

update_clusters_in_db()