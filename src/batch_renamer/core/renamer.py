"""Core file renaming logic - independent of UI framework"""

import os
from pathlib import Path
from typing import List, Tuple, Optional
from ..utils.constants import SIMPLIFIED_TO_TRADITIONAL
from ..utils.converter import has_opencc, get_opencc_converter


class FileRenamer:
    """File renaming engine - UI-agnostic business logic"""

    def __init__(self):
        """Initialize the file renamer"""
        self.targets: List[Tuple[Path, str]] = []

    def apply_conversion(self, name: str, operation: str, find_text: str = "", replace_text: str = "") -> str:
        """
        應用文字轉換操作

        Args:
            name: 原始名稱
            operation: 操作類型 ("s2t" = 簡轉繁, "replace" = 替換, "none" = 無)
            find_text: 要查找的文本 (用於 replace 操作)
            replace_text: 替換文本

        Returns:
            轉換後的名稱
        """
        if operation == "s2t":
            # 優先使用 OpenCC，失敗則用微型字典
            if has_opencc():
                converter = get_opencc_converter()
                if converter:
                    converted = converter.convert(name)
                    if converted != name:
                        return converted
            return name.translate(SIMPLIFIED_TO_TRADITIONAL)

        elif operation == "replace":
            if find_text:
                return name.replace(find_text, replace_text)

        return name

    def apply_formatting(self, item: Path, name: str, prefix: str = "", suffix: str = "", symbols: str = "") -> str:
        """
        應用文件名格式化 (移除符號、添加前綴後綴)

        Args:
            item: 路徑對象
            name: 名稱
            prefix: 前綴
            suffix: 後綴
            symbols: 要移除的符號

        Returns:
            格式化後的名稱
        """
        # 移除指定符號
        if symbols:
            for char in symbols:
                name = name.replace(char, "")

        if item.is_file():
            # 文件：保持副檔名
            stem = Path(name).stem
            ext = Path(name).suffix
            return f"{prefix}{stem}{suffix}{ext}"
        else:
            # 資料夾：直接添加
            return f"{prefix}{name}{suffix}"

    def scan_directory(
        self,
        root_path: Path,
        rename_mode: str,
        filter_type: str,
        valid_exts: List[str],
        operation: str,
        find_text: str = "",
        replace_text: str = "",
        prefix: str = "",
        suffix: str = "",
        symbols: str = ""
    ) -> List[Tuple[Path, str]]:
        """
        遞歸掃描目標資料夾及其子資料夾，生成重命名配對

        Args:
            root_path: 根目錄路徑
            rename_mode: "files" 或 "both" (包含資料夾)
            filter_type: "all" 或 "ext"
            valid_exts: 有效的副檔名列表
            operation: 操作類型
            find_text: 查找文本
            replace_text: 替換文本
            prefix: 前綴
            suffix: 後綴
            symbols: 要移除的符號

        Returns:
            [(原始路徑, 新名稱), ...] 列表
        """
        if not root_path.exists():
            return []

        targets = []

        def _scan_recursive(directory: Path) -> None:
            """遞歸掃描資料夾及其所有子資料夾"""
            try:
                for item in directory.iterdir():
                    # 跳過隱藏文件和資料夾
                    if item.name.startswith('.'):
                        continue

                    # 如果是資料夾，遞歸進入
                    if item.is_dir():
                        if rename_mode != "files":
                            # 如果需要重命名資料夾，則處理
                            new_name = item.name

                            # 1. 應用文字轉換
                            new_name = self.apply_conversion(new_name, operation, find_text, replace_text)

                            # 2. 應用格式化
                            new_name = self.apply_formatting(item, new_name, prefix, suffix, symbols)

                            targets.append((item, new_name))

                        # 遞歸掃描子資料夾
                        _scan_recursive(item)

                    # 如果是文件
                    else:
                        # 副檔名篩選
                        if filter_type == "ext" and valid_exts:
                            if item.suffix.lower() not in valid_exts:
                                continue

                        new_name = item.name

                        # 1. 應用文字轉換
                        new_name = self.apply_conversion(new_name, operation, find_text, replace_text)

                        # 2. 應用格式化
                        new_name = self.apply_formatting(item, new_name, prefix, suffix, symbols)

                        targets.append((item, new_name))

            except Exception as e:
                print(f"掃描錯誤 ({directory}): {e}")

        # 開始遞歸掃描
        _scan_recursive(root_path)
        self.targets = targets
        return targets

    def execute_rename(self, targets: List[Tuple[Path, str]]) -> Tuple[int, int]:
        """
        執行實際的文件重命名操作

        Args:
            targets: [(原始路徑, 新名稱), ...] 列表

        Returns:
            (成功數量, 失敗數量)
        """
        success = 0
        failed = 0

        for old, new in targets:
            if old.name == new:
                continue
            try:
                os.rename(old, old.parent / new)
                success += 1
            except Exception as ex:
                failed += 1
                print(f"[ERR] {old.name}: {ex}")

        return success, failed
