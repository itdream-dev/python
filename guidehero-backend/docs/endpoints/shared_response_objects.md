# Json format of shared models used in many places


## datetime

Always in GMT timezone

Format: %d %b %Y %H:%M:%S

### Example

```
28 Nov 2016 14:47:38
```

## Card


### Fields

 - evaluation_period_status - String(50). Options: ['close', 'open', 'done'] Status of evaluation period.
 - evaluation_start_dt - DateTime (RFC 822). Evaluation period start date.
 - evaluation_end_dt - DateTime (RFC 822). Evaluation period end date.
 - answer_visibility - String(50). Options: ['anyone', 'only_askers']. if card is answer on ask deck, then answer_visibility contains who can view the answer.
 - is_answer - Boolean. if card is child of deck in ask mode, then this field shows if the card is answer or question.
 - creator_info - info about creator. [[user_extended]] Format
 - image_scale - Integer. Exists only for IMAGE card type. Obsolete. Use `scale` field instead.
 - scale - Integer. Valid for VIDEO and IMAGE cards.
 - original_prize_pool - Integer. Silver points of inital prize pool for the card.
 - views_count - Integer. How many times the card was viewed
 - viewed_by_me - Boolean. If user provided, then return if card was viewed by user
 - commented_by_me - Boolean. If user provided, then return if card was commented by
 - won_by_me - Boolean. If user provided, then return if card was won by user
 - winners - List of users who get prize. Additional field is `prize`
 - sponsors - List of users who made contribution. Additional field is `contribution`

### Example

```json
{
   "silver_points":10,
   "description":"",
   "creator":"owner",
   "creator_info": [[user_extended]],
   "updated_at":null,
   "prize_to_join":10,
   "original_prize_pool":10,
   "creator_thumbnail":null,
   "likes":0,
   "asked_users":[list of [[card_related_user]] ],
   "id":"68fe278c-4e8d-496b-9db7-37cb9a52ac68",
   "liked_by_me":false,
   "name":"test_deck",
   "ask_enabled":true,
   "created_at":null,
   "format":"",
   "evaluation_status": 'open',
   "evaluation_start_dt": "29 Nov 2016 14:47:38",
   "evaluation_end_dt": "30 Nov 2016 14:47:38",
   "answer_visibility": "only_askers",
   "scale": 3,
   "image_scale": 3,
   "is_answer": true
   "comments":[

   ],
   "content":null,
   "joined_users":[list of [[join_user]] ],
   "givers": [list of [[card_related_user]] ],
   "published":false,
   "type":"deck",
   "children": [list of [[card]] ],
}
```

## card_related_user

base serialization for user that has relation with card (defined in UserRoleCard)
extended in [[joined_users]]

### Example

```json
{
    "username":"test_user",
    "bio":null,
    "last_name":"",
    "linkedin_headline":null,
    "confirmed_at":null,
    "stripped_email":null,
    "active":true,
    "first_name":"",
    "user_id":"1ad018b7-0341-4a42-8153-acb05a1981a6",
    "source":null,
    "thumbnail_url":null,
    "linkedin_profile":null,
    "email":null
}
```

## joined_users

has the same fields as [[card_related_user]] plus _contribution_ field

### Example

```json
{
    ...
    # the same fields as in [[card_related_user]] format
    ...
    "contribution": 50
}
```

## user_extended

```json
{
    'bio': None,
    'last_name': u'Smith',
    'linkedin_headline': None,
    'confirmed_at': None,
    'stripped_email': None,
    'active': True,
    'first_name': u'John',
    'user_id': u'6fe05ad4-19d4-4f23-b0e3-7efc2985f2a9',
    'source': None,
    'thumbnail_url': None,
    'linkedin_profile': None,
    'username': 'john.smith',
    'email':  'john.sith@example.com'
}
```

## base_user_info

Function: `app.api.auth_api.get_base_user_info`

```json
{
    'id': user.id,
    'email': user.email,
    'stripped_email': user.stripped_email,
    'first_name': user.first_name,
    'last_name': user.last_name,
    'username': user.username,
    'bio': user.bio,

    'thumbnail_url': user.thumbnail_url,
    'linkedin_profile': user.linkedin_profile,
    'linkedin_headline': user.linkedin_headline,

    'active': user.active,
    'confirmed_at': user.confirmed_at,
    'source': user.source,
    'total_silver_points': user.silver_points,
    'tier': user.tier
}
```

## UserProfile

```json
  {
    'user_info': [[shared_response_objects.user_extended]],
    'cards': list of [[shared_response_objects.Card]],
    'stats': {
        'total_likes': Integer, Number of total likes gathered by user.
        'total_followers': Integer, Number of total followers of this user. (Not implemented yet.  Always 113)
        'total_following': Integer, Number of total following by this user. (Not implemented yet.  Always 113)
        'total_shared': Integer, Number of total shared cards created by this user. (Not implemented yet.  Always 113)
        'total_silver_points': Integer, Silver Points balance of user.
    }
    'followers': [[shared_response_objects.user_extended]], # list of user who follow the asked user
    'followings': [[shared_response_objects.user_extended]], # list of user who is followed BY the asked user
  }
```

Response from sigin endpoints

## SigninUserInfo

Response from sigin endpoints

```json
{
    'user': {
        'id': USER_ID,
        'email': EMAIL,
        'stripped_email': STRIPPED_EMAIL,
        'first_name': USER_FIRSTNAME,
        'last_name': USER_LASTNAME,
        'username': USERNAME,
        'bio': BIO,
        'thumbnail_url': THUMBNAIL_URL,
        'linkedin_profile': LINKEDIN_PROFILE,
        'linkedin_headline': LINKEDIN_HEADLINE,
        'active': ACTIVE,
        'confirmed_at': CONFIRMED_AT,
        'source': SOURCE,
    },
    'auth_token': USER_AUTH_TOKEN
}
```
