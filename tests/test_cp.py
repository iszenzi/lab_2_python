from unittest.mock import patch
from src.commands import cp


class TestCp:
    def test_cp_existing_file(self):
        """Тест cp с существующим файлом в существующий каталог"""
        mock_source = "/test/file.txt"
        mock_destination = "/test/dir"

        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch("os.path.exists", side_effect=[True, True]),  # source, destination
            patch("os.path.isdir", side_effect=[True, False]),  # destination, source
            patch("shutil.copy2") as mock_copy,
            patch("logging.info") as mock_logging_info,
        ):
            cp("file.txt dir")

            mock_copy.assert_called_once_with(mock_source, mock_destination)
            mock_logging_info.assert_called_once_with("cp file.txt dir")

    def test_cp_not_existing_file(self):
        """Тест cp с несуществующим файлом в существующий каталог"""
        mock_source = "/test/file.txt"
        mock_destination = "/test/dir"

        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch("os.path.exists", side_effect=[False, True]),  # source, destination
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            cp("file.txt dir")

            mock_logging_error.assert_called_once_with(
                f"ERROR: Файла '{mock_source}' не существует"
            )
            mock_print.assert_called_once_with(
                f"ERROR: Файла '{mock_source}' не существует"
            )

    def test_cp_existing_dir_with_r(self):
        """Тест cp с существующим каталогом в существующий каталог с -r"""
        mock_source = "/test/test_dir"
        mock_destination = "/test/dir"

        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch("os.path.exists", side_effect=[True, True]),  # source, destination
            patch("os.path.isdir", side_effect=[True, True]),  # destination, source
            patch("shutil.copytree") as mock_copytree,
            patch("logging.info") as mock_logging_info,
        ):
            cp("-r test_dir dir")

            mock_copytree.assert_called_once_with(
                mock_source, mock_destination, dirs_exist_ok=True
            )
            mock_logging_info.assert_called_once_with("cp -r test_dir dir")

    def test_cp_existing_dir_without_r(self):
        """Тест cp с существующим каталогом в существующий каталог без -r"""
        mock_source = "/test/test_dir"
        mock_destination = "/test/dir"

        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch("os.path.exists", side_effect=[True, True]),  # source, destination
            patch("os.path.isdir", side_effect=[True, True]),  # destination, source
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            cp("test_dir dir")

            mock_logging_error.assert_called_once_with(
                f"ERROR: '{mock_source}' является каталогом, требуется аргумент '-r'"
            )
            mock_print.assert_called_once_with(
                f"ERROR: '{mock_source}' является каталогом, требуется аргумент '-r'"
            )

    def test_cp_existing_file_with_r(self):
        """Тест cp с существующим файлом в существующий каталог с -r"""
        mock_source = "/test/file.txt"
        mock_destination = "/test/dir"

        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch("os.path.exists", side_effect=[True, True]),  # source, destination
            patch("os.path.isdir", side_effect=[True, False]),  # destination, source
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            cp("-r file.txt dir")

            mock_logging_error.assert_called_once_with(
                "ERROR: Аргумент '-r' не требуется"
            )
            mock_print.assert_called_once_with("ERROR: Аргумент '-r' не требуется")

    def test_cp_not_existing_destination(self):
        """Тест cp с существующим файлом в несуществующий каталог"""
        mock_source = "/test/file.txt"
        mock_destination = "/test/dir"

        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch("os.path.exists", side_effect=[True, False]),  # source, destination
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            cp("file.txt dir")

            mock_logging_error.assert_called_once_with(
                f"ERROR: Файла '{mock_destination}' не существует"
            )
            mock_print.assert_called_once_with(
                f"ERROR: Файла '{mock_destination}' не существует"
            )

    def test_cp_too_little_arguments(self):
        """Тест cp с недостатком аргументов"""
        with (
            patch("builtins.print") as mock_print,
            patch("logging.error") as mock_logging_error,
        ):
            cp("file.txt")

            mock_print.assert_called_once_with("ERROR: Слишком мало аргументов")
            mock_logging_error.assert_called_once_with("ERROR: Слишком мало аргументов")

    def test_cp_too_many_arguments(self):
        """Тест cp с избытком аргументов"""
        with (
            patch("builtins.print") as mock_print,
            patch("logging.error") as mock_logging_error,
        ):
            cp("file.txt dir file.txt file.txt")

            mock_print.assert_called_once_with("ERROR: Cлишком много аргументов")
            mock_logging_error.assert_called_once_with(
                "ERROR: Cлишком много аргументов"
            )

    def test_cp_unknown_flag(self):
        """Тест cp с неизвестным флагом"""
        with (
            patch("builtins.print") as mock_print,
            patch("logging.error") as mock_logging_error,
        ):
            cp("file.txt dir -x")

            mock_print.assert_called_once_with("ERROR: Незивестный флаг '-x'")
            mock_logging_error.assert_called_once_with("ERROR: Незивестный флаг '-x'")

    def test_cp_empty_path(self):
        """Тест cp с пустой строкой"""
        with (
            patch("builtins.print") as mock_print,
            patch("logging.error") as mock_logging_error,
        ):
            cp("")

            mock_print.assert_called_once_with("ERROR: Вы не ввели путь к файлу")
            mock_logging_error.assert_called_once_with(
                "ERROR: Вы не ввели путь к файлу"
            )

    def test_cp_missing_argument(self):
        """Тест cp без источника или назначения"""
        with (
            patch("builtins.print") as mock_print,
            patch("logging.error") as mock_logging_error,
        ):
            cp("-r file.txt")

            mock_print.assert_called_once_with(
                "ERROR: Источник или путь назначения не указаны"
            )
            mock_logging_error.assert_called_once_with(
                "ERROR: Источник или путь назначения не указаны"
            )
