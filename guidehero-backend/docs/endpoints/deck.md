# Deck Endpoints

Links to another file has format: *[[filename.ParagraphId]]*, for example: *[[shared_response_objects.Card]]* - means, 
look paragraph _Card_ inside file _/docs/endpoints/shared_response_objects.md_

## add_mode
 - Url: /api/v1/deck/add_mode
 - method: POST

### Arguments
  - deck_id - integer. deck or card id where we want to enable ask mode
  - format - string. Accepted answers format decription
  - is_ask_mode_enabled - boolean. Enable or Disable ask mode
  - asked_user_ids - list of integers. Users has been asked to answer on the question.
  - initial_prize - Integer. Optional. Default=0. Initial prize for solve ask
  - prize_to_join - Integer. Optional. Default=0. Prize added to deck prize pool when new user join to ask
  - distibution_rule - Enum String(50). Optional. Default='proportinaolly'. options=['evenly', 'proportionally']. Define rule how to distribute prize among givers
  - distributtion_for - Intenger. Optional. Default=None. Number of top givers where prize will be distributed between
  - evaluation_start_dt - Datetime (format: [[shared_response_objects.Card]]). Optional. Default=None. Start of the evaluation period where we accept answers from givers. Example: "29 Nov 2016 14:47:38"
  - evaluation_end_dt - Datetime (format: [[shared_response_objects.Card]]). Optional. Default=None. End of the evaluation period where we accept answers from givers. Example: "29 Nov 2016 14:47:38"

### Success Response

| Code | Content |
|--- | --- |
| 200 | {result: "success", "deck": [[shared_response_objects.Card]]} |

### Error Response

| Code | Content |
|--- | --- |
| 400 | {error: ERROR_DESCRIPTION} |

### Comments
if deck_id point to the card. We create new deck and add the card as first child of new deck. deck_id is id of new deck in the response


## join_ask

Add current user to the deck as asker

 - URL: /api/vi/deck/join_ask
 - method: POST

### Arguments
 - deck_id - integer. Required. Deck id in ask mode.
 - custom_join_prize - integer. Optional. Default is _prize_to_join_ of the Deck id in ask mode. _custom_join_prize_ can not be less than _prize_to_join_ of the deck

### Success Response

| Code | Content |
|--- | --- |
| 200 | {result: "success", "deck": [[shared_response_objects.Card]]} |

### Error Response

| Code | Content |
|--- | --- |
| 400 | {error: ERROR_DESCRIPTION} |

### Example

#### Request
```
{'deck_id': u'd92bbea6-860c-41b2-8a33-0e8209a6e068'}
```

#### Response
 - Code: 200
 - Content:
```
{"result": "success", "deck": [[shared_response_objects.Card]]}
```

## unjoin_ask

Remove current user to the deck as asker

 - URL: /api/vi/deck/unjoin_ask
 - method: POST

### Arguments
 - deck_id - integer. Required. Deck id in ask mode.

### Success Response

| Code | Content |
|--- | --- |
| 200 | {result: "success", "deck": [[shared_response_objects.Card]]} |

### Error Response

| Code | Content |
|--- | --- |
| 400 | {error: ERROR_DESCRIPTION} |

### Example

#### Request
```
{'deck_id': u'd92bbea6-860c-41b2-8a33-0e8209a6e068'}
```

#### Response
 - Code: 200
 - Content:
```
{result: "success", "deck": [[shared_response_objects.Card]]}
```

## give_card_to_deck

Add card as answert to the deck in ask mode.

 - URL: /api/vi/deck/give_card_to_deck
 - method: POST

### Arguments
 - deck_id - integer. Required. Deck id in ask mode.
 - card_id - integer. Required. Card that should be added to the deck as answer.
 - visibility - String(50). Optional. Default: 'anyone'. Options: ['anyone', 'only_askers']. Set answer visibility.  Card that should be added to the deck as answer.

### Success Response

| Code | Content |
|--- | --- |
| 200 | {result: "success", "deck": [[shared_response_objects.Card]]} |

### Error Response

| Code | Content |
|--- | --- |
| 400 | {error: ERROR_DESCRIPTION} |

### Example

#### Request
```
{'deck_id': u'd92bbea6-860c-41b2-8a33-0e8209a6e068', 'card_id': u'ef45bea6-860c-41b2-8a33-0e8209a6e329'}
```

#### Response
 - Code: 200
 - Content:
```
{result: "success", "deck": [[shared_response_objects.Card]]}
```

## revoke_card_from_deck

Revoke answer from the deck

 - URL: /api/vi/deck/revoke_card_from_deck
 - method: POST

### Arguments
 - card_id - integer. Required. Card that should be revoked from ask deck.

### Success Response

| Code | Content |
|--- | --- |
| 200 | {"deck": [[shared_response_objects.Card]]} |

### Error Response

| Code | Content |
|--- | --- |
| 400 | {error: ERROR_DESCRIPTION} |

### Example

#### Request
```
{'card_id': u'ef45bea6-860c-41b2-8a33-0e8209a6e329'}
```

