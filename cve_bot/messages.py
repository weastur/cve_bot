import logging

logger = logging.getLogger(__name__)

TAGS = (("<b>", "</b>"), ("<i>", "</i>"), ("<s>", "</s>"), ("<code>", "</code>"))  # noqa: WPS221


class MessageSplitter(object):
    def __init__(self, message, chunk_size=4096):
        logger.debug("Initial message = %s", message)
        self._msg = message
        self._chunk_size = chunk_size
        self._splitted = []
        self._split()
        logger.debug("Splitted message = %s", self._splitted)

    def __iter__(self):
        return iter(self._splitted)

    def _split_tagged_text_0(self, chunk, pos_close, tag_close):
        end_chunk_pos = pos_close + len(tag_close)
        chunk += self._msg[:end_chunk_pos]
        self._msg = self._msg[end_chunk_pos:]
        if not self._msg:
            self._splitted.append(chunk)
        return chunk

    def _split_tagged_text_1(self, chunk, tag_open, tag_close):
        end_chunk_pos = self._chunk_size - len(chunk) - len(tag_close)
        chunk += self._msg[:end_chunk_pos] + tag_close
        self._msg = tag_open + self._msg[end_chunk_pos:]
        self._splitted.append(chunk)
        return ""

    def _split_regular_text_0(self, chunk):
        end_chunk_pos = self._chunk_size - len(chunk)
        chunk += self._msg[:end_chunk_pos]
        self._msg = self._msg[end_chunk_pos:]
        self._splitted.append(chunk)
        return ""

    def _split_regular_text_1(self, chunk, pos_open):
        chunk += self._msg[:pos_open]
        self._msg = self._msg[pos_open:]
        if not self._msg:
            self._splitted.append(chunk)
        return chunk

    def _split(self):  # noqa: WPS231
        chunk = ""
        while self._msg:
            pos_open, pos_close, tag_open, tag_close = self._find_lowest_pos()
            if pos_open == 0:
                if len(chunk) + pos_close + len(tag_close) <= self._chunk_size:
                    chunk = self._split_tagged_text_0(chunk, pos_close, tag_close)
                elif self._chunk_size - len(chunk) > len(tag_open) + len(tag_close):  # noqa: WPS221
                    chunk = self._split_tagged_text_1(chunk, tag_open, tag_close)
                else:
                    self._splitted.append(chunk)
                    chunk = ""
            else:
                if pos_open == -1:
                    pos_open = len(self._msg)
                if len(chunk) + pos_open > self._chunk_size:
                    chunk = self._split_regular_text_0(chunk)
                else:
                    chunk = self._split_regular_text_1(chunk, pos_open)

    def _find_lowest_pos(self):
        lowest_pos_open = -1
        lowest_pos_close = -1
        lowest_tag_open = None
        lowest_tag_close = None
        for tag_open, tag_close in TAGS:
            pos = self._msg.find(tag_open)
            if pos != -1 and (lowest_pos_open == -1 or pos < lowest_pos_open):
                lowest_pos_open = pos
                lowest_pos_close = self._msg.find(tag_close)
                lowest_tag_open = tag_open
                lowest_tag_close = tag_close
        return lowest_pos_open, lowest_pos_close, lowest_tag_open, lowest_tag_close
