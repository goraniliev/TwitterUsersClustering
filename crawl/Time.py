# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
from api.API import get_api_instance

__author__ = 'goran'


def get_top_user_names(num=1, url='http://www.time.mk/twitter/topfoll/'):
    page = urllib2.urlopen(url + str(num))
    soup = BeautifulSoup(page)

    user_names = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None and href.startswith('twitter/user/'):
            screen_name = href[13:]
            # idx, name = get_id_and_name_by_screen_name(api, screen_name)
            # users.append((int(idx), screen_name, name))
            user_names.append(screen_name)
    return user_names


def get_top_users_from_p_pages(p=100):
    user_names = []
    p += 1
    for i in xrange(1, p):
        user_names += get_top_user_names(num=p)

    return user_names


def get_top_users(api, user_names):
    users = []
    for i in xrange(0, len(user_names), 15):
        users += api.lookup_users(user_names[i:min(i+15, len(user_names))])
    return users