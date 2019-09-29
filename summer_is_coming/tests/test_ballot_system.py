import io
import itertools
from copy import deepcopy
from unittest.mock import patch

import pytest

from summer_is_coming import utils
from summer_is_coming.ballot import BallotKingdom, BallotMessage
from summer_is_coming.universe_competition_factory import BallotFactory


class TestBallotKingdom:
    @staticmethod
    def read_message_helper(kingdoms):
        kingdom, *_ = kingdoms
        BallotKingdom._messages = []
        BallotKingdom(kingdom)
        assert BallotKingdom._messages != []

    @staticmethod
    def test_constructor(kingdoms):
        kingdom, kingdom2, kingdom3 = kingdoms
        ballot_kingdom = BallotKingdom(kingdom)
        ballot_kingdom.is_competing = True
        assert (
            ballot_kingdom.kingdom.give_allegiance(
                kingdom2, msg=ballot_kingdom.kingdom.emblem
            )
            is False
        )
        ballot_kingdom.is_competing = False
        assert ballot_kingdom.kingdom.give_allegiance(
            kingdom2, msg=ballot_kingdom.kingdom.emblem
        )

        TestBallotKingdom.read_message_helper(kingdoms)

    @staticmethod
    def test__read_messages(kingdoms):
        TestBallotKingdom.read_message_helper(kingdoms)

    @staticmethod
    def test__check_availabiliy(kingdoms):
        kingdom, kingdom2, _ = kingdoms
        ballot_kingdom = BallotKingdom(kingdom)
        fn = ballot_kingdom._check_availability(ballot_kingdom.kingdom.give_allegiance)

        ballot_kingdom.is_competing = True
        assert fn(kingdom2, msg=kingdom.emblem) is False
        ballot_kingdom.is_competing = False
        assert fn(kingdom2, msg=kingdom.emblem)
        assert fn(kingdom2, msg=kingdom.emblem) is False

    @staticmethod
    def test_compete(kingdoms):
        ballot_kingdoms = [BallotKingdom(kingdom) for kingdom in kingdoms]
        ballot_kingdom, *other_kingdoms = ballot_kingdoms
        ballot_messages = ballot_kingdom.compete(other_kingdoms)

        assert len(ballot_messages) == len(other_kingdoms)
        assert all([msg.sender == ballot_kingdom for msg in ballot_messages])
        sort_key = lambda x: x.kingdom.name
        assert sorted(
            [msg.receiver for msg in ballot_messages], key=sort_key
        ) == sorted(other_kingdoms, key=sort_key)


