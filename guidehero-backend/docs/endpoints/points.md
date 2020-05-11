# Points Endpoints

Links to another file has format: *[[filename.ParagraphId]]*, for example: *[[shared_response_objects.Card]]* - means, 
look paragraph _Card_ inside file _/docs/endpoints/shared_response_objects.md_


## transfer

Transfer points from/to card or user

 - URL: /api/v1/points/transfer
 - method: POST

### Arguments
 - transaction_type - String. Options ['send_to_friend', 'verify_with_facebook']. Type of transaction.

 Depending from tranaction type, The endpoint accepts different arguments:

#### send_to_friend
 - user_from - String. Required. ID of the sender.
 - user_to - String. Required. ID of the recipient.
 - silver_points - Integer. Required. Silver points to transfer.

#### verify_with_*
 - user_to - String. Required. ID of the user
 - transaction_type - String. Required. Options: ['verify_with_facebook'].
 

### Success Response

 - Code: 200
 - Content:
```json
  {
  }
```
