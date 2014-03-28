import os
import json
import requests

from buildbot.status.base import StatusReceiverMultiService
from buildbot.status.builder import Results, SUCCESS


class StatusPush(StatusReceiverMultiService):

    def __init__(self, domain, token, channel, localhost_replace=False, **kwargs):
        StatusReceiverMultiService.__init__(self)
        self.domain = domain
        self.token = token
        self._url = "https://%s/services/hooks/incoming-webhook?token=%s" % \
            (self.domain, self.token)
        self.channel = channel
        self.localhost_replace = localhost_replace

    def setServiceParent(self, parent):
        StatusReceiverMultiService.setServiceParent(self, parent)
        self.master_status = self.parent
        self.master_status.subscribe(self)
        self.master = self.master_status.master

    def disownServiceParent(self):
        self.master_status.unsubscribe(self)
        self.master_status = None
        for w in self.watched:
            w.unsubscribe(self)
        return StatusReceiverMultiService.disownServiceParent(self)

    def builderAdded(self, name, builder):
        return self  # subscribe to this builder

    def buildFinished(self, builderName, build, result):
        url = self.master_status.getURLForThing(build)
        if self.localhost_replace:
            url = url.replace("//localhost", "//%s" % self.localhost_replace)

        message = "%s - %s - <%s>" % \
            (builderName, Results[result].upper(), url)
        payload = {
            'channel': self.channel,
            'username': 'Buildbot',
            'text': message
        }
        if result == SUCCESS:
            payload['icon_emoji'] = ':sunglasses:'
        else:
            payload['icon_emoji'] = ':skull:'

        requests.post(
            self._url,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(payload)
        )
