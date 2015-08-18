

def getUserProfileFromUser(User):
	print (User.user)
	user_profile = UserProfile.objects.get(User=User)
	return user_profile