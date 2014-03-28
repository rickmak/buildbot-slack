buildbot-slack
==============

Simple Script for push notification to slack.com from buildbot http://buildbot.net
Depends on requests-2.2.1

Usage
=====
at buildbot.cfg file, 

```
import slack
master_config['status'].append(
    slack.StatusPush(
        "domain.slack.com",
        "your-secret-token",
        "#channel",
        localhost_replace="buildbot.retain.cc")
    )
```
