# -*- coding: utf-8 -*-

# This will be accessible at the URL: /start/cats/<function>

import random

GREETINGS = ['Hola', 'Ciao', "Bonjour", 'Hello', 'Ya/Su']


# This will be accessible at the URL: /start/cats/onechi
def onechi():
    if session.c is None:
        session.c = 1
    else:
        session.c += 1
    return dict(greeting=random.choice(GREETINGS),
                count=session.c)

def twochi():
    greeting = request.args[0]
    logger.info("The greeting is: %r" % greeting)
    return dict(greeting=greeting)
