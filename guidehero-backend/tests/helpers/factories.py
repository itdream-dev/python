import uuid
from collections import namedtuple
import mock
import factory
import flask
from lib.models import card
from lib.models import user
from lib.models import card_likes
from lib.models import user_role_card
from lib.models import card_role
from lib.registry import get_registry
from lib.models import tag
from lib.models import transfer
from lib.models import card_comments
from lib.models import comment_like


def assertObjects(testcase, obj1, obj2, fields):
    testcase.assertEqual(
        type(obj1),
        type(obj2),
        'Type is not the same: {} != {}'.format(type(obj1), type(obj2))
    )
    for name in fields:
        testcase.assertEqual(
            getattr(obj1, name),
            getattr(obj2, name),
            'Attribute {} is not same:\n {} != {}'.format(name, getattr(obj1, name), getattr(obj2, name))
        )


def assertList(testcase, l1, l2, msg=None):
    testcase.assertEqual(len(l1), len(l2), 'Size of list is not the same {} !={}'.format(len(l1), len(l2)))
    for idx, it1 in enumerate(l1):
        it2 = l2[idx]
        testcase.assertEqual(it1, it2)


def get_assert_list(testcase):
    def assertList(l1, l2, msg=None):
        testcase.assertEqual(len(l1), len(l2), 'Size of list is not the same {} !={}'.format(len(l1), len(l2)))
        for idx, it1 in enumerate(l1):
            it2 = l2[idx]
            testcase.assertEqual(it1, it2)
    return assertList


class FactoryPlus(factory.alchemy.SQLAlchemyModelFactory):
    @classmethod
    def register_assert(cls, testcase):
        model_class = cls._meta.model
        testcase.addTypeEqualityFunc(model_class, cls.get_assert(testcase))

    @classmethod
    def get_assert(cls, testcase):
        def assert_func(it1, it2, msg=None):
            cls.assert_items(cls, testcase, it1, it2, msg=msg)
        return assert_func

    @classmethod
    def assert_items(cls, testcase, it1, it2, msg=None):
        testcase.assertEqual(it1, it2)

    @classmethod
    def get(cls, *args, **kwargs):
        model_class = cls._meta.model
        if args:
            return model_class.query.get(*args)
        if kwargs:
            q = model_class.query
            for key, value in kwargs.items():
                q = q.filter(getattr(model_class, key) == value)
            return list(q)
        return list(model_class.query.all())


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = user.User
        sqlalchemy_session = get_registry()['DB'].session
    id = factory.Sequence(lambda n: str(uuid.uuid4()))
    username = factory.Sequence(lambda n: 'username_{}'.format(n))
    silver_points = 0
    tier = ''
    first_name = ''
    last_name = ''
    bio = ''

    @classmethod
    def get(cls, *args, **kwargs):
        if args:
            return user.User.query.get(*args)
        email = kwargs.pop('email')
        if email is not None:
            return user.User.query.filter(user.User.email == email).first()

    @classmethod
    def register_assert(cls, testcase):
        testcase.addTypeEqualityFunc(user.User, cls.get_assert(testcase))

    @classmethod
    def get_assert(cls, testcase):
        def assert_func(it1, it2, msg=None):
            assertObjects(testcase, it1, it2, ['id', 'silver_points', 'username', 'first_name', 'last_name', 'bio'])
        return assert_func


class CardFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = card.Card
        sqlalchemy_session = get_registry()['DB'].session
    id = factory.Sequence(lambda n: str(uuid.uuid4()))
    type = card.Card.TEXT
    is_ask_mode_enabled = False
    creator = factory.SubFactory(UserFactory)
    description = ''

    tags = []
    tag_names = []

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        tag_names = kwargs.pop('tag_names')
        if tag_names:
            kwargs['tags'] = [Tag.build(name=name) for name in tag_names]
        return kwargs

    @classmethod
    def create(cls, likes=0, *args, **kwargs):
        card = super(CardFactory, cls).create(*args, **kwargs)
        for _ in range(likes):
            CardLikesFactory(card=card)
        return card

    @classmethod
    def get(cls, *args, **kwargs):
        if args:
            return card.Card.query.get(*args)

    @classmethod
    def register_assert(cls, testcase):
        testcase.addTypeEqualityFunc(card.Card, cls.get_assert(testcase))
        Tag.register_assert(testcase)

    @classmethod
    def get_assert(cls, testcase):
        def assert_func(it1, it2, msg=None):
            assertList(testcase, it1.tags, it2.tags)
            return assertObjects(
                testcase,
                it1,
                it2,
                (
                    'name', 'content', 'sub_content', 'description', 'x_position', 'y_position',
                    'width', 'height', 'scale', 'position', 'parent_id'
                )
            )
        return assert_func


class ImageCardFactory(CardFactory):
    type = card.Card.IMAGE


class DeckFactory(CardFactory):
    type = card.Card.DECK


class AskDeckFactory(DeckFactory):
    type = card.Card.DECK
    is_ask_mode_enabled = True

    @classmethod
    def create(cls, question=None, answers=None, *args, **kwargs):
        card = super(AskDeckFactory, cls).create(*args, **kwargs)
        if question:
            question.is_answer = False
            card.cards.append(question)
        if answers:
            for answer in answers:
                answer.is_answer = True
                card.cards.append(answer)
        return card


class CardLikesFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = card_likes.CardLikes
        sqlalchemy_session = get_registry()['DB'].session

    user = factory.SubFactory(UserFactory)
    card = factory.SubFactory(CardFactory)


