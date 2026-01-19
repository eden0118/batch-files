"""Simplified to Traditional Chinese conversion utilities"""

from typing import Optional

# Global state for OpenCC
_HAS_OPENCC = False
_OPENCC_CONVERTER: Optional[object] = None
_OPENCC_STATUS = "Init..."


def init_opencc() -> None:
    """初始化 OpenCC (簡轉繁工具)"""
    global _HAS_OPENCC, _OPENCC_CONVERTER, _OPENCC_STATUS

    try:
        from opencc import OpenCC
        for config in ['s2t', 's2t.json', 't2s', 't2s.json']:
            try:
                temp_cc = OpenCC(config)
                if temp_cc.convert('国') == '國':
                    _OPENCC_CONVERTER = temp_cc
                    _HAS_OPENCC = True
                    _OPENCC_STATUS = f"Active ({config})"
                    break
            except:
                continue
        if not _HAS_OPENCC:
            _OPENCC_STATUS = "Missing (Fallback Active)"
    except ImportError:
        _OPENCC_STATUS = "Module Missing"


def has_opencc() -> bool:
    """Check if OpenCC is available"""
    return _HAS_OPENCC


def get_opencc_converter() -> Optional[object]:
    """Get the OpenCC converter instance"""
    return _OPENCC_CONVERTER


def get_opencc_status() -> str:
    """Get OpenCC initialization status"""
    return _OPENCC_STATUS


# Initialize on import
init_opencc()
