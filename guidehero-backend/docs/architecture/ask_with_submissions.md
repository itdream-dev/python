Before any submissions
```
{
    'id': 'ask_deck_id',
    'type': 'deck',
    'ask_enabled': true,
    'children': [
        // this is the ask part
        {
            'id': 'ask_container_id'
            'type': 'deck',
            'ask_enabled': false,
            'children': [
                // these are the ask cards
                {
                    'id': 'ask_card_1'
                    'type': 'image'
                }, 
                {
                    'id': 'ask_card_2'
                    'type': 'video'
                }
                
            ]
        }
    ]
}
```
After user A submits a card
```
{
    'id': 'ask_deck_id',
    'type': 'deck',
    'ask_enabled': true,
    'children': [
        // this is the ask part
        {
            'id': 'ask_container_id'
            'type': 'deck',
            'ask_enabled': false,
            'children': [
                // these are the ask cards
                {
                    'id': 'ask_card_1'
                    'type': 'image'
                }, 
                {
                    'id': 'ask_card_2'
                    'type': 'video'
                }
                
            ]
        },
        // anything bellow will be submissions
        {
            'id': 'user_a_submissions_container',
            'type': 'deck',
            'children': [
                {
                    'id': 'submission_card_a_1'
                    'type': 'image'
                }
            ]
        }
    ]
}
```

After user B submits a card
```
{
    'id': 'ask_deck_id',
    'type': 'deck',
    'ask_enabled': true,
    'children': [
        // this is the ask part
        {
            'id': 'ask_container_id'
            'type': 'deck',
            'ask_enabled': false,
            'children': [
                // these are the ask cards
                {
                    'id': 'ask_card_1'
                    'type': 'image'
                }, 
                {
                    'id': 'ask_card_2'
                    'type': 'video'
                }
                
            ]
        },
        // anything bellow will be submissions
        {
            'id': 'user_a_submissions_container',
            'type': 'deck',
            'children': [
                {
                    'id': 'submission_card_a_1'
                    'type': 'image'
                }
            ]
        },
        {
            'id': 'user_b_submissions_container',
            'type': 'deck',
            'children': [
                {
                    'id': 'submission_card_b_1'
                    'type': 'image'
                }
            ]
        }
    ]
}
```

After user A submits another card
```
{
    'id': 'ask_deck_id',
    'type': 'deck',
    'ask_enabled': true,
    'children': [
        // this is the ask part
        {
            'id': 'ask_container_id'
            'type': 'deck',
            'ask_enabled': false,
            'children': [
                // these are the ask cards
                {
                    'id': 'ask_card_1'
                    'type': 'image'
                }, 
                {
                    'id': 'ask_card_2'
                    'type': 'video'
                }
                
            ]
        },
        // anything bellow will be submissions
        {
            'id': 'user_a_submissions_container',
            'type': 'deck',
            'children': [
                {
                    'id': 'submission_card_a_1'
                    'type': 'image'
                },
                {
                    'id': 'submission_card_a_2'
                    'type': 'video'
                }
            ]
        },
        {
            'id': 'user_b_submissions_container',
            'type': 'deck',
            'children': [
                {
                    'id': 'submission_card_b_1'
                    'type': 'image'
                }
            ]
        }
    ]
}
```
