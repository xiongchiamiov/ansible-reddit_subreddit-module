#!/usr/bin/env python

import praw
from ansible.module_utils.basic import *

VERSION = '0.0.1'

def main():
    argument_spec = {
        'client_id': {'required': True, 'type': 'str'},
        'client_secret': {'required': True, 'type': 'str'},
        'username': {'required': True, 'type': 'str'},
        'password': {'required': True, 'type': 'str'},
        'subreddit': {'required': True, 'type': 'str'},
    }
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    # According to reddit API rules, needs to be in the format:
    #     <platform>:<app ID>:<version string> (by /u/<reddit username>)
    # https://github.com/reddit/reddit/wiki/API
    user_agent = 'Unknown:ansible-reddit_subreddit-module:v{}' \
                 '(by u/xiongchiamiov)'.format(VERSION)
    reddit = praw.Reddit(client_id=module.params['client_id'],
                         client_secret=module.params['client_secret'],
                         username=module.params['username'],
                         password=module.params['password'],
                         user_agent=user_agent)

    subreddit = reddit.subreddit(module.params['subreddit'])
    current_text = subreddit.stylesheet().stylesheet
    new_text = '.foo { color: red; }'
    changed = current_text != new_text
    if changed and not module.check_mode:
        # Note that subreddit.stylesheet is different than
        # subreddit.stylesheet() !
        subreddit.stylesheet.update(new_text)

    module.exit_json(changed=changed, read_only=reddit.read_only,
                     params=module.params, current_text=current_text,
                     new_text=new_text)

if __name__ == '__main__':
    main()
