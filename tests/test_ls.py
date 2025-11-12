from unittest.mock import patch
from src.get_ls import ls


class TestLs:
    def test_ls_current_dir(self):
        """Тест ls в текущем каталоге"""
        mock_cwd = "/test"
        mock_files = ["file1.txt", "dir", "file2.txt"]

        with (
            patch("os.getcwd", return_value=mock_cwd),
            patch("os.path.abspath", return_value=mock_cwd),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", side_effect=[True, False, True, False]),
            patch("os.path.isfile", side_effect=[True, True]),
            patch("os.listdir", return_value=mock_files),
            patch("builtins.print") as mock_print,
            patch("logging.info") as mock_logging_info,
        ):
            ls("")

        mock_print.assert_any_call(f"\n{mock_cwd}:\n")
        mock_print.assert_any_call("FILE file1.txt")
        mock_print.assert_any_call("DIR dir")
        mock_print.assert_any_call("FILE file2.txt")
        mock_logging_info.assert_called_once_with("ls ")

    def test_ls_parent_dir(self):
        """Тест ls в родительском каталоге"""
        mock_cwd = "/test/dir"
        mock_parent = "/test"
        mock_files = ["dir", "file.txt"]

        with (
            patch("os.getcwd", return_value=mock_cwd),
            patch("os.path.dirname", return_value=mock_parent),
            patch("os.path.abspath", return_value=mock_parent),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", side_effect=[True, True, False]),
            patch("os.path.isfile", side_effect=[True]),
            patch("os.listdir", return_value=mock_files),
            patch("builtins.print") as mock_print,
            patch("logging.info") as mock_logging_info,
        ):
            ls("..")

            mock_print.assert_any_call(f"\n{mock_parent}:\n")
            mock_print.assert_any_call("DIR dir")
            mock_print.assert_any_call("FILE file.txt")
            mock_logging_info.assert_called_once_with("ls ..")

    def test_ls_not_existing_path(self):
        """Тест ls с несуществующем путем"""
        mock_path = "/test/dir"

        with (
            patch("os.path.abspath", return_value=mock_path),
            patch("os.path.exists", return_value=False),
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            ls("dir")

            mock_logging_error.assert_called_once_with(
                f"ERROR: Файла '{mock_path}' не существует"
            )
            mock_print.assert_any_call(
                f"\n{f"ERROR: Файла '{mock_path}' не существует"}"
            )

    def test_ls_not_dir(self):
        """Тест ls с файлом"""
        mock_path = "/test/file.txt"

        with (
            patch("os.path.abspath", return_value=mock_path),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", return_value=False),
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            ls("file.txt")

            mock_logging_error.assert_called_once_with(
                f"ERROR: '{mock_path}' не является каталогом"
            )
            mock_print.assert_any_call(
                f"\n{f"ERROR: '{mock_path}' не является каталогом"}"
            )

    def test_ls_unknown_flag(self):
        """Тест ls с неизвестным флагом"""
        with (
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            ls("-x")

            mock_logging_error.assert_called_once_with("ERROR: Неизвестный флаг '-x'")
            mock_print.assert_called_once_with("ERROR: Неизвестный флаг '-x'")