#### Response
 - Code: 200
 - Content:
```
{"deck": [[shared_response_objects.Card]]}
```

## end_evaluation_period

Ends evaluation period for deck (set _evaluation_period_status_ to 'done') and distribte prize pool according to _distribution_rule_ and _distribution_for_ values

 - URL: /api/vi/deck/end_evaluation_period
 - method: POST

### Arguments
 - deck_id - integer. Required. Deck id in ask mode.

### Success Response

| Code | Content |
|--- | --- |
| 200 | {"deck": [[shared_response_objects.Card]]} |

### Error Response

| Code | Content |
|--- | --- |
| 400 | {error: ERROR_DESCRIPTION} |

### Example

#### Request
```
{'deck_id': u'd92bbea6-860c-41b2-8a33-0e8209a6e068'}
```

#### Response
 - Code: 200
 - Content:
```
{"deck": [[shared_response_objects.Card]]}
```

## get_winners

Returns winners list for deck

 - URL: /api/vi/deck/get_winners
 - method: GET

### Arguments
 - deck_id - integer. Required. Deck id in ask mode.

### Success Response


 - Code: 200
 - Content:
```json
{
    'total_likes': 100,
    'winnners': [
        {
            [[shared_response_objects.user_extended]],
            'prize': 100,
            'likes': 10,
            'likes_percent': 45
        },
        {
            ....
        }
    ]
}

```

## get_sponsors

Returns winners list for deck

 - URL: /api/vi/deck/get_sponsors
 - method: GET

### Arguments
 - deck_id - integer. Required. Deck id in ask mode.

### Success Response


 - Code: 200
 - Content:
```json
{
    'sponsors': [
        {
            [[shared_response_objects.user_extended]],
            'contribution': 100,
        },
        {
            ....
        }
    ]
}

```

## create_deck

Create new deck

 - URL: /api/vi/deck/create_deck
 - method: POST

### Arguments
 - deck_title - String. Title of the deck
 - card_ids - List of String. Ids of children card of new deck
 - is_ask_mode_enabled - Boolean. If ask mode should be enabled for new deck
 - format - String. Define deck format is ask mode is enabled
 - tags - List of String. Name of tags for deck.

### Success Response

 - Code: 200
 - Content:
```json
{'result': 'success'}

```

## create_image_card

Create new image card

 - URL: /api/vi/deck/create_image_card
 - method: POST

### Arguments
 - card_title - String. Title of the deck
 - card_description - String. Description
 - s3_file_name - String. Name of image on s3
 - image_x - Integer. 
 - image_y - Integer
 - image_width - Integer. Witdth of the image.
 - image_height - Integer. Height of the image
 - tags - List of String. Name of tags for deck.
 - image_scale - Integer. Default=None, Scale of the image (eg. 0, 1, 2, 3, ..).

### Success Response

 - Code: 200
 - Content:
```json
{'result': 'success'}

```

## edit_image_card

Edit new image card

 - URL: /api/vi/deck/edit_image_card
 - method: POST

### Arguments
 - card_id - String. Id of the card to edit.
 - card_title - String. Title of the deck
 - card_description - String. Description
 - s3_file_name - String. Name of image on s3
 - image_x - Integer. 
 - image_y - Integer
 - image_width - Integer. Witdth of the image.
 - image_height - Integer. Height of the image
 - tags - List of String. Name of tags for deck.
 - image_scale - Integer. Default=None, Scale of the image (eg. 0, 1, 2, 3, ..).
 - scale - Integer. Default=None, Scale of the image (eg. 0, 1, 2, 3, ..). 

### Success Response

 - Code: 200
 - Content:
```json
[[shared_response_objects.Card]]
```

## edit_video_card

Edit new video card

 - URL: /api/vi/deck/edit_video_card
 - method: POST

### Arguments
 - card_id - String. Id of the card to edit.
 - card_title - String. Title of the deck
 - card_description - String. Description
 - s3_file_name - String. Name of video on s3
 - thumbnail_url - String. Url to the thumbnail
 - tags - List of String. Name of tags for deck.
 - scale - Integer. Default=None, Scale of the video (eg. 0, 1, 2, 3, ..). 

### Success Response

 - Code: 200
 - Content:
```json
[[shared_response_objects.Card]]
```

## create_text_card

Create new text card

 - URL: /api/vi/deck/create_text_card
 - method: POST

### Arguments
 - card_title - String. Title of the deck
 - language - String. Language of pronunciation
 - card_content - String. Content of the card
 - card_description - String. Description
 - tags - List of String. Name of tags for deck.

### Success Response

 - Code: 200
 - Content:
```json
{'result': 'success'}

```

## edit_deck

Edit deck

 - URL: /api/vi/deck/edit_deck
 - method: POST

### Arguments
 - deck_id - String. ID of deck for editing
 - card_ids - List of String. List of children for deck
 - tags - List of String. Name of tags for deck.

### Success Response

 - Code: 200
 - Content:
```json
{'result': 'success'}

```


## generate_video_upload_params