class TestBallot:
    @staticmethod
    @pytest.fixture
    def southeros_ballot():
        return BallotFactory.get("Southeros")

    @staticmethod
    @pytest.fixture
    def southeros_ballot_with_competitors(southeros_ballot):
        ballot_kingdom, ballot_kingdom2, ballot_kingdom3, *other_kingdoms = (
            southeros_ballot._ballot_kingdoms
        )
        southeros_ballot._competitors = [
            ballot_kingdom,
            ballot_kingdom2,
            ballot_kingdom3,
        ]
        return southeros_ballot

    @staticmethod
    @pytest.fixture
    def southeros_ballot_with_competitors_and_allies(southeros_ballot_with_competitors):
        ballot_kingdom, ballot_kingdom2, *other_kingdoms = (
            southeros_ballot_with_competitors._ballot_kingdoms
        )
        ballot_kingdom.kingdom._allies_received.add(other_kingdoms[0].kingdom)
        ballot_kingdom2.kingdom._allies_received.add(other_kingdoms[1].kingdom)
        return southeros_ballot_with_competitors

    @staticmethod
    def test__process_input(southeros_ballot):
        assert southeros_ballot._process_input(" air water ") == ["Air", "Water"]
        assert southeros_ballot._process_input("air water") == ["Air", "Water"]
        with pytest.raises(ValueError):
            southeros_ballot._process_input("")

    @staticmethod
    def test__reset_state(southeros_ballot_with_competitors_and_allies):
        southeros_ballot = southeros_ballot_with_competitors_and_allies
        ballot_kingdom, ballot_kingdom2, *_ = southeros_ballot._ballot_kingdoms
        southeros_ballot._ballot = ["123", "132"]

        southeros_ballot._reset_state()
        assert not ballot_kingdom.kingdom._allies_received
        assert not ballot_kingdom2.kingdom._allies_given
        assert not southeros_ballot._ballot

    @staticmethod
    def test__get_worthy_competitors(southeros_ballot_with_competitors):
        southeros_ballot = southeros_ballot_with_competitors
        ballot_kingdom, ballot_kingdom2, ballot_kingdom3, *other_kingdoms = (
            southeros_ballot._ballot_kingdoms
        )

        sort_key = lambda x: x.kingdom.name
        assert sorted(
            southeros_ballot._get_worthy_competitors(), key=sort_key
        ) == sorted([ballot_kingdom, ballot_kingdom2, ballot_kingdom3], key=sort_key)

        ballot_kingdom.kingdom._allies_received.add(other_kingdoms[0].kingdom)
        ballot_kingdom2.kingdom._allies_received.add(other_kingdoms[1].kingdom)
        assert sorted(
            southeros_ballot._get_worthy_competitors(), key=sort_key
        ) == sorted([ballot_kingdom, ballot_kingdom2], key=sort_key)

        ballot_kingdom.kingdom._allies_received.add(other_kingdoms[2].kingdom)
        assert southeros_ballot._get_worthy_competitors() == [ballot_kingdom]

    @staticmethod
    def test__update_competitors(southeros_ballot_with_competitors_and_allies):
        southeros_ballot = southeros_ballot_with_competitors_and_allies
        ballot_kingdom, ballot_kingdom2, ballot_kingdom3, *other_kingdoms = (
            southeros_ballot._ballot_kingdoms
        )

        sort_key = lambda x: x.kingdom.name
        southeros_ballot._update_competitors()
        assert sorted(southeros_ballot._competitors, key=sort_key) == sorted(
            [ballot_kingdom, ballot_kingdom2], key=sort_key
        )

    @staticmethod
    def test__settle_tie(southeros_ballot_with_competitors):
        southeros_ballot = southeros_ballot_with_competitors
        ballot_kingdom, ballot_kingdom2, ballot_kingdom3, *_ = (
            southeros_ballot._ballot_kingdoms
        )
        assert southeros_ballot._winner is None
        southeros_ballot._settle_tie()
        assert isinstance(southeros_ballot._winner, BallotKingdom)

    @staticmethod
    @patch("builtins.input", side_effect=["Air Land"])
    def test_register_competitors(input_mock, southeros_ballot):
        southeros_ballot.register_competitors()
        assert southeros_ballot._competitors == [
            utils.sorted_list_get_with_key(southeros_ballot._ballot_kingdoms, "Air"),
            utils.sorted_list_get_with_key(southeros_ballot._ballot_kingdoms, "Land"),
        ]
        for competitor in southeros_ballot._competitors:
            assert competitor.is_competing

    @staticmethod
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show_status(stdout_patch, southeros_ballot_with_competitors_and_allies):
        southeros_ballot = southeros_ballot_with_competitors_and_allies
        southeros_ballot._round_count = 5
        competitors = deepcopy(southeros_ballot._competitors)

        southeros_ballot.show_status()
        expected_out = "Results after round five ballot count\n"

        # this is why competitors was deepcopied, so that we do not access the kingdom objects in southeros_ballot when checking
        for competitor in competitors:
            expected_out += f"Output: Allies for {competitor.kingdom.name}: {len(competitor.kingdom._allies_received)}\n"

        assert stdout_patch.getvalue() == expected_out

    @staticmethod
    def test_winner(southeros_ballot_with_competitors):
        TestBallot.test__settle_tie(southeros_ballot_with_competitors)

    @staticmethod
    def test_evaluate_competitors(southeros_ballot_with_competitors):
        southeros_ballot = southeros_ballot_with_competitors
        ballot_kingdom, ballot_kingdom2, ballot_kingdom3, *other_kingdoms = (
            southeros_ballot._ballot_kingdoms
        )

        msg = BallotMessage(
            sender=ballot_kingdom,
            receiver=other_kingdoms[0],
            msg=other_kingdoms[0].kingdom.emblem,
        )
        msg2 = BallotMessage(
            sender=ballot_kingdom2,
            receiver=other_kingdoms[1],
            msg=other_kingdoms[1].kingdom.emblem,
        )
        southeros_ballot._ballot = [msg, msg2]

        assert southeros_ballot._winner is None
        southeros_ballot.evaluate_competitors()
        assert southeros_ballot._winner is None

        msg3 = BallotMessage(
            sender=ballot_kingdom,
            receiver=other_kingdoms[2],
            msg=other_kingdoms[2].kingdom.emblem,
        )
        southeros_ballot._ballot.append(msg3)

        assert southeros_ballot._winner is None
        southeros_ballot.evaluate_competitors()
        assert southeros_ballot._winner is ballot_kingdom

    @staticmethod
    def test_commence(southeros_ballot_with_competitors):
        southeros_ballot = southeros_ballot_with_competitors
        ballot_kingdom, ballot_kingdom2, ballot_kingdom3, *_ = (
            southeros_ballot._ballot_kingdoms
        )
        expected_messages = [
            (sender, receiver)
            for sender, receiver in itertools.product(
                southeros_ballot._competitors, southeros_ballot._ballot_kingdoms
            )
            if sender.kingdom != receiver.kingdom
        ]
        southeros_ballot.commence()
        actual_messages = [
            (msg.sender, msg.receiver) for msg in southeros_ballot._ballot
        ]

        sort_key = lambda x: x[0].kingdom.name + x[1].kingdom.name
        assert sorted(expected_messages, key=sort_key) == sorted(
            actual_messages, key=sort_key
        )
