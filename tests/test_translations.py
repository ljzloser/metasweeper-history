from pathlib import Path
import xml.etree.ElementTree as ET

import pytest
from PySide6.QtCore import QCoreApplication, QTranslator

from plugin_manager.translations import _PUBLIC_CONTEXTS


PACKAGE = Path(__file__).resolve().parents[1] / "history"
CONTEXT = "HistoryPlugin"


@pytest.mark.parametrize("locale", ("en_US", "de_DE", "ja_JP", "pl_PL"))
def test_catalog_is_private_complete_and_loadable(qapp, locale):
    source = PACKAGE / "translations" / f"{locale}.ts"
    tree = ET.parse(source)
    assert {node.findtext("name") for node in tree.findall(".//context")} == {CONTEXT}
    assert CONTEXT not in _PUBLIC_CONTEXTS
    messages = tree.findall(".//message")
    assert messages
    translator = QTranslator()
    assert translator.load(str(source.with_suffix(".qm")))
    for message in messages:
        translation = message.find("translation")
        assert translation is not None, message.findtext("source")
        assert translation.get("type") not in ("unfinished", "vanished", "obsolete")
        assert "".join(translation.itertext()).strip(), message.findtext("source")
    assert any(translator.translate(CONTEXT, message.findtext("source")) for message in messages)


def test_plugin_sources_use_private_contexts():
    for source in PACKAGE.rglob("*.py"):
        text = source.read_text(encoding="utf-8")
        assert 'translate("Form"' not in text, source
        assert 'translate("SkinManager"' not in text, source


def test_config_text_retranslates_after_language_change(qapp):
    from plugin_manager.config_widget import OtherInfoWidget
    from history.plugin import HistoryConfig

    class Translator(QTranslator):
        def isEmpty(self):
            return False

        def translate(self, context, source, disambiguation=None, n=-1):
            if context == "HistoryPlugin" and source == "小数位数":
                return "Decimal places"
            return None

    widget = OtherInfoWidget(HistoryConfig())
    translator = Translator()
    assert QCoreApplication.installTranslator(translator)
    try:
        QCoreApplication.sendEvent(widget, __import__("PySide6.QtCore", fromlist=["QEvent"]).QEvent(
            __import__("PySide6.QtCore", fromlist=["QEvent"]).QEvent.Type.LanguageChange))
        assert widget._labels["float_decimals"].text() == "Decimal places"
        assert widget._widgets["float_decimals"].get_value() == 2
    finally:
        QCoreApplication.removeTranslator(translator)


def test_history_view_and_filter_symbols_follow_language(qapp, qtbot, tmp_path):
    from history.main_widget import HistoryMainWidget
    from history.models import CompareSymbol, LogicSymbol

    class Translator(QTranslator):
        def isEmpty(self):
            return False

        def translate(self, context, source, disambiguation=None, n=-1):
            values = {"查询": "Query", "与": "and", "等于": "equals"}
            return values.get(source) if context == CONTEXT else None

    widget = HistoryMainWidget(tmp_path / "history.db", tmp_path / "fields.json")
    qtbot.addWidget(widget)
    widget.show()
    old_logic = LogicSymbol.display_names()[0]
    old_compare = CompareSymbol.display_names()[0]
    translator = Translator()
    assert QCoreApplication.installTranslator(translator)
    try:
        qtbot.waitUntil(lambda: widget.query_button.text() == "Query")
        assert LogicSymbol.display_names()[0] == "and"
        assert CompareSymbol.display_names()[0] == "equals"
        assert LogicSymbol.from_display_name(old_logic).to_sql == "and"
        assert CompareSymbol.from_display_name(old_compare).to_sql == "="
    finally:
        QCoreApplication.removeTranslator(translator)
