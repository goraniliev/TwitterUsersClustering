# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
from common.common import is_inserted

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
    return [(u.id, u.screen_name, u.name.encode('utf-8'))
            for u in api.lookup_users(screen_names=user_names) if not is_inserted(u.id)]
