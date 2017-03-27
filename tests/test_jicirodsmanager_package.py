"""Test the jicirodsmanager package."""


def test_version_is_string():
    import jicirodsmanager
    assert isinstance(jicirodsmanager.__version__, str)
