import os, sys

from twisted.application.service import Service
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue

from jersey import log

from twittytwister.twitter import TwitterFeed

from vtwt.util import recodeText



class VtwtService(Service):

    def __init__(self, user, password):
        self._twt = self._buildTwitterClient(user, password)
        self._mostRecentId = None


    def _buildTwitterClient(self, user, password):
        return TwitterFeed(user, password)


    @inlineCallbacks
    def getTimelineUpdates(self, params={}):
        """Get recent updates from the user's home timeline.
        """
        if self._mostRecentId:
            params.setdefault("since_id", self._mostRecentId)

        messages = []
        yield self._twt.home_timeline(lambda m: messages.insert(0, m), params)
        for msg in messages:
            msg.text = recodeText(msg.text)
            self._mostRecentId = msg.id

        returnValue(messages)


    def tweet(self, text):
        return self._twt.update(text)


    @inlineCallbacks
    def follow(self, user):
        users = []
        yield self._twt.follow_user(user, users.append)
        returnValue(users[0])


    @inlineCallbacks
    def unfollow(self, user):
        users = []
        yield self._twt.unfollow_user(user, users.append)
        returnValue(users[0])


    def block(self, user):
        return self._twt.block(user)


    @inlineCallbacks
    def getFollowers(self, user=None):
        followers = []
        yield self._twt.list_followers(lambda f: followers.insert(0, f), user)
        returnValue(followers)


    @inlineCallbacks
    def getFollowees(self, user=None):
        followees = []
        yield self._twt.list_friends(lambda f: followees.insert(0, f), user)
        returnValue(followees)



