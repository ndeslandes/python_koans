#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: Create a Proxy Class
#
# In this assignment, create a proxy class (one is started for you
# below).  You should be able to initialize the proxy object with any
# object.  Any attributes called on the proxy object should be forwarded
# to the target object.  As each attribute call is sent, the proxy should
# record the name of the attribute sent.
#
# The proxy class is started for you.  You will need to add a method
# missing handler and any other supporting methods.  The specification
# of the Proxy class is given in the AboutProxyObjectProject koan.

# Note: This is a bit trickier that its Ruby Koans counterpart, but you
# can do it!
from collections import Counter

from runner.koan import *


class Proxy(object):
   def __init__(self, target_object):
      # WRITE CODE HERE
      self._messages = []
      #initialize '_obj' attribute last. Trust me on this!
      self._obj = target_object

   # WRITE CODE HERE
   def messages(self):
      return self._messages

   def was_called(self, message):
      return message in self._messages

   def number_of_times_called(self, message):
      _count = Counter(self._messages).get(message)
      if _count:
         return _count
      else: # catch None
         return 0

   def __getattribute__(self, attr_name):
      try: # call on self
         retval = object.__getattribute__(self, attr_name)
      except AttributeError: # call on child object
         retval = self._obj.__getattribute__(attr_name)
         object.__getattribute__(self, '_messages').append(attr_name)

      return retval

   def __setattr__(self, attr_name, attr_value):
      if hasattr(self, '_obj'): # call child object and log message
         self._obj.__setattr__(attr_name, attr_value)
         object.__getattribute__(self, '_messages').append(attr_name)
      else: # use this before_obj is set in __init__
         object.__setattr__(self, attr_name, attr_value)

   def messages(self):
      return self._messages


# The proxy object should pass the following Koan:
#
class AboutProxyObjectProject(Koan):
   def test_proxy_method_returns_wrapped_object(self):
      # NOTE: The Television class is defined below
      tv = Proxy(Television())

      self.assertTrue(isinstance(tv, Proxy))

   def test_tv_methods_still_perform_their_function(self):
      tv = Proxy(Television())

      tv.channel = 10
      tv.power()

      self.assertEqual(10, tv.channel)
      self.assertTrue(tv.is_on())

   def test_proxy_records_messages_sent_to_tv(self):
      tv = Proxy(Television())

      tv.power()
      tv.channel = 10

      self.assertEqual(['power', 'channel'], tv.messages())

   def test_proxy_handles_invalid_messages(self):
      tv = Proxy(Television())

      ex = None
      try:
         tv.no_such_method()
      except AttributeError as ex:
         pass

      self.assertEqual(AttributeError, type(ex))

   def test_proxy_reports_methods_have_been_called(self):
      tv = Proxy(Television())

      tv.power()
      tv.power()

      self.assertTrue(tv.was_called('power'))
      self.assertFalse(tv.was_called('channel'))

   def test_proxy_counts_method_calls(self):
      tv = Proxy(Television())

      tv.power()
      tv.channel = 48
      tv.power()

      self.assertEqual(2, tv.number_of_times_called('power'))
      self.assertEqual(1, tv.number_of_times_called('channel'))
      self.assertEqual(0, tv.number_of_times_called('is_on'))

   def test_proxy_can_record_more_than_just_tv_objects(self):
      proxy = Proxy("Py Ohio 2010")

      result = proxy.upper()

      self.assertEqual("PY OHIO 2010", result)

      result = proxy.split()

      self.assertEqual(["Py", "Ohio", "2010"], result)
      self.assertEqual(['upper', 'split'], proxy.messages())


# ====================================================================
# The following code is to support the testing of the Proxy class.  No
# changes should be necessary to anything below this comment.

# Example class using in the proxy testing above.
class Television(object):
   def __init__(self):
      self._channel = None
      self._power = None

   @property
   def channel(self):
      return self._channel

   @channel.setter
   def channel(self, value):
      self._channel = value

   def power(self):
      if self._power == 'on':
         self._power = 'off'
      else:
         self._power = 'on'

   def is_on(self):
      return self._power == 'on'


# Tests for the Television class.  All of theses tests should pass.
class TelevisionTest(Koan):
   def test_it_turns_on(self):
      tv = Television()

      tv.power()
      self.assertTrue(tv.is_on())

   def test_it_also_turns_off(self):
      tv = Television()

      tv.power()
      tv.power()

      self.assertFalse(tv.is_on())

   def test_edge_case_on_off(self):
      tv = Television()

      tv.power()
      tv.power()
      tv.power()

      self.assertTrue(tv.is_on())

      tv.power()

      self.assertFalse(tv.is_on())

   def test_can_set_the_channel(self):
      tv = Television()

      tv.channel = 11
      self.assertEqual(11, tv.channel)
