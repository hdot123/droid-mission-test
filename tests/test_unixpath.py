from unixpath import normalize


# --- acceptance points from the work order ---


def test_absolute_dotdot_cancels_previous_segment():
    assert normalize("/a/b/../c") == "/a/c"


def test_collapse_slashes_drop_dot_and_trailing_slash():
    assert normalize("a//b/./c/") == "a/b/c"


def test_dotdot_beyond_root_absolute_stops_at_root():
    assert normalize("/../../x") == "/x"


def test_relative_keeps_uncancellable_dotdot():
    assert normalize("a/../../b") == "../b"


def test_dot_slash_is_dot():
    assert normalize("./") == "."


def test_root_stays_root():
    assert normalize("/") == "/"


def test_empty_string_is_dot():
    assert normalize("") == "."


def test_relative_leading_dotdot_kept():
    assert normalize("../a") == "../a"


# --- remaining stated requirements ---


def test_repeated_dotdot_beyond_root_on_absolute_paths():
    assert normalize("/a/../../..") == "/"
    assert normalize("/../../..") == "/"
    assert normalize("/a/b/../../../") == "/"


def test_relative_keeps_multiple_leading_dotdot():
    assert normalize("../..") == "../.."
    assert normalize("a/../../b/../..") == "../.."
    assert normalize("../../a/../../b") == "../../../b"


def test_dot_in_middle_of_path():
    assert normalize("/a/./b/./c") == "/a/b/c"
    assert normalize("a/./b") == "a/b"
    assert normalize("./a/./b") == "a/b"


def test_no_trailing_slash_except_root():
    assert normalize("/a/b/") == "/a/b"
    assert normalize("a/b//") == "a/b"
    assert normalize("a/b/./") == "a/b"


# --- extra coverage ---


def test_cancel_to_empty_relative_is_dot():
    assert normalize("a/..") == "."
    assert normalize("a/b/../..") == "."


def test_dotdot_segment_stacks_and_cancels():
    assert normalize("..") == ".."
    assert normalize("../a/..") == ".."
    assert normalize("a/b/../c/") == "a/c"


def test_collapse_consecutive_slashes():
    assert normalize("a//b") == "a/b"
    assert normalize("///a/b") == "/a/b"


def test_dot_only_and_relative_prefixes():
    assert normalize("./.") == "."
    assert normalize("./a") == "a"


def test_type_is_str():
    result = normalize("/x/../y")
    assert isinstance(result, str)
