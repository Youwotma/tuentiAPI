#!/bin/env/python

 # tuentiAPI Class
 # Python implementation of the PHP API by Sergios Cruz aka scromega (scr.omega at gmail dot com) http://scromega.net
 #
 # More info:
 # http://scromega.net/7-accediendo-a-la-api-cerrada-de-tuenti.html
 
 
 # Modo de uso:
 #
 # from tuentiAPI import tuentiAPI
 # api = tuentiAPI("cani@hotmail.com","1234")  # (tu usuario y password)
 # print api.request("getFriends",{})
 # friends,inbox = api.mrequest( (("getFriends",{}),("getInbox",{})) )
 # print friends
 # print inbox

import simplejson
import hashlib
import httplib2

class tuentiAPI:
	user_data = {}
	def __init__(self,email,pw):
		raw_response = self.http(self.json((("getChallenge",{"type":"login"}),)))
		response = simplejson.loads(raw_response)[0]
		passcode = self.md5(response['challenge']+self.md5(pw))
		appkey = ('MDI3MDFmZjU4MGExNWM0YmEyYjA5MzRkODlm'+
		          'Mjg0MTU6MC4xMzk0ODYwMCAxMjYxMDYwNjk2')
		raw_response = self.http(self.json((('getSession',{
			"passcode":passcode,
			"application_key":appkey,
			"timestamp":response['timestamp'],
			"seed":response['seed'],
			"email":email
		}),)))
		self.user_data = simplejson.loads(raw_response)[0]

	def md5(self,str):
		return hashlib.md5(str).hexdigest()
	def http(self,data):
		headers = {"Content-length":str(len(data))}
		url = 'http://api.tuenti.com/api/'
		http = httplib2.Http()
		request, reply = http.request(url,'POST',headers = headers,body = data)
		return reply
	def json(self,iterable):
		calls = []
		request = {}
		for k in iterable:
			calls.append(k[:2])
		
		if self.user_data.get("session_id",False):
			request['session_id'] = self.user_data['session_id']
		request['version'] = '0.4'
		request['requests'] = calls
		return simplejson.dumps(request)
	def request(self,method, parameters={}):
		return self.mrequest(((method, parameters),))[0]
	def mrequest(self,iterable):
		tmp = self.json(iterable)
		tmp = self.http(tmp)
		tmp = simplejson.loads(tmp)
		return tmp

