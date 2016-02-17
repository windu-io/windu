# Windu API

![Windu icon](https://pbs.twimg.com/profile_images/613690247495446528/F8NnOJPn_bigger.png)



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
		
* Update connected status to `online` :

		curl -X POST -d "connected_status=online" https://windu.herokuapp.com/api/account/connected-status/
		
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
You need to import or add your contacts before use any **Windu** method that interacts with any contact (photos, messages, groups, status).

###Adding/Importing/Removing/Listing contacts

* Adding contact:

	**This method is to add a single contact, if you need to add in bulk use `import-contacts` instead.**
	*(Adding a contact will sync all contacts)*


		curl -X POST -d "contact_id=XXXXXX&first_name=John Malkovich" http://windu.herokuapp.com/api/contacts/add-contact/
		
* Importing contacts:

	**This method will import and REPLACE ALL your contacts**
	*(Importing will sync all contacts)*

		curl -X POST -H "Content-Type: application/json" https://windu.herokuapp.com/api/contacts/import-contacts/ -d "{\"contacts\":[{\"contact_id\":\"3333333\",\"first_name\":\"John\"},{\"contact_id\":\"11111111\",\"first_name\":\"Tony\",\"last_name\":\"Stark\"},{\"contact_id\":\"22222222\",\"first_name\":\"Hulk\"}]}"
		
	Why no `merge-contacts`?
	
	- Merge is tricky (specially handling the remove), and lead to ghost records, you can do the merge yourself, listing all contacts and them, importing the merged result.
		
* Listing all contacts:

	List all contacts from your account:
	
		curl -X GET http://windu.herokuapp.com/api/contacts/
		
* Show contact info:
	
	Show contact information:

		curl -X GET http://windu.herokuapp.com/api/contacts/<contact-id>/
		
* Updating contacts:

	This method will only update the `first_name` and/or `last_name` no sync will happen.

		curl -X PATCH -d "first_name=Jon Arbuckle" http://windu.herokuapp.com/api/contacts/<contact-id>/
		
* Remove contact:

	**This method is to remove a single contact, if you need to remove in bulk use `remove-contacts` instead.**
	*(Removing a contact will sync all contacts)*
	
		curl -X DELETE http://windu.herokuapp.com/api/contacts/<contact-id>/
		
		
* Remove several contacts:

	*(Removing contacts will sync all contacts)*
	
		curl -X POST -H "Content-Type: application/json" -d "{\"contacts\":[\"XXXXXX\",\"YYYYYY\",\"ZZZZZZZ\"]}" http://windu.herokuapp.com/api/contacts/remove-contacts/
		
###Syncing

* Force syncing your contacts:

	**Your contacts are automatically synced every time you add, remove or import any contact, so you normally DONT'T NEED THIS METHOD. This is just in case you need for some reason force re-sync all contacts:**
	
		curl -X POST http://windu.herokuapp.com/api/contacts/force-sync/
		


---------
#### To perform any operation with contacts, get the status message, connected status, profile photo, sending a message, add to a group, the contact MUST be in your contact list, see above how to import or add a contact 
------


##Status Message, Connected Status and Photo


###Status Message

* Get contact latest status message:

		curl -X GET http://windu.herokuapp.com/api/contacts/<contact-id>/status-message/
		
* Get contact status message history:

		curl -X GET http://windu.herokuapp.com/api/contacts/<contact-id>/status-message-history/
		
* Get all contacts statuses messages:
	
		curl -X GET http://windu.herokuapp.com/api/contacts/statuses-messages/
		

### Connected Status & Last seen

__Contact presence and last seen will only work if YOUR connected status is `online`, otherwise you will get an out of date value.__

* Get contact connected status `online` or `offline`, if the connected status is `offline` this will also return the `last-seen`:

		curl -X GET http://windu.herokuapp.com/api/contacts/<contact-id>/connected-status/
		
* Get connected status from **ALL** your contacts:

		curl -X GET http://windu.herokuapp.com/api/contacts/connected-statuses/
		

### Profile photo

The profile photo method will return the contact photo as `Content-Type` **`image/jpeg`**, to retrieve the photo as url use the methods ended by `-url` sufix.

The profile photo can be retrived as **preview** or **full**. The preview photo will be much smaller and much faster to be retrieved.

* #### Preview photo


* Get contact **preview** profile photo URL:

		curl -X GET http://windu.herokuapp.com/api/contacts/<contact-id>/preview-photo-url/
		
* Get contact **preview** profile photo history URLs:

		curl -X GET http://windu.herokuapp.com/api/contacts/<contact-id>/preview-photo-history-urls/
		
* Get **preview** profile photo URL from **ALL** contacts:

		curl -X GET http://windu.herokuapp.com/api/contacts/preview-photos-urls/
		
* ####Full photo


* Get contact profile photo URL:

		curl -X GET http://windu.herokuapp.com/api/contacts/<contact-id>/photo-url/
		
* Get contact profile photo history URLs:

		curl -X GET http://windu.herokuapp.com/api/contacts/<contact-id>/photo-history-urls/
		
* Get profile photo URLs from **ALL** contacts:

		curl -X GET http://windu.herokuapp.com/api/contacts/photos-urls/
		

###Blocking/Unblocking


* To block a number/contact:

		curl -X POST http://windu.herokuapp.com/api/contacts/<contact-id>/block/
		
* To unblock a number/contact:

		curl -X POST http://windu.herokuapp.com/api/contacts/<contact-id>/unblock/
		
* To get a list of blocked numbers:

		curl -X GET http://windu.herokuapp.com/api/contacts/blocked-list/
		
* Block a list of numbers:
		
	*(This will replace all current blocked numbers)*
	
		curl -X POST -H "Content-Type: application/json" -d "{\"numbers\":[\"XXXXXX\",\"YYYYYY\",\"ZZZZZZZ\"]}" http://windu.herokuapp.com/api/contacts/blocked-list/



##Messages

##Groups
	

		
	



		

		


		
		
		

		
		
