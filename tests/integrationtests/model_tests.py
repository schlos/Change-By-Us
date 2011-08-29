from unittest2 import TestCase
from nose.tools import *
from mock import Mock

import mixins

from datetime import datetime
from datetime import timedelta
from framework.orm_holder import OrmHolder
from giveaminute.project import addMessage
from giveaminute.models import *

class Test_StoredMessage_CreatedDateTime (mixins.AppSetupMixin, TestCase):
    def test_is_returned_from_the_db_in_local_time(self):
        before = datetime.now() - timedelta(seconds=1)
        addMessage(self.db, projectId=5, message='hello', message_type='my message type')
        after = datetime.now()

        messages = self.db.query('select created_datetime from project_message where project_id=5')
        created_datetime = messages[0]['created_datetime']

        self.assertIsNone(created_datetime.tzinfo)
        self.assert_(before <= created_datetime <= after, "%s <= %s <= %s" % (before, created_datetime, after))


class Test_Volunteer (mixins.AppSetupMixin, TestCase):
    fixtures = ['aarons_db_20110826.sql']

    def test_makes_associated_need_accessible_when_it_is_created(self):
        orm = OrmHolder().orm
        vol = Volunteer()
        vol.need_id=2 #orm.query(Need).get(2)
        vol.member_id=1
        orm.add(vol)
        orm.commit()

        assert_equal(vol.need_id, 2)
        assert vol.need is not None


class Test_User_avatarPath (mixins.AppSetupMixin, TestCase):
    fixtures = ['aarons_db_20110826.sql']

    def test_returns_the_supposed_path_to_the_users_avatar_image_on_the_media_root(self):
        orm = OrmHolder().orm
        user = orm.query(User).get(3)

        path = user.avatar_path

        assert_equal(path, 'images/1/1.png')

    def test_returns_None_if_user_has_no_avatar_set(self):
        orm = OrmHolder().orm
        user = orm.query(User).get(2)

        path = user.avatar_path

        assert_is_none(path)