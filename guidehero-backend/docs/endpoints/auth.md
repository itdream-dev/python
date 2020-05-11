# Auth Endpoints

*linkedin_signin*, *fb_signin*, *google_signin* endpoints returns user and auth_token data. 

### Example of response
```
{
    u'auth_token': u'.....', 
    u'user': {
        u'username': u'test',
        u'bio': None,
        u'first_name': u'',
        u'last_name': u'',
        u'linkedin_headline': None,
        u'source': None,
        u'confirmed_at': None,
        u'stripped_email': None,
        u'email': u'test@test.com',
        u'linkedin_profile': None,
        u'thumbnail_url': None,
        u'active': None,
        u'id': u'1be8a09c-5e3f-4544-b600-88bfb6e1babd',
        u'total_silver_points': 41
    }
}
```

## sigin

ONLY FOR TESTING AND DEBUGGING. WORKS ONLY IF DEBUG IS TRUE

 - Url: /api/v1/auth/sigin
 - method: POST

### Arguments
  - email - String. email of the user

### Success Response

| Code | Content |
|--- | --- |
| 200 | [[shared_response_objects.SigninUserInfoh|


## get_user_info

 - Url: /api/v1/auth/get_user_info
 - method: POST

### Arguments
  - user_id - String. Optional. Id if the user. If user_id is not provided, then current user is used.
  - fields - Comma separated list of String. Optional.  List of additional info for user. Options: wins,asks,gives,likes,published
    - wins - gives list of ask deck, won by user. List of [[shared_response_objects.Card]]
    - asks - list of ask deck where user joined to ask. List of [[shared_response_objects.Card]]
    - gives - list of ask deck where user gave his answer. List of [[shared_response_objects.Card]]
    - likes -list of cards liked by user. List of [[shared_response_objects.Card]]
    - published -list of cards published by user. List of [[shared_response_objects.Card]]

### Success Response

| Code | Content |
|--- | --- |
| 200 | [[shared_response_objects.base_user_info]] + additional fields depending from fields argument |

## edit_user

    Edit current user info

 - Url: /api/v1/auth/edit_user
 - method: POST

### Arguments
  - username - String. 
  - first_name - String. 
  - last_name - String. 
  - bio - String. 

### Success Response

| Code | Content |
|--- | --- |
| 200 | [[shared_response_objects.base_user_info]] |