Generating params necessary to upload videos to s3

 - URL: /api/vi/deck/generate_video_upload_params
 - method: POST

### Arguments
 - file_name - file name of the video eg "02adf23482.mp4"

### Success Response

 - Code: 200
 - Content:
```json
{
    "result": {
        "bucket_name": "ivysaur-development-video",
        "fields": {
            "AWSAccessKeyId": "AKIAINEDUQ2PHQEBEV7Q",
            "key": "dd015381-c048-4e6d-b251-a697bd8c7bbd-02adf23482.mp4",
            "policy": "eyJjb25kaXRpb25zIjogW3siYnVja2V0IjogIml2eXNhdXItZGV2ZWxvcG1lbnQtdmlkZW8ifSwgeyJrZXkiOiAiZGQwMTUzODEtYzA0OC00ZTZkLWIyNTEtYTY5N2JkOGM3YmJkLXlvaGVpLm1wNCJ9XSwgImV4cGlyYXRpb24iOiAiMjAxNi0xMi0xMlQwNjo0MTo0MFoifQ==",
            "signature": "+cYE1UoXYamMu5NagPTkjJyN7Fg="
        },
        "url": "https://ivysaur-development-video.s3.amazonaws.com/"
    }
}
```


## create_video_card

Create new video card

 - URL: /api/vi/deck/create_video_card
 - method: POST

### Arguments
 - card_title - String. Title of the deck
 - card_description - String. Description
 - s3_file_name - String. Name of video on s3
 - scale - Integer. Scale of video
 

### Success Response

 - Code: 200
 - Content:
```json
{'result': 'success'}

```

## like_comment

Add like to comment from current user

 - URL: /api/vi/deck/like_comment
 - method: POST

### Arguments
 - comment_id - String. id of the comment

### Success Response

 - Code: 200
 - Content:
```json
{}
```

## unlike_comment

Add like to comment from current user

 - URL: /api/vi/deck/unlike_comment
 - method: POST

### Arguments
 - comment_id - String. id of the comment

### Success Response

 - Code: 200
 - Content:
```json
{}
```

## view_card

Add 1 to card view counter

 - URL: /api/vi/deck/view_card
 - method: POST

### Arguments
 - card_id - String. id of the card

### Success Response

 - Code: 200
 - Content:
```json
{}
```

## move_card

Move card to or from deck

 - URL: /api/v1/deck/move_card
 - method: POST

### Arguments
 - card_ids - List of String. Required. ids of cards that user wants to move.
 - move_to - String. Optional. Id of deck where user wants to move cards to.

### Comments

 - card for moving and destination deck must belong to current user
 - if move_to is not provided. Then cards will be detached from their current deck.


### Success Response

 - Code: 200
 - Content:
```json
| 200 | {result: "success"} |
```

## copy_card

Create copy of the card

 - URL: /api/v1/deck/copy_card
 - method: POST

### Arguments
 - card_id - Card to be copied

### Returns
 new card json object

### Comments

list of fields to copy:

'type',
'name',
'content',
'sub_content',
'language',
'pronunciation',
'published',
'description',
'creator',
'x_position',
'y_position',
'height',
'width',
'scale',
'silver_points',
'original_prize_pool',
'gold_points',
'prize_to_join',
'answer_visibility',
'liked_users',
'comments',
'is_ask_mode_enabled',
'format',
'distribution_rule',
'distribution_for',
'evaluation_start_dt',
'evaluation_end_dt',
'evaluation_period_status',
'is_answer',
'tags',
'video_length',

### Success Response

 - Code: 200
 - Content:
```json
| 200 | [[shared_response_objects.Card]] |
```

## convert_card_to_deck

Convert card to deck

 - URL: /api/v1/deck/convert_card_to_dict
 - method: POST

### Arguments
 - card_id - Id of the card to be converted in deck

### Comments
 - Card must belong to current user.
 - Card must be not deck

Structure befor:
```
{
   id: 'CardAID'
   name: 'CardA',
   type: 'card'
}
```

Structure after:
```
{
    id: 'NEW ID OF DECK'
    type: 'deck'
    name: 'CardA',
    children: [
        {
            id: 'CardAID'
            name: 'CardA'
            type: 'card'
        }
    ]
}
```

### Return
   
   Json object of new deck

### Success Response

 - Code: 200
 - Content:
```json
| 200 | [[shared_response_objects.Card]] |
```

## change_order

Move card to or from deck

 - URL: /api/v1/deck/change_order
 - method: POST

### Arguments
 - card_id - String. Required. The id of card that we want to change order
 - position - Integer. Required. New position of card inside deck.

### Restriction

 - Card must belongs to unpublished deck and to current user

### Success Response

 - Code: 200
```json
| 200 | {"result": "success"} |
```

### Error Response

 - Code: 400
 - Content:
```json
| 400 | {"result": "error", "message": "Description of error if available"} |
```

### Example

##### Success

######  Request
```json
{"card_id": "486dd66a-811a-421a-92b7-13e346eed3d8", "position": "1"}
```

###### Response
```json
{"result": "success"}
```
