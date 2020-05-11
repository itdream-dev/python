Initialy we have ask deck with another deck inside for questions and one question and one submission as child of ask deck.

```
ask_deck
    deck_question
        question1
    submission1
```

When we add another submission to the ask_deck, we create new deck for submissions and add submission1 and new submission there,
the structure becomes:
```
ask_deck
    deck_questions
        question1
    deck_answers
        submission1
        submission2
```

## in tests:

### Initial:

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
            {'id': 'Submission1', 'name': 'Submission1'}
        ]
    },
    {'id': 'Submission2', 'name': 'Submission2'}
]
```

### Command

- url: /api/v1/deck/give_card_to_deck
- data:
```
{
    'deck_id': 'Ask1',
    'card_id': 'Submission2'
}
```

### Result

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
        {'type': 'deck', is_answer=True,
            'children': [
                {'id': 'Submission1', 'name': 'Submission1'},
                {'id': 'Submission2', 'name': 'Submission2'}
            ]
        },
    ]
}
]
```
