Structure befor:
```
{
   id: 'CardAID'
   name: 'CardA',
   type: 'card',
   description: 'Description',
   tags: ['tag1']
}
```

Structure after:
```
{
    id: 'NEW ID OF DECK'
    type: 'deck'
    name: 'CardA',
    description: 'Description',
    tags: ['tag1'],

    children: [
        {
            id: 'CardAID',
            name: 'CardA',
            type: 'card',
            description: 'Description',
            tags: ['tag1'],
        }
    ]
}
```
