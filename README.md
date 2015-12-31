# Windu API

![Windu icon](https://avatars3.githubusercontent.com/u/12955363?v=3&s=200)



**Windu** is an open source messaging platform 

REST API
========
## Login/Token Request
* Request OAuth token

		curl -X POST -d "grant_type=password&username=<user>&password=<password>&client_id=RoVMZF1EIpC2vcfGC864gr4NZsv0mJlyPlE3gtQY" https://windu.herokuapp.com/o/token/
		
* Refreshing your token

		curl -X POST -d "grant_type=refresh_token&refresh_token=<refresh_token>&client_id=RoVMZF1EIpC2vcfGC864gr4NZsv0mJlyPlE3gtQY" https://windu.herokuapp.com/o/token/

		
* Using your token

	*You will need send the Authentication header for every request, the next examples will omit the authentication header only for the sake of cleanliness.*
		
		curl -H "Authorization: Bearer <Token>" https://windu.herokuapp.com/api/call
		


## Account 

### Status Message

* Get account status message:

		curl -X GET http://windu.herokuapp.com:8000/api/account/status-message/
		
* Update account status message:

		curl -X POST -d "status_message=😍😍😍😍" http://windu.herokuapp.com/api/account/status-message/

### Profile photo

* Get profile photo:

		curl -X GET http://windu.herokuapp.com:8000/api/account/profile-photo/
		
* Update profile photo:

		curl -X POST -F "photo=@photo.jpg" http://windu.herokuapp.com/api/account/profile-photo/
		
* Remove profile photo:

		curl -X DELETE http://windu.herokuapp.com:8000/api/account/profile-photo/
		
### Connected Status

* Get current connected status:

		curl -X GET http://windu.herokuapp.com:8000/api/account/connected-status/
		
* Update connected status to *online* :

		curl -X POST -d "status=online" http://windu.herokuapp.com/api/account/status-message/
		

		
		
