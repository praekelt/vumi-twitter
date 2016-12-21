Vumi Twitter Transport
======================

.. image:: https://img.shields.io/travis/praekelt/vumi-twitter.svg
    :target: https://travis-ci.org/praekelt/vumi-twitter

.. image:: https://coveralls.io/repos/praekelt/vumi-twitter/badge.png?branch=develop
    :target: https://coveralls.io/r/praekelt/vumi-twitter?branch=develop
    :alt: Code Coverage


The Twitter transport allows any Vumi_ application to interact with Twitter users, by making use of the Twitter APIs_.

Getting Started
===============

Prerequisites
~~~~~~~~~~~~~

In order to run the Twitter transport, you need to have set up a Twitter app. Go to https://apps.twitter.com and sign in, then select "Create New App". Fill in the required fields (you don't need to worry too much about "Website" and "Callback URL") and create the application.

You should be redirected to your app's dashboard. We now need to generate an API access token. Head to the "Permissions" tab and make sure that it's set to "Read, Write and Access direct messages". Then head back to the "Keys and Access Tokens" tab and select "Create my Access Token".

You should now have a total of four tokens on your dashboard: a consumer key, consumer secret, access token, and access token secret. We're ready to move on to the next step.

Setting up the channel
~~~~~~~~~~~~~~~~~~~~~~

The best way to run the transport is by making use of Junebug_, which allows you to launch and manage Vumi transports using a RESTful HTTP interface. The transport also requires Redis and RabbitMQ to run. Install them as follows::

    $ sudo apt-get install redis-server rabbitmq-server
    $ pip install junebug
    $ pip install vxtelegram

You should have both Redis and RabbitMQ running to start the transport::

    $ sudo service redis-server start
    $ sudo service rabbitmq-server start

Launch Junebug with the Twitter channel configured::

    $ jb -p 8080 \
    $   --channels telegram:vxtwitter.twitter.TwitterTransport \
    $   --logging-path logs

.. note::

    If your logs end with something other than ``Got an authenticated AMQP connection``, you might have to change some RabbitMQ permissions. Run the following commands to set RabbitMQ up correctly::

        $ sudo rabbitmqctl add_user vumi vumi
        $ sudo rabbitmqctl add_vhost /develop
        $ sudo rabbitmqctl set_permissions -p /develop vumi '.*' '.*' '.*'

To create the channel and launch the transport, we can post the channel's config file to Junebug. The config file should be in the following format (we'll call it ``config.json``):

.. code-block:: json

    {
        "type": "twitter",
        "amqp_queue": "twitter_transport",
        "config": {
            "transport_name": "twitter_transport",
            "screen_name": "SCREEN_NAME",
            "consumer_key": "CONSUMER_KEY",
            "consumer_secret": "CONSUMER_SECRET",
            "access_token": "ACCESS_TOKEN",
            "access_token_secret": "ACCESS_TOKEN_SECRET",
            "terms": ["TERMS"],
            "autofollow": "AUTOFOLLOW",
            "autoresponse": "AUTORESPONSE",
            "autoresponse_type": "AUTORESPONSE_TYPE"
        }
    }

Explanation of config fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``SCREEN_NAME``: your Twitter handle
- ``CONSUMER_KEY``: your API consumer key, obtained from your app's dashboard
- ``CONSUMER_SECRET``: your consumer secret, obtained from your app's dashboard
- ``ACCESS_TOKEN``: your API access token, obtained from your app's dashboard
- ``ACCESS_TOKEN_SECRET``: your access token secret, obtained from your app's dashboard
- ``TERMS``: a list of terms you want the transport to track (optional - if given, the transport will "receive" all new tweets that contain the given terms)
- ``AUTOFOLLOW``: ``true`` or ``false``, whether your bot should automatically follow users who follow it
- ``AUTORESPONSE``: ``true`` or ``false``, whether your bot should automatically respond to users who follow it
- ``AUTORESPONSE_TYPE``: how to respond to users who follow your bot (optional - one of ``dms`` or ``tweets``)

Starting the transport
~~~~~~~~~~~~~~~~~~~~~~

Starting the transport is as simple as posting the config file to Junebug::

    $ curl -X POST -d@config.json http://localhost:8080/channels/

Your transport is now up and running! You can check which channels you have running in Junebug at any time by making the following request::

    $ curl -X GET http://localhost:8080/channels/

You can also view details of a specific channel by making a GET request like::

    $ curl -X GET localhost:8080/channels/<channel_id>

and delete a channel by making a DELETE request to that same URL. Sending a message over your channel is as simple as::

    $ curl -X POST -d MESSAGE_PAYLOAD http://localhost:8080/channels/<channel_id>/messages/

Running the transport with a Vumi application
=============================================

Running a Vumi application as a Twitter bot is incredibly easy once the transport is running::

    $ twistd -n vumi_worker \
        --worker-class=vumi.demos.words.EchoWorker \
        --set-option=transport_name:twitter_transport

Embedding images in tweets
==========================

The Twitter transport is capable of uploading images and embedding them in tweets. To make use of this functionality, include the following payload in your messages' ``helper_metadata``:

.. code-block:: python

    helper_metadata={
        'twitter': {
            'media': [
                'file_path': 'PATH_TO_IMAGE',
            ],
        },
    }

Please note that some limitations apply, and a maximum of four images can be embedded (see here_). Also note that embedded GIFs or videos are not yet supported by the transport.

Things to note
==============

Inbound messages published by the transport contain some helpful extra information in their ``helper_metadata`` fields. For example, inbound tweets contain the following payload:

.. code-block:: python

    helper_metadata={
        'twitter': {
            'in_reply_to_status_id': ''     # The status the tweet is in response to
            'in_reply_to_screen_name': ''   # The handle of the user being replied to
            'user_mentions': []             # A list of users tagged in the tweet
        }
    }

whereas inbound direct messages contain the following metadata:

.. code-block:: python

    helper_metadata={
        'dm_twitter': {
            'id': ''                # The id of the direct message
            'user_mentions': []     # A list of users mentioned in the message
        }
    }

User profile information
~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to make requests to Twitter's API is by using twurl_, a cURL-like command line program tailored specifically for Twitter. Make sure you have Ruby installed and run::

    $ gem install twurl

To authourise twurl to access protected resources, run the following command::

    $ twurl authorize --consumer-key YOUR_CONSUMER_KEY --consumer-secret YOUR_CONSUMER_SECRET

This returns a URL that you can open in the browser. Do so, log in to Twitter, and you'll receive a code. Paste that code into the (still running) terminal and press Enter. Twurl is now authourised to make requests to Twitter.

Getting a user's profile information is now as simple as::

    $ twurl /1.1/users/show?user_id=USER_ID

or, using their Twitter handle::

    $ twurl /1.1/users/show?screen_name=USER_HANDLE

.. _Vumi: http://vumi.readthedocs.org
.. _APIs: https://dev.twitter.com/docs
.. _Junebug: http://junebug.readthedocs.org
.. _here: https://dev.twitter.com/rest/media/uploading-media.html#imagerecs
.. _twurl: https://github.com/twitter/twurl