class UserRoleCard(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = user_role_card.UserRoleCard
        sqlalchemy_session = get_registry()['DB'].session

    user = factory.SubFactory(UserFactory)
    card = factory.SubFactory(CardFactory)
    role_id = card_role.CardRole.JOINED


class Tag(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = tag.Tag
        sqlalchemy_session = get_registry()['DB'].session
    name = factory.Sequence(lambda n: 'tag_{}'.format(n))

    @classmethod
    def register_assert(cls, testcase):
        testcase.addTypeEqualityFunc(tag.Tag, cls.get_assert(testcase))

    @classmethod
    def get_assert(cls, testcase):
        def assert_func(it1, it2, msg=None):
            return assertObjects(testcase, it1, it2, ['name'])
        return assert_func


class Transfer(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = transfer.Transfer
        sqlalchemy_session = get_registry()['DB'].session
    id = factory.Sequence(lambda n: str(uuid.uuid4()))
    user_from = None
    user_to = None
    silver_points = 0
    transaction_type = 'send_to_friend'

    @classmethod
    def get(cls, *args, **kwargs):
        if args:
            return transfer.Transfer.query.get(*args)
        if kwargs:
            q = transfer.Transfer.query
            for key, value in kwargs.items():
                q = q.filter(getattr(transfer.Transfer, key) == value)
            return list(q)
        return list(transfer.Transfer.query.all())

    @classmethod
    def register_assert(cls, testcase):
        testcase.addTypeEqualityFunc(transfer.Transfer, cls.get_assert(testcase))

    @classmethod
    def get_assert(cls, testcase):
        def assert_func(it1, it2, msg=None):
            testcase.assertEqual(it1.id, it2.id)
            testcase.assertEqual(it1.user_from, it2.user_from)
            testcase.assertEqual(it1.card_from, it2.card_from)
            testcase.assertEqual(it1.user_to, it2.user_to)
            testcase.assertEqual(it1.card_to, it2.card_to)
            testcase.assertEqual(it1.silver_points, it2.silver_points)
            testcase.assertEqual(it1.transaction_type, it2.transaction_type)
        return assert_func


class Comment(FactoryPlus):
    class Meta:
        model = card_comments.CardComments
        sqlalchemy_session = get_registry()['DB'].session
    id = factory.Sequence(lambda n: str(uuid.uuid4()))
    user = factory.SubFactory(UserFactory)
    card = factory.SubFactory(CardFactory)
    content = 'This is card comment'

    @classmethod
    def assert_items(cls, testcase, it1, it2, msg=None):
        testcase.assertEqual(it1.content, it2.content)
        if it1.user:
            testcase.assertEqual(it1.user.id, it2.user.id)
        if it1.card:
            testcase.assertEqual(it1.card.id, it2.card.id)


class CommentLike(FactoryPlus):
    class Meta:
        model = comment_like.CommentLike
        sqlalchemy_session = get_registry()['DB'].session
    user = factory.SubFactory(UserFactory)
    comment = factory.SubFactory(Comment)

    @classmethod
    def assert_items(cls, testcase, it1, it2, msg=None):
        testcase.assertEqual(it1.id, it2.id)
        testcase.assertEqual(it1.user.id, it2.user.id)
        testcase.assertEqual(it1.comment.id, it2.comment.id)


class NamedTupleFactory(factory.Factory):
    class Meta:
        model = object

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        members = [key for key in kwargs]
        class_name = '_'.join(members)
        model_class = namedtuple(class_name, members)
        obj = super(NamedTupleFactory, cls)._create(model_class, *args, **kwargs)
        return obj


class TransferTypeRepository(object):
    def __init__(self):
        self.__types = []
        self.m = None

    def __getitem__(self, name):
        for tt in self.__types:
            if tt.code == name:
                return tt

    def __enter__(self):
        self.m = mock.patch('lib.models.transfer.TYPES', new=self)
        self.m.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.m.stop()

    def create(self, *args, **kwargs):
        tt = TransferType(*args, **kwargs)
        self.__types.append(tt)
        return tt


class TransferType(factory.Factory):
    class Meta:
        model = transfer.TransferTypeBase
    code = 'send_to_friend'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        def exit():
            raise NotImplementedError()
        obj = transfer.TransferTypeWithSilverPoints(code=kwargs['code'], silver_points=kwargs['silver_points'])
        setattr(obj, '__exit__', exit)
        return obj


class ApiRequestEnvironmentFactory(factory.Factory):
    class Meta:
        model = dict

    path = None
    query_string = None
    method = 'POST'
    content_type = 'application/json'
    data = None

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        data = kwargs.pop('data')
        kwargs['data'] = flask.json.dumps(data)
        return kwargs


class JsonResponseFactory(factory.Factory):
    class Meta:
        model = flask.Response
    response = None
    status = '200 OK'
    data = {}

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        data = kwargs.pop('data')
        kwargs['response'] = flask.json.dumps(data)
        return kwargs

    @classmethod
    def register_assert(cls, testcase):
        testcase.addTypeEqualityFunc(flask.Response, cls.get_assert(testcase))

    @classmethod
    def get_assert(cls, testcase):
        def assert_func(it1, it2, msg=None):
            testcase.assertEqual(it1.status, it2.status)
            data1 = flask.json.loads(it1.data)
            data2 = flask.json.loads(it2.data)
            testcase.assertEqual(data1, data2)
        return assert_func


class JsonResponseWithResultStatusFactory(factory.Factory):
    class Meta:
        model = flask.Response
    response = None
    status = '200 OK'
    data = {'result': 'success'}
    extra_data = {}

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        data = kwargs.pop('data')
        data.update(kwargs.pop('extra_data'))
        kwargs['response'] = flask.json.dumps(data)
        return kwargs

    @classmethod
    def register_assert(cls, testcase):
        testcase.addTypeEqualityFunc(flask.Response, cls.get_assert(testcase))

    @classmethod
    def get_assert(cls, testcase):
        def assert_func(it1, it2, msg=None):
            testcase.assertEqual(it1.status, it2.status)
            data1 = flask.json.loads(it1.data)
            data2 = flask.json.loads(it2.data)
            testcase.assertEqual(data1, data2)
        return assert_func
