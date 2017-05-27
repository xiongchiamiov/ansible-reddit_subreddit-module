#!/usr/bin/env python

import praw
from ansible.module_utils.basic import *

VERSION = '0.0.1'

def main():
    argument_spec = {
        'client_id': {"required": True, "type": "str"},
        'client_secret': {"required": True, "type": "str"},
    }
    module = AnsibleModule(argument_spec=argument_spec)

    # According to reddit API rules, needs to be in the format:
    #     <platform>:<app ID>:<version string> (by /u/<reddit username>)
    # https://github.com/reddit/reddit/wiki/API
    user_agent = 'Unknown:ansible-reddit_subreddit-module:v{}' \
                 '(by u/xiongchiamiov)'.format(VERSION)
    reddit = praw.Reddit(client_id=module.params['client_id'],
                         client_secret=module.params['client_secret'],
                         user_agent=user_agent)

    module.exit_json(changed=True)

if __name__ == '__main__':
    main()
