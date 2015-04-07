# -*- coding: utf-8 -*-


from freezegun import freeze_time  # $ pip install freezegun

from service.handlers import filters


class TestWindowTimeFilter:

    def test_1(self):
        record = {}
        filter_window = filters.WindowTimeFilter("08:00", "11:00")
        test_cases = (
            ("2015-04-06 08:00:01", False),
            ("2015-04-06 09:40:01", False),
            ("2015-04-06 11:00:00", False),
            ("2015-04-06 12:00:01", True),
            ("2015-04-06 12:56:01", True),
        )
        for now, expected in test_cases:
            freezer = freeze_time(now)
            freezer.start()
            assert filter_window.filter(record) == expected
            freezer.stop()

    def test_2(self):
        record = {}
        filter_window = filters.WindowTimeFilter("08:00", "14:00")
        test_cases = (
            ("2015-04-06 08:00:01", False),
            ("2015-04-06 09:40:01", False),
            ("2015-04-06 14:00:00", False),
            ("2015-04-06 16:00:01", True),
        )
        for now, expected in test_cases:
            freezer = freeze_time(now)
            freezer.start()
            assert filter_window.filter(record) == expected
            freezer.stop()

    def test_3(self):
        record = {}
        filter_window = filters.WindowTimeFilter("14:00", "18:00")
        test_cases = (
            ("2015-04-06 14:00:01", False),
            ("2015-04-06 16:40:01", False),
            ("2015-04-06 19:00:01", True),
        )
        for now, expected in test_cases:
            freezer = freeze_time(now)
            freezer.start()
            assert filter_window.filter(record) == expected
            freezer.stop()

    def test_4(self):
        record = {}
        filter_window = filters.WindowTimeFilter("18:00", "6:00")
        test_cases = (
            ("2015-04-06 18:00:01", False),
            ("2015-04-07 02:40:01", False),
            ("2015-04-07 06:00:00", False),
            ("2015-04-07 06:00:01", True),
        )
        for now, expected in test_cases:
            freezer = freeze_time(now)
            freezer.start()
            assert filter_window.filter(record) == expected
            freezer.stop()
