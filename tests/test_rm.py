from unittest.mock import patch
from src.get_rm import rm


class TestRm:
    def test_rm_existing_file(self):
        """Тест rm с существующим файлом"""
        mock_path = "/test/file.txt"
        mock_parent = "/mock"

        with (
            patch(
                "os.path.abspath",
                side_effect=[mock_path, "/", mock_parent, mock_parent],
            ),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", return_value=False),
            patch("os.remove") as mock_remove,
            patch("logging.info") as mock_logging_info,
        ):
            rm("file.txt")

            mock_remove.assert_called_once_with(mock_path)
            mock_logging_info.assert_called_once_with("rm file.txt")

    def test_rm_not_existing_file(self):
        """Тест rm с несуществующим путём"""
        mock_path = "/test/file.txt"
        mock_parent = "/mock"

        with (
            patch(
                "os.path.abspath",
                side_effect=[mock_path, "/", mock_parent, mock_parent],
            ),
            patch("os.path.exists", return_value=False),
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            rm("file.txt")

            mock_logging_error.assert_called_once_with(
                f"ERROR: Файла '{mock_path}' не существует"
            )
            mock_print.assert_called_once_with(
                f"ERROR: Файла '{mock_path}' не существует"
            )

    def test_rm_dir_with_r(self):
        """Тест rm каталога с -r"""
        mock_path = "/test/dir"
        mock_parent = "/mock"

        with (
            patch(
                "os.path.abspath",
                side_effect=[mock_path, "/", mock_parent, mock_parent],
            ),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", return_value=True),
            patch("os.access", return_value=True),
            patch("builtins.input", return_value="y"),
            patch("shutil.rmtree") as mock_rmtree,
            patch("logging.info") as mock_logging_info,
        ):
            rm("-r dir")

            mock_rmtree.assert_called_once_with(mock_path)
            mock_logging_info.assert_called_once_with("rm -r dir")

    def test_rm_dir_without_r(self):
        """Тест rm каталога без -r"""
        mock_path = "/test/dir"
        mock_parent = "/mock"

        with (
            patch(
                "os.path.abspath",
                side_effect=[mock_path, "/", mock_parent, mock_parent],
            ),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", return_value=True),
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            rm("dir")

            mock_logging_error.assert_called_once_with(
                f"ERROR: '{mock_path}' является каталогом, требуется аргумент '-r'"
            )
            mock_print.assert_called_once_with(
                f"ERROR: '{mock_path}' является каталогом, требуется аргумент '-r'"
            )

    def test_rm_dir_with_r_cancel(self):
        """Тест rm отмены удаления каталога с -r"""
        mock_path = "/test/dir"
        mock_parent = "/mock"

        with (
            patch(
                "os.path.abspath",
                side_effect=[mock_path, "/", mock_parent, mock_parent],
            ),
            patch("os.path.exists", return_value=True),
            patch("os.path.isdir", return_value=True),
            patch("builtins.input", return_value="n"),
            patch("builtins.print") as mock_print,
        ):
            rm("-r dir")

            mock_print.assert_called_once_with("Удаление отменено")

    def test_rm_root_dir(self):
        """Тест rm корневого каталога"""
        with (
            patch("os.path.abspath", side_effect=["/", "/"]),
            patch("os.path.exists", return_value=True),
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            rm("/")

            mock_logging_error.assert_called_once_with(
                "ERROR: Нельзя удалить корневой каталог"
            )
            mock_print.assert_called_once_with("ERROR: Нельзя удалить корневой каталог")

    def test_rm_parent_dir(self):
        """Тест rm родительского каталога"""
        mock_parent = "/test"

        with (
            patch(
                "os.path.abspath",
                side_effect=[mock_parent, "/", mock_parent, mock_parent],
            ),
            patch("os.path.exists", return_value=True),
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            rm("..")

            mock_logging_error.assert_called_once_with(
                "ERROR: Нельзя удалить родительский каталог"
            )
            mock_print.assert_called_once_with(
                "ERROR: Нельзя удалить родительский каталог"
            )

    def test_rm_too_many_arguments(self):
        """Тест rm с избытком аргументов"""
        with (
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            rm("file.txt file1.txt file2.txt")

            mock_logging_error.assert_called_once_with(
                "ERROR: Cлишком много аргументов"
            )
            mock_print.assert_called_once_with("ERROR: Cлишком много аргументов")

    def test_rm_empty_path(self):
        """Тест rm с пустой строкой"""
        with (
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            rm("")

            mock_logging_error.assert_called_once_with(
                "ERROR: Вы не ввели путь к файлу"
            )
            mock_print.assert_called_once_with("ERROR: Вы не ввели путь к файлу")

    def test_rm_unknown_flag(self):
        """Тест rm с неизвестным флагом"""
        with (
            patch("builtins.print") as mock_print,
            patch("logging.error") as mock_logging_error,
        ):
            rm("file.txt -x")

            mock_print.assert_called_once_with("ERROR: Неизвестный флаг '-x'")
            mock_logging_error.assert_called_once_with("ERROR: Неизвестный флаг '-x'")
