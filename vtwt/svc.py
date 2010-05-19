import os, sys

from twisted.application.service import Service
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue

from jersey import log

from twittytwister.twitter import TwitterFeed

from vtwt.util import recodeText



class VtwtService(Service):

    name = "vtwt"

    def __init__(self, user, password):
        self._twt = self._buildTwitterClient(user, password)


    def _buildTwitterClient(self, user, password):
        return TwitterFeed(user, password)


    @inlineCallbacks
    def getHomeTimeline(self, params={}):
        """Get recent updates from a user's timeline.
        """
        log.trace("Getting home timeline.")

        messages = []
        yield self._twt.home_timeline(lambda m: messages.insert(0, m), params)

        for msg in messages:
            msg.text = self._recodeText(msg.text)

        returnValue(messages)


    @inlineCallbacks
    def getUserTimeline(self, user, params={}):
        """Get recent updates from the user's home timeline.
        """
        log.trace("Getting timeline for {0}".format(user))

        messages = []
        yield self._twt.user_timeline(lambda m: messages.insert(0, m),
                user, params)

        for msg in messages:
            msg.text = self._recodeText(msg.text)

        returnValue(messages)


    def _recodeText(self, text):
        """Recode HTML entities refs; e.g. '&amp;' to '&'
        
        Work around buggy Twitter clients that mangle retweets such that
        &amp;lt;3 recodes to <3 (instead of &lt;3).
        """
        return recodeText(recodeText(text))


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


    def unblock(self, user):
        return self._twt.unblock(user)


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



