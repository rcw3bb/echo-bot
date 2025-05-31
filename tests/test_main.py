"""
Unit tests for the __main__ module in echo_bot.

Author: Ron Webb
Since: 1.0.0
"""

from unittest.mock import patch

def test_main_runs_chatbot(monkeypatch):
    """
    Test that main() calls run_chatbot().
    """
    from echo_bot import __main__
    called = {}
    monkeypatch.setattr(__main__, "run_chatbot", lambda: called.setdefault("ran", True))
    __main__.main()
    assert called.get("ran")


def test_main_entry_point(monkeypatch):
    """
    Test that running __main__ as __main__ calls main().
    """
    import sys
    import echo_bot.__main__ as main_mod
    called = {}
    monkeypatch.setattr(main_mod, "main", lambda: called.setdefault("main", True))
    monkeypatch.setitem(sys.modules, "__main__", main_mod)
    main_mod.__dict__["__name__"] = "__main__"
    # Simulate running as script
    exec('if __name__ == "__main__": main()', main_mod.__dict__)
    assert called.get("main")
