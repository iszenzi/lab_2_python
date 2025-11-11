from unittest.mock import patch
from src.commands import cd


class TestCd:
    def test_cd_existing_dir(self):
        """Тест cd с существующим каталогом"""
        mock_path = "/test"
        with (
            patch("os.path.abspath", return_value=mock_path),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", return_value=True),
            patch("os.chdir") as mock_chdir,
            patch("logging.info") as mock_logging_info,
        ):
            cd(mock_path)

            mock_chdir.assert_called_once_with(mock_path)

            mock_logging_info.assert_called_once_with(f"cd {mock_path}")

    def test_cd_not_existing_diк(self):
        """Тест cd с несуществующим каталогом"""
        mock_path = "/test"
        with (
            patch("os.path.abspath", return_value=mock_path),
            patch("os.path.exists", return_value=False),
            patch("os.path.isdir", return_value=False),
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            cd(mock_path)

            mock_logging_error.assert_called_once_with(
                f"ERROR: Пути '{mock_path}' не существует"
            )
            mock_print.assert_called_once_with(
                f"ERROR: Пути '{mock_path}' не существует"
            )

    def test_cd_not_dir(self):
        """Тест cd с файлом"""
        mock_path = "/test"
        with (
            patch("os.path.abspath", return_value=mock_path),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", return_value=False),
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            cd(mock_path)

            mock_logging_error.assert_called_once_with(
                f"ERROR: '{mock_path}' не является каталогом"
            )
            mock_print.assert_called_once_with(
                f"ERROR: '{mock_path}' не является каталогом"
            )

    def test_cd_too_many_arguments(self):
        """Тест cd с избытком аргументами"""
        with (
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            cd("first test ")

            mock_logging_error.assert_called_once_with(
                "ERROR: Слишком много аргументов"
            )
            mock_print.assert_called_once_with("ERROR: Слишком много аргументов")

    def test_cd_current_dir(self):
        """Тест cd в текущий каталог"""
        with patch("logging.info") as mock_logging_info:
            cd(".")
            mock_logging_info.assert_called_once_with("cd .")

    def test_cd_parent_dir(self):
        """Тест cd в родительский каталог"""
        mock_path = "/dir"
        mock_path_dirname = "/test"
        with (
            patch("os.getcwd", return_value=mock_path),
            patch("os.path.dirname", return_value=mock_path_dirname),
            patch("os.path.abspath", return_value=mock_path_dirname),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", return_value=True),
            patch("os.chdir") as mock_chdir,
            patch("logging.info") as mock_logging_info,
        ):
            cd("..")

            mock_chdir.assert_called_once_with(mock_path_dirname)
            mock_logging_info.assert_called_once_with(f"cd {mock_path_dirname}")

    def test_cd_home_dir(self):
        """Тест cd в домашний каталог"""
        mock_path = "/home/user/Илья"
        with (
            patch("os.path.expanduser", return_value=mock_path),
            patch("os.path.abspath", return_value=mock_path),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", return_value=True),
            patch("os.chdir") as mock_chdir,
            patch("logging.info") as mock_logging_info,
        ):
            cd("~")

            mock_chdir.assert_called_once_with(mock_path)
            mock_logging_info.assert_called_once_with(f"cd {mock_path}")
