import locale
from typing import Dict


class LanguageManager:
    """可爱的多语言小管家~"""

    def __init__(self) -> None:
        self.lang = self._detect_language()
        self.texts: Dict[str, Dict[str, str]] = {
            "start_game": {"zh": "开始游戏", "en": "Start Game", "jp": "ゲーム開始"},
            "hint": {"zh": "提示", "en": "Hint", "jp": "ヒント"},
            "undo": {"zh": "撤销", "en": "Undo", "jp": "元に戻す"},
            "success": {"zh": "成功", "en": "Success", "jp": "成功"},
            "close": {"zh": "接近", "en": "Close", "jp": "惜しい"},
            "fail": {"zh": "失败", "en": "Fail", "jp": "失敗"},
            "editor": {"zh": "编辑器", "en": "Editor", "jp": "エディター"},
        }

    def _detect_language(self) -> str:
        loc = locale.getdefaultlocale()[0] if locale.getdefaultlocale() else "en_US"
        if loc and loc.lower().startswith("zh"):
            return "zh"
        if loc and loc.lower().startswith("ja"):
            return "jp"
        return "en"

    def t(self, key: str) -> str:
        return self.texts.get(key, {}).get(self.lang, key)
