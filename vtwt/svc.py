import os, sys

from twisted.application.service import Service
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue

from jersey import log

from twittytwister.twitter import TwitterFeed

from vtwt.util import decodeText


class VtwtService(Service):

    def __init__(self, user, password):
        self._twt = TwitterFeed(user, password)
        self._mostRecentId = None


    @inlineCallbacks
    def getTimelineUpdates(self, sinceId=None):
        params = {}
        if sinceId:
            params["since_id"] = sinceId
        if self._mostRecentId:
            params["since_id"] = self._mostRecentId

        messages = []
        yield self._twt.home_timeline(lambda m: messages.insert(0, m), params)

        for msg in messages:
            msg.text = decodeText(msg.text)
        if messages:
            self._mostRecentId = messages[-1].id

        returnValue(messages)


    def tweet(self, text):
        return self._twt.update(text)


    def follow(self, users):
        d = Deferred()
        self._twt.follow_user(self.config["friend"],
                d.callback).addErrback(d.errback)
        return d


    def unfollow(self, users):
        d = Deferred()
        self._twt.unfollow_user(self.config["friend"],
                d.callback).addErrback(d.errback)
        return d


    @inlineCallbacks
    def getFollowers(self, user=None):
        followers = []
        yield self._twt.list_followers(lambda f: followers.insert(0, f), user)
        returnValue(followers)


    @inlineCallbacks
    def getFollowed(self, user=None):
        followees = []
        yield self._twt.list_friends(lambda f: followees.insert(0, f), user)
        returnValue(followees)



