from tuentiAPI import tuentiAPI
api = tuentiAPI("cani@hotmail.com","1234")  # (tu usuario y password)
print api.request("getFriends",{})
friends,inbox = api.mrequest( (("getFriends",{}),("getInbox",{})) )
print friends
print inbox