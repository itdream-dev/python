There are two points we're using in the app now.
One is "silver points" and another one is "gold points".

Here are the api endpoints related with them.

1. Use points
- url: 				account/use_points
- method:			POST
- parameters:		user_id, payment_type, username, email
	user_id: User Id
	payment_type: If you're going to use venmo, this field should be "Venmo" otherewise it could be the card type, for example "Amazon".
	username: This field is valid only when the payment_type is "Venmo". It's just a username of Venmo account.
	email: Email address for card/venmo

- response: 		Updated pont data of user in JSON format
- functionality: 	For now, it sends points info to email.

2. Get points from Venmo
- url: 				account/get_points_from_venmo
- method:			POST
- parameters:		user_id, username, email, amount
	user_id: User Id
	username: This field is valid only when the payment_type is "Venmo".
	email: Email address for Venmo account
	amount: Amount to use for getting points

- response: 		Updated pont data of user in JSON format
- functionality: 	For now, it sends points info to email.