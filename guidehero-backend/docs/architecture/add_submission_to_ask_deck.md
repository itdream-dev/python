Initialy we have ask deck with another deck inside for questions and one question.

```
ask_deck
    deck_question
        question1
```

When we add  submission1 to the ask_deck:
```
ask_deck
    deck_questions
        question1
    submission1
```

## in tests:

#### Initial
```
[
    {
        'type': 'ask', 'id':  'Ask1', 'name': 'Ask_name',
        'children': [
            {'type': 'deck', 'id': 'QUESTION-COLLECTION',
                'children': [
                    {'id': 'Question1', 'name': 'Question1'}
                ]
            },
        ]
    },
    {'id': 'Submission1', 'name': 'Submission1'}
]
```

### Action

url: /api/v1/deck/give_card_to_deck
data: {
    'deck_id': 'Ask1',
    'card_id': 'Submission1'
}

### Final

```
[
{
    'type': 'ask', 'id':  'Ask1', 'name': 'Ask_name',
    'children': [
        {'type': 'deck', 'id': 'QUESTION-COLLECTION',
            'children': [
                {'id': 'Question1', 'name': 'Question1'}
            ]
        },
        {'id': 'Submission1', 'name': 'Submission1'},
    ]
}
]
```
