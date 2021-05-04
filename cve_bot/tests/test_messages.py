from cve_bot.messages import MessageSplitter


def test_one_chunk():
    msg = "Text <b>is formatted</b>"
    assert list(MessageSplitter(msg)) == ["Text <b>is formatted</b>"]


def test_unformatted_split():
    msg = "aaabbb"
    assert list(MessageSplitter(msg, chunk_size=3)) == ["aaa", "bbb"]

    msg = "Text <b>is formatted</b>"
    assert list(MessageSplitter(msg, chunk_size=15)) == ["Text <b>is </b>", "<b>formatte</b>", "<b>d</b>"]


def test_formatted_split():
    msg = "<b>Formatted</b> and <b>splitted</b>"
    assert list(MessageSplitter(msg, chunk_size=16)) == ["<b>Formatted</b>", " and <b>spli</b>", "<b>tted</b>"]

    msg = "<code>long part</code>"
    assert list(MessageSplitter(msg, chunk_size=18)) == ["<code>long </code>", "<code>part</code>"]

    msg = "<b>text</b><b>text</b>"
    assert list(MessageSplitter(msg, chunk_size=13)) == ["<b>text</b>", "<b>text</b>"]
