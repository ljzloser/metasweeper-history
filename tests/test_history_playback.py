import sys
from pathlib import Path
from unittest.mock import Mock

import pytest


@pytest.mark.parametrize(("executable_names", "has_source", "expected_name"), [
    ((), False, None),
    (("metasweeper.exe",), False, "metasweeper.exe"),
    (("metaminsweeper.exe",), False, "metaminsweeper.exe"),
    (("metasweeper.exe", "metaminsweeper.exe"), False, "metasweeper.exe"),
    (("metasweeper.exe", "metaminsweeper.exe"), True, "main.py"),
    ((), True, "main.py"),
])
def test_history_playback_command(
    tmp_path, monkeypatch, executable_names, has_source, expected_name,
):
    from history import history_table

    for name in executable_names:
        (tmp_path / name).touch()
    main_py = tmp_path / "src" / "main.py"
    if has_source:
        main_py.parent.mkdir()
        main_py.touch()
    monkeypatch.setattr(history_table, "get_executable_dir", lambda: tmp_path)
    launch = Mock()
    warning = Mock()
    monkeypatch.setattr(history_table.subprocess, "Popen", launch)
    monkeypatch.setattr(history_table.QMessageBox, "warning", warning)
    monkeypatch.setattr(
        history_table.QTimer, "singleShot", lambda delay, cleanup: cleanup())
    table = Mock()
    table.save_evf.return_value = True

    history_table.HistoryTable.play_row(table)

    if expected_name is None:
        launch.assert_not_called()
        table.save_evf.assert_not_called()
        warning.assert_called_once()
        return
    warning.assert_not_called()
    launch.assert_called_once()
    replay_path = Path(table.save_evf.call_args.args[0])
    expected_command = (
        [sys.executable, str(main_py), str(replay_path)] if has_source
        else [str(tmp_path / expected_name), str(replay_path)]
    )
    assert launch.call_args.args[0] == expected_command
    assert not replay_path.exists()
