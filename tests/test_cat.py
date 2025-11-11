from unittest.mock import patch, mock_open
from src.commands import cat


class TestCat:
    def test_cat_existing_file(self):
        """Тест cat с существующим файлом"""
        mock_path = "/test/file.txt"
        mock_content = "TEST\nTEST TEST\nTEEEEEEST TEST TEST"
        with (
            patch("builtins.open", mock_open(read_data=mock_content)) as mock_file,
            patch("os.path.abspath", return_value=mock_path),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", return_value=False),
            patch("builtins.print") as mock_print,
            patch("logging.info") as mock_logging_info,
        ):
            cat(mock_path)

            mock_file.assert_called_once_with(mock_path, "r", encoding="utf-8")
            mock_print.assert_any_call("TEST\n", end="")
            mock_print.assert_any_call("TEST TEST\n", end="")
            mock_print.assert_any_call("TEEEEEEST TEST TEST", end="")
            mock_logging_info.assert_called_once_with(f"cat {mock_path}")

    def test_cat_not_existing_diк(self):
        """Тест cat с несуществующим файлом"""
        mock_path = "/test/file.txt"
        with (
            patch("os.path.abspath", return_value=mock_path),
            patch("os.path.exists", return_value=False),
            patch("builtins.print") as mock_print,
            patch("logging.error") as mock_logging_error,
        ):
            cat(mock_path)

            mock_logging_error.assert_called_once_with(
                f"ERROR: Файла '{mock_path}' не существует"
            )
            mock_print.assert_called_once_with(
                f"ERROR: Файла '{mock_path}' не существует"
            )

    def test_cat_not_file(self):
        """Тест cat с каталогом"""
        mock_path = "/test/dir"
        with (
            patch("os.path.abspath", return_value=mock_path),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", return_value=True),
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            cat(mock_path)

            mock_logging_error.assert_called_once_with(
                f"ERROR: '{mock_path}' является каталогом"
            )
            mock_print.assert_called_once_with(
                f"ERROR: '{mock_path}' является каталогом"
            )

    def test_cat_too_many_argument(self):
        """Тест cat с несколькими аргументами"""
        with (
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            cat("/file1.txt /file2.txt")

            mock_logging_error.assert_called_once_with(
                "ERROR: Слишком много аргументов"
            )
            mock_print.assert_called_once_with("ERROR: Слишком много аргументов")

    def test_cat_empty_path(self):
        """Тест cat с пустой строкой"""
        with (
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            cat("")

            mock_logging_error.assert_called_once_with(
                "ERROR: Вы не ввели путь к файлу"
            )
            mock_print.assert_called_once_with("ERROR: Вы не ввели путь к файлу")
