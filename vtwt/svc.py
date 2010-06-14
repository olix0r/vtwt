import os, sys

from twisted.application.service import Service
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue

from jersey import log

from twittytwister.twitter import TwitterFeed

from vtwt.util import recodeText



class VtwtService(Service):

    def __init__(self, user, password):
        self.name = "vtwt:{0}".format(user)
        self.user = user
        self._twt = self._buildTwitterClient(user, password)


    def _buildTwitterClient(self, user, password):
        return TwitterFeed(user, password)


    @inlineCallbacks
    def getTimeline(self, user=None, params={}):
        """Get recent updates from a user's timeline.
        """
        log.trace("Getting home timeline.")

        messages = []
        def addMessage(msg):
            msg.text = self._recodeText(msg.text)
            messages.insert(0, msg)

        if user in (None, "home"):
            yield self._twt.home_timeline(addMessage, params)
        else:
            yield self._twt.user_timeline(addMessage, user, params)

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
        """Follow a user.  Return a dictionary representing the user.
        """
        users = []
        yield self._twt.follow_user(user, users.append)
        returnValue(users[0])


    @inlineCallbacks
    def unfollow(self, user):
        """Unfollow a user.  Return a dictionary representing the user.
        """
        users = []
        yield self._twt.unfollow_user(user, users.append)
        returnValue(users[0])


    def block(self, user):
        """Block a user.
        """
        users = []
        return self._twt.block(user)


    def unblock(self, user):
        """Unblock a user.
        """
        return self._twt.unblock(user)


    @inlineCallbacks
    def getFollowers(self, user=None):
        """Get a list of followers (optionally, for another user).
        """
        followers = []
        yield self._twt.list_followers(lambda f: followers.insert(0, f), user)
        returnValue(followers)


    @inlineCallbacks
    def getFollowees(self, user=None):
        """Get a list of users following 
        """
        followees = []
        yield self._twt.list_friends(lambda f: followees.insert(0, f), user)
        returnValue(followees)



