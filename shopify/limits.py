#!/usr/bin/python

############################################################
#
# Copyright 2016 Paladin Logic, Ltd
#           All Rights Reserved
#
############################################################


# Imports
import shopify
import logging
from functools import wraps

logger = logging.getLogger('root').getChild('shopify.limits')

CREDIT_LIMIT_HEADER_PARAM = 'x-shopify-shop-api-call-limit'

def debug(f):
    fname = f.func_name

    @wraps(f)
    def wrapped(*args, **kwargs):
        r = f(*args, **kwargs)

        logger.debug("%s() output '%s'", fname, r)
        return r

    return wrapped

# Functions
@debug
def api_credit_limit_param():
    return shopify.ShopifyResource.connection.response.headers[CREDIT_LIMIT_HEADER_PARAM].split('/')

@debug
def credit_left():
    return credit_limit() - credit_used()

@debug
def credit_maxed():
    return credit_left() <= 1

@debug
def credit_limit():
    return int(api_credit_limit_param()[1])

@debug
def credit_used():
    return int(api_credit_limit_param()[0])

#Function Aliases
available_calls = credit_left
maxed = credit_maxed
call_limit = credit_limit
call_count = credit_used
