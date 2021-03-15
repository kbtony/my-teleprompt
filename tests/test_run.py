from datetime import datetime

from teleprompter.run import CommandLine, utcoffset_to_seconds, Query, lookup


def test_command_line():
    argv = ["run.py", "example.csv", "2021-06-19T15:27:30+10:00"]
    user_input = CommandLine(argv)
    assert user_input.filename == "example.csv"
    assert user_input.query == "2021-06-19T15:27:30+10:00"


def test_utcoffset_to_seconds():
    time = ["11:30", "0425", "01"]
    assert utcoffset_to_seconds(time[0]) == 41400
    assert utcoffset_to_seconds(time[1]) == 15900
    assert utcoffset_to_seconds(time[2]) == 3600


def test_query():
    query = ["2021-06-19T15:27:30Z", "2020-11-19T15:27:30+10:00", "2008-06-08T19:37:22-09:22"]
    my_query = [Query(query[0]), Query(query[1]), Query(query[2])]
    assert my_query[0].date.isoformat() == "2021-06-19T15:27:30"
    assert my_query[0].check == "19/6/21"
    assert my_query[1].time == "10:00"
    assert my_query[1].date.isoformat() == "2020-11-19T05:27:30"
    assert my_query[2].time == "09:22"
    assert my_query[2].date.isoformat() == "2008-06-09T04:59:22"
    assert not my_query[2].early


def test_lookup():
    program_list = [['T.V Shopping', 'G', '19/6/21', '0:00', '10800'], ['Days of Our Lives', 'PG', '19/6/21', '3:00', '3600'], ['M.A.S.H', 'PG', '19/6/21', '4:00', '5400'], ['The Simpsons', 'PG', '19/6/21', '5:30', '1800'], ['Futurama', 'PG', '19/6/21', '6:00', '3600'], ['Family Guy', 'M', '19/6/21', '7:00', '3000']]
    date = datetime.fromisoformat("2021-06-19T05:27:30").replace(tzinfo=None)
    result = lookup(program_list, date, "19/6/21", 36000, True)
    assert result == "[15:30] That was M.A.S.H, up next is The Simpsons which is rated PG and coming up later is Futurama."
