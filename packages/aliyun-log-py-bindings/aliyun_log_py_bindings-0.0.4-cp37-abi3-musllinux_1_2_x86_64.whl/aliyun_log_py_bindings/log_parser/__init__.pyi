from typing import List, Dict


def logs_to_flat_json_str(uncompressed: bytes) -> str:
    """
    :param uncompressed: the uncompressed bytes
    :return: the flatten json str in string type
    """
    ...


def lz4_logs_to_flat_json_str(compressed: bytes, raw_size: int) -> str:
    """
    :param compressed: the lz4 compressed bytes
    :param raw_size: the raw size of bytes decompressed
    :return: the flatten json str in string type
    """
    ...


def lz4_logs_to_flat_json(compressed: bytes,
                          raw_size: int,
                          time_as_str: bool,
                          decode_utf8: bool) -> List[Dict]:
    """
    :param compressed: the lz4 compressed bytes
    :param raw_size: the raw size of bytes decompressed
    :param time_as_str: whether to convert log.Time and log.Time_us to string type
    :param decode_utf8: If set to true, type of log content value will be str, otherwise bytes. If decode_utf8 is true and the
        uncompressed data contains non-utf8 charters, an exception is raised
    :return: the flatten json list
    """
    ...
