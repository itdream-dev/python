# Account Endpoints

Links to another file has format: *[[filename.ParagraphId]]*, for example: *[[shared_response_objects.Card]]* - means, 
look paragraph _Card_ inside file _/docs/endpoints/shared_response_objects.md_


## get_profile

Return base info, cards and statistics for user
Add current user to the deck as asker

 - URL: /api/v1/account/get_profile
 - method: POST

### Arguments
 - user_id - String. Required. ID of the user

### Success Response

 - Code: 200
 - Content: [[shared_response_objects.UserProfile]]

### Error Response

| Code | Content |
|--- | --- |
| 400 | {error: ERROR_DESCRIPTION} |


## get_points

Returns statistics about user points

 - URL: /api/v1/account/get_points
 - method: POST

### Arguments
 - user_id - String. Required. ID of the user

### Success Response

 - Code: 200
 - Content:
```json
{
    'total_points': 113,
    'cumulative_earnings': 113,
    'points_purchased': 113,
    'points_used': 113,
    'use_points': [
        {'id': 'donate_to_charity', 'name': 'Donate to charity'},
        {'id': 'donate_to_category', 'name': 'Donate to a category'},
        {'id': 'send_to_friend', 'name': 'Send to a friend'},
        {'id': 'convert_to_venmo_credit', 'name': 'Convert to  Venmo credit'},
        {'id': 'convert_to_amazon_gift_card', 'name': 'Convert to Amazon Gift card'},
        {'id': 'convert_to_starbucks_gift_card', 'name': 'Convert to Starbucks Gift card'},
    ],
    'get_points': [
        {'id': 'use_promo_code', 'name': 'Use Promo/Gift code'},
        {'id': '0.99', 'name': '$ 0.99', 'silver_points': 100},
        {'id': '4.99', 'name': '$ 4.99', 'silver_points': 550},
        {'id': '9.99', 'name': '$ 9.99', 'silver_points': 1200},
        {'id': 'verify_with_facebook', 'name': 'Verify with Facebook', 'silver_points': 25},
        {'id': 'verify_with_twitter', 'name': 'Verify with Twitter', 'silver_points': 25},
        {'id': 'verify_with_linkedin', 'name': 'Verify with LinkedIn', 'silver_points': 25},
        {'id': 'verify_with_instagram', 'name': 'Verify with Instagram', 'silver_points': 25},
        {'id': 'invite_3_friends', 'name': 'Invite 3 friends', 'silver_points': 50},
        {'id': 'invite_10_friends', 'name': 'Invite 10 friends', 'silver_points': 50},
        {'id': 'invite_30_friends', 'name': 'Invite 30 friends', 'silver_points': 100},
        {'id': 'first_time_prize_bonus', 'name': 'First time prize bonus', 'silver_points': 500},
    ]
}
```

### Error Response

| Code | Content |
|--- | --- |
| 400 | {error: ERROR_DESCRIPTION} |


## does_user_exist

    Check if user with specific user name exists

 - Url: /api/v1/auth/does_user_exist
 - method: POST

### Arguments
  - username - String. 

### Success Response

| Code | Content |
|--- | --- |
| 200 | {"result": true} or {"result": false} |


## follow_user

    Register current user as follower of another user

 - Url: /api/v1/auth/follow_user
 - method: POST

### Arguments
  - following_id - String. The id if the user, that the current user wants to follow (becomes his follower).

### Success Response

 - Code: 200 OK
 - Content:
```json
{
    "following": [[shared_response_objects.UserProfile]] # profile of following user
    "follower": [[shared_response_objects.UserProfile]] # profile of follower user
```


## unfollow_user

    Unregister current user as follower of another user

 - Url: /api/v1/auth/unfollow_user
 - method: POST

### Arguments
  - following_id - String. The id if the user, that the current user don't want to follow.

### Success Response

 - Code: 200 OK
 - Content:
```json
{
    "following": [[shared_response_objects.UserProfile]] # profile of following user
    "follower": [[shared_response_objects.UserProfile]] # profile of follower user
```
