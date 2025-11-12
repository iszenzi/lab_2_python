from unittest.mock import patch
from src.commands import mv


class TestMv:
    def test_mv_rename_file(self):
        """Тест mv для переименования файла"""
        mock_source = "/test/old.txt"
        mock_destination = "/test/new.txt"
        mock_destination_dirname = "/test"
        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch(
                "os.path.exists", side_effect=[True, True, False, False]
            ),  # source, dirname, destination, destination в элиф
            patch("os.path.dirname", return_value=mock_destination_dirname),
            patch("os.access", side_effect=[True, True]),  # source R, dirname W
            patch("os.path.isdir", return_value=False),  # destination
            patch("os.path.isfile", return_value=False),  # destination
            patch("shutil.move") as mock_move,
            patch("logging.info") as mock_logging_info,
        ):
            mv("old.txt new.txt")

            mock_move.assert_called_once_with(mock_source, mock_destination)
            mock_logging_info.assert_called_once_with("mv old.txt new.txt")

    def test_mv_rename_dir(self):
        """Тест mv для переименования каталога"""
        mock_source = "/test/old"
        mock_destination = "/test/new"
        mock_destination_dirname = "/test"
        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch(
                "os.path.exists", side_effect=[True, True, False, False]
            ),  # source, dirname, destination, destination в элиф
            patch("os.path.dirname", return_value=mock_destination_dirname),
            patch("os.access", side_effect=[True, True]),  # source R, dirname W
            patch("os.path.isdir", return_value=False),  # destination
            patch("os.path.isfile", return_value=False),  # destination
            patch("shutil.move") as mock_move,
            patch("logging.info") as mock_logging_info,
        ):
            mv("old new")

            mock_move.assert_called_once_with(mock_source, mock_destination)
            mock_logging_info.assert_called_once_with("mv old new")

    def test_mv_file_to_dir(self):
        """Тест mv файла в существующий каталог"""
        mock_source = "/test/file.txt"
        mock_destination = "/test/dir"
        mock_destination_dirname = "/test"
        mock_new_destination = "/test/dir/file.txt"

        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch(
                "os.path.exists", side_effect=[True, True, True, False]
            ),  # source, dirname, destination, new_destination
            patch("os.path.dirname", return_value=mock_destination_dirname),
            patch("os.access", side_effect=[True, True]),  # source R, dirname W
            patch("os.path.isdir", return_value=True),  # destination is dir
            patch("os.path.join", return_value=mock_new_destination),
            patch("os.path.isfile", return_value=False),  # destination
            patch("shutil.move") as mock_move,
            patch("logging.info") as mock_logging_info,
        ):
            mv("file.txt dir")

            mock_move.assert_called_once_with(mock_source, mock_new_destination)
            mock_logging_info.assert_called_once_with("mv file.txt dir")

    def test_mv_not_existing_file(self):
        """Тест mv с несуществующим файлом в существующий каталог"""
        mock_source = "/test/file.txt"
        mock_destination = "/test/dir"

        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch(
                "os.path.exists", side_effect=[False, True, True, False]
            ),  # source, dirname, destination, new_destination
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            mv("file.txt dir")

            mock_logging_error.assert_called_once_with(
                f"ERROR: Файла '{mock_source}' не существует"
            )
            mock_print.assert_called_once_with(
                f"ERROR: Файла '{mock_source}' не существует"
            )

    def test_mv_not_existing_destination_dirname(self):
        """Тест mv с несуществующем destination_dirname"""
        mock_source = "/test/file.txt"
        mock_destination = "/test/dir/file.txt"
        mock_destination_dirname = "/test/dir"

        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch("os.path.exists", side_effect=[True, False]),  # source, dirname
            patch("os.path.dirname", return_value=mock_destination_dirname),
            patch("os.access", return_value=True),
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            mv("file.txt dir/file.txt")

            mock_logging_error.assert_called_once_with(
                f"ERROR: Каталога '{mock_destination_dirname}' не существует"
            )
            mock_print.assert_called_once_with(
                f"ERROR: Каталога '{mock_destination_dirname}' не существует"
            )

    def test_mv_no_r_access_file(self):
        """Тест mv без прав чтения источника"""
        mock_source = "/test/file.txt"
        mock_destination = "/test/dir"

        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch("os.path.exists", return_value=True),  # source
            patch("os.access", return_value=False),  # source R
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            mv("file.txt dir")

            mock_logging_error.assert_called_once_with(
                f"ERROR: Нет прав на чтение '{mock_source}'"
            )
            mock_print.assert_called_once_with(
                f"ERROR: Нет прав на чтение '{mock_source}'"
            )

    def test_mv_no_w_access_dir(self):
        """Тест mv без прав записи в destination_dirname"""
        mock_source = "/test/file.txt"
        mock_destination = "/test/dir"
        mock_destination_dirname = "/test"
        with (
            patch("os.path.abspath", side_effect=[mock_source, mock_destination]),
            patch(
                "os.path.exists", side_effect=[True, True, True]
            ),  # source, dirname, destination
            patch("os.path.dirname", return_value=mock_destination_dirname),
            patch("os.access", side_effect=[True, False]),  # source R, dirname W
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            mv("file.txt dir")

            mock_logging_error.assert_called_once_with(
                f"ERROR: Нет прав на запись в каталог '{mock_destination_dirname}'"
            )
            mock_print.assert_called_once_with(
                f"ERROR: Нет прав на запись в каталог '{mock_destination_dirname}'"
            )

    def test_cp_too_little_arguments(self):
        """Тест mv с недостатком аргументов"""
        with (
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            mv("file.txt")

            mock_logging_error.assert_called_once_with("ERROR: Слишком мало аргументов")
            mock_print.assert_called_once_with("ERROR: Слишком мало аргументов")

    def test_mv_too_many_arguments(self):
        """Тест mv с избытком аргументов"""
        with (
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            mv("file.txt file1.txt file2.txt")

            mock_logging_error.assert_called_once_with(
                "ERROR: Слишком много аргументов"
            )
            mock_print.assert_called_once_with("ERROR: Слишком много аргументов")

    def test_mv_empty_path(self):
        """Тест mv с пустой строкой"""
        with (
            patch("logging.error") as mock_logging_error,
            patch("builtins.print") as mock_print,
        ):
            mv("")

            mock_logging_error.assert_called_once_with(
                "ERROR: Вы не ввели путь к файлу"
            )
            mock_print.assert_called_once_with("ERROR: Вы не ввели путь к файлу")
