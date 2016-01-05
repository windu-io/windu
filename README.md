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

An account is linked to your number, in order to use Windu API you need to add and register an account.

With exception of `create-account` every method accept an optional `account=000000` parameter, if you don't provide any account the first account will be used.

### Adding, Registering and Removing account number.

* Creating account, you will receive a SMS with the code to register your account

		curl -X POST -d "account=000000000&nickname=John Lennon" https://windu.herokuapp.com/api/account/create-account/

* If you already added an account, but want to receive a new SMS code to register:
  
		curl -X POST -d "account=000000000" https://windu.herokuapp.com/api/account/request-sms-code/
		
* Or if you want to receive a voice call:

		curl -X POST -d "account=000000000" https://windu.herokuapp.com/api/account/request-voice-code/
		
* After receive your code you need to register your account:

		curl -X POST -d "code=<received code>" https://windu.herokuapp.com/api/account/register-code/
		
* If you want to remove your account:
		
		curl -X POST -d "account=000000000&feedback=cool" https://windu.herokuapp.com/api/account/remove-account/


### Status Message

* Get account status message:

		curl -X GET https://windu.herokuapp.com/api/account/status-message/
		
* Update account status message:

		curl -X POST -d "status_message=😍😍😍😍" https://windu.herokuapp.com/api/account/status-message/

### Profile photo

* Get profile photo:

		curl -X GET https://windu.herokuapp.com/api/account/profile-photo/
		
* Update profile photo:

		curl -X POST -F "photo=@photo.jpg" https://windu.herokuapp.com/api/account/profile-photo/
		
* Remove profile photo:

		curl -X DELETE https://windu.herokuapp.com/api/account/profile-photo/
		
### Connected Status

* Get current connected status:

		curl -X GET https://windu.herokuapp.com/api/account/connected-status/
		
* Update connected status to *online* :

		curl -X POST -d "status=online" https://windu.herokuapp.com/api/account/connected-status/
		
### Nickname

* Get current nickname:

		curl -X GET https://windu.herokuapp.com/api/account/nickname/
		
* Update your nickname (The nickname will appear on your notifications):

		curl -X POST -d "nickname=🚚🚎MyNick🚒" https://windu.herokuapp.com/api/account/nickname/
		
### Privacy settings

* Get current privacy settings:

		curl -X GET https://windu.herokuapp.com/api/account/privacy-settings/
		
* Update your privacy settings (status_message, photo, last_seen) possible values `none`, `contacts` and `all` :

		curl -X POST -d "photo=contacts&status_message=all" https://windu.herokuapp.com/api/account/privacy-settings/
		
## Contacts

###Adding/Importing/Removing contacts

* Adding contact:

	**This method is to add a single contact, if you need to add in bulk use `import-contacts` instead.**
	*(Adding a contact will sync all contacts)*


		curl -X POST -d "contact_id=XXXXXX&first_name=John Malkovich"http://windu.herokuapp.com/api/contacts/import-contacts/
		
* Importing contacts:

	**This method will import and replace all your contacts**
	*(Importing will sync all contacts)*


		curl -X POST -d "contact_id=XXXXXX&first_name=John Malkovich" http://windu.herokuapp.com/api/contacts/add-contact/
		
* Updating contacts:

	This method will only update the `first_name` and/or `last_name` no sync will happen.

		curl -X POST -d "contact_id=XXXXXX&first_name=Jon Arbuckle" http://windu.herokuapp.com/api/contacts/add-contact/
		
* Remove contact:

	**This method is to remove a single contact, if you need to remove in bulk use `remove-contacts` instead.**
	*(Removing a contact will sync all contacts)*
	
		curl -X POST -d "contact_id=XXXXXX&first_name=John Malkovich" http://windu.herokuapp.com/api/contacts/<contact-id>/remove-contact
		
	



		

		


		
		
		

		
		
