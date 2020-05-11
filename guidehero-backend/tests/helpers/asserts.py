import flask
from lib.models import transfer as transfer_module
from lib.models.user import User


def assertJsonResponse(r1, r2):
    assert r1.status == r2.status, 'Result response status {} is as expected {}'.format(r1.status, r2.status)
    flask.json.loads(r1.data)
    flask.json.loads(r2.data)


def assertJsonResponseWithResultStatus(r1, r2):
    assertJsonResponse(r1, r2)
    r1_data = flask.json.loads(r1.data)
    r2_data = flask.json.loads(r2.data)
    print(r1_data, r2_data)
    assert r1_data['result'] == r2_data['result'], 'Result is not the same {} != {}'.format(r1_data['result'], r2_data['result'])


def assertJsonCardData(data1, data2):
    data1 = flask.json.loads(data1)
    data2 = flask.json.loads(data2)
    assert data1['name'] == data2['name'], 'Name for card is not the same: {} != {}'.format(data1['name'], data2['name'])


def assertCard(c1, c2):
    assertTags(c1.tags, c2.tags)
    assert c1.scale == c2.scale, "Scale are not the same {} != {}".format(c1.scale, c2.scale)


def assertTags(ts1, ts2):
    assert type(ts1) == type(ts2), 'Type of result={}, type of expected={}'.format(type(ts1), type(ts2))
    ts1_names = sorted([unicode(tag.name) for tag in ts1])
    ts2_names = sorted([unicode(tag.name) for tag in ts2])
    assert ts1_names == ts2_names, 'Result tags are {}, but expected {}'.format(ts1_names, ts2_names)


def assertUser(u2):
    if u2 is None:
        return
    u1 = User.query.get(u2.id)
    assert u1.id == u2.id, 'ID is not  the same {} != {}'.format(u1.id, u2.id)
    assert u1.silver_points == u2.silver_points, 'Silver Points are not the same: {} != {}'.format(u1.silver_points, u2.silver_points)


def Transfer(it2):
    T = transfer_module.Transfer
    it1 = transfer_module.Transfer.query.filter(
        T.user_from == it2.user_from,
        T.card_from == it2.card_from,
        T.user_to == it2.user_to,
        T.card_to == it2.card_to,
        T.transaction_type == it2.transaction_type).first()
    if it1 is None:
        assert 1 == 2, "Can not find object"
    _assertObjects(it1, it2, ['silver_points'])


def assertObjects(obj1, obj2, fields):
    return _assertObjects(obj1, obj2, fields)


def _assertObjects(obj1, obj2, fields):
    assert type(obj1) == type(obj2), 'Type is not the same: {} != {}'.format(type(obj1), type(obj2))
    for name in fields:
        _assertAttribute(obj1, obj2, name)


def _assertAttribute(obj1, obj2, name):
    assert getattr(obj1, name) == getattr(obj2, name), 'Attribute {} is not same:\n {} != {}'.format(name, getattr(obj1, name), getattr(obj2, name))
