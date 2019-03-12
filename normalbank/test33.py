import itchat
itchat.auto_login()

friends=itchat.get_friends()
user = itchat.search_friends(name='阿朱')
username = user[0]['UserName']
print(username)
