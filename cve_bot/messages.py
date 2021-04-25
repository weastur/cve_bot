TAGS = (("<b>", "</b>"), ("<i>", "</i>"), ("<s>", "</s>"), ("<code>", "</code>"))  # noqa: WPS221


class MessageSplitter(object):
    def __init__(self, message, chunk_size=4096):
        self._msg = message
        self._chunk_size = chunk_size
        self._splitted = []
        self._split()

    def __iter__(self):
        return iter(self._splitted)

    def _split(self):  # noqa: WPS210
        current_chunk_idx = 0
        while current_chunk_idx * self._chunk_size < len(self._msg):
            current_chunk_start_pos = current_chunk_idx * self._chunk_size
            current_chunk_end_pos = (current_chunk_idx + 1) * self._chunk_size
            current_chunk = self._msg[current_chunk_start_pos:current_chunk_end_pos]
            for tag_open, tag_close in TAGS:
                tag_open_last_pos = current_chunk.rfind(tag_open)
                tag_close_last_pos = current_chunk.rfind(tag_close)
                if tag_open_last_pos > tag_close_last_pos:
                    current_chunk = (
                        self._msg[current_chunk_start_pos : current_chunk_end_pos - len(tag_close)] + tag_close
                    )
                    self._msg = "{prev}{tag_close}{tag_open}{last}".format(
                        prev=self._msg[:current_chunk_end_pos],
                        tag_close=tag_close,
                        tag_open=tag_open,
                        last=self._msg[current_chunk_end_pos:],
                    )
                    break
            self._splitted.append(current_chunk)
            current_chunk_idx += 1
