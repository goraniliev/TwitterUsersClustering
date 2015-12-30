# -*- coding: utf-8 -*-
import tweepy

__author__ = 'goran'

def get_api_instance(consumer_key='8wiTu4VA2HQ8IacbcOcxG5N6e',
                     consumer_secret='5btRjpbp1K7rHRtxJqWVeaeMnCEOZK5Ypp6D2i1kp9h0cmPlNR',
                     access_token='241699249-2zZJjh8Lgkh80WHh5Gvj1MLqSNHJqS1LOSvcnmsN',
                     access_token_secret='blkvpDNPadb2iTcLyG1iURLH12kxidkq0zELvmJj4xDrT'):
    '''
    Returns tweepy.api.API object, which gives authorized access to the Twitter API.
    It is obligatory to have access tokens to access Twitter API.
    :param consumer_key:
    :param consumer_secret:
    :param access_token:
    :param access_token_secret:
    :return:
    '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    """
    @type api: tweepy.api.API
    """
    api = tweepy.API(auth)

    return api


def get_id_and_name_by_screen_name(api, screen_name):
    user = api.get_user(screen_name)
    return int(user.id), user.name.encode('utf-8')
