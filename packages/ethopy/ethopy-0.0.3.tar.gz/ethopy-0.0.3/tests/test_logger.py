import pytest
from ethopy.core.Logger import Logger
from unittest.mock import Mock
from unittest.mock import patch

def mock_find_protocol_path(task_idx):
    if task_idx is not None:
        return "protocol_path"
    else:
        return False


@pytest.fixture
def mock_protocol_path(mocker):
    mocker.patch(
        "Logger.Logger._find_protocol_path", side_effect=mock_find_protocol_path
    )


config = {
    "SCHEMATA": {
        "experiment": "lab_experiments",
        "stimulus": "lab_stimuli",
        "behavior": "lab_behavior",
        "recording": "lab_recordings",
        "mice": "lab_mice",
    },
    "dj_local_conf": {
        "database.host": "127.0.0.1",
        "database.user": "root",
        "database.password": "test",
        "database.port": 3306,
        "database.reconnect": True,
        "loglevel": "WARNING",
        "database.enable_python_native_blobs": True,
    },
}


def test_init(mocker):
    mock_conn = mocker.patch("datajoint.Connection", return_value=None)
    mock_control = Mock()
    mock_control.__and__ = Mock(
        return_value=mock_control
    )  # add a __and__ method to the mock_control object
    mock_experiment = Mock()
    mock_experiment.Control = Mock(
        return_value=mock_control
    )  # set return_value to the mock_control object
    mock_schemata = {
        "experiment": mock_experiment,
        # add other keys if needed
    }
    mock_init_schemata = mocker.patch(
        "ethopy.core.Logger.Logger._initialize_schemata", return_value=mock_schemata
    )
    mocker.patch.dict("ethopy.core.Logger.config", config)
    mock_log_setup = mocker.patch(
        "ethopy.core.Logger.Logger._log_setup", return_value=None
    )
    mock_log_sync_setup_info = mocker.patch(
        "ethopy.core.Logger.Logger._sync_setup_info", return_value=True
    )
    mock_log_inserter = mocker.patch(
        "ethopy.core.Logger.Logger.inserter", return_value=True
    )

    mocker.patch(
        "ethopy.core.Logger.Logger._find_protocol_path",
        side_effect=mock_find_protocol_path,
    )

    logger = Logger()
    assert logger.setup is not None
    assert logger.is_pi is not None
    assert logger.task_idx is None
    assert logger.protocol_path is None
    assert logger.manual_run is False
    assert logger.setup_status == "ready"
    assert logger.writer is not None
    assert logger.rec_fliptimes is True
    assert logger.trial_key == {"animal_id": 0, "session": 1, "trial_idx": 0}
    assert logger.setup_info == {}
    assert logger.datasets == {}
    assert logger.lock is False
    assert logger.queue is not None
    assert logger.ping_timer is not None
    assert logger.logger_timer is not None
    assert logger.total_reward == 0
    assert logger.curr_state == ""
    # assert logger.private_conn is not None
    assert logger._schemata is not None
    assert logger.source_path == logger.DEFAULT_SOURCE_PATH
    assert logger.target_path == logger.DEFAULT_TARGET_PATH
    assert logger.thread_end is not None
    assert logger.thread_lock is not None
    assert logger.inserter_thread is not None
    assert logger.getter_thread is not None


def test_parse_protocol(mocker):
    mock_conn = mocker.patch("datajoint.Connection", return_value=None)
    mock_control = Mock()
    mock_control.__and__ = Mock(
        return_value=mock_control
    )  # add a __and__ method to the mock_control object
    mock_experiment = Mock()
    mock_experiment.Control = Mock(
        return_value=mock_control
    )  # set return_value to the mock_control object
    mock_schemata = {
        "experiment": mock_experiment,
        # add other keys if needed
    }
    mock_init_schemata = mocker.patch(
        "ethopy.core.Logger.Logger._initialize_schemata", return_value=mock_schemata
    )
    mocker.patch.dict("ethopy.core.Logger.config", config)
    mock_log_setup = mocker.patch(
        "ethopy.core.Logger.Logger._log_setup", return_value=None
    )
    mock_log_sync_setup_info = mocker.patch(
        "ethopy.core.Logger.Logger._sync_setup_info", return_value=True
    )
    mock_log_inserter = mocker.patch(
        "ethopy.core.Logger.Logger.inserter", return_value=True
    )

    mocker.patch(
        "ethopy.core.Logger.Logger._find_protocol_path",
        side_effect=mock_find_protocol_path,
    )

    logger = Logger()
    assert logger._parse_protocol("123") == (123, logger._find_protocol_path(123))
    assert logger._parse_protocol("test_protocol") == (None, "test_protocol")
    assert logger._parse_protocol(None) == (None, None)


def test_update_protocol(mocker):
    mock_conn = mocker.patch("datajoint.Connection", return_value=None)
    mock_control = Mock()
    mock_control.__and__ = Mock(
        return_value=mock_control
    )  # add a __and__ method to the mock_control object
    mock_experiment = Mock()
    mock_experiment.Control = Mock(
        return_value=mock_control
    )  # set return_value to the mock_control object
    mock_schemata = {
        "experiment": mock_experiment,
        # add other keys if needed
    }
    mock_init_schemata = mocker.patch(
        "ethopy.core.Logger.Logger._initialize_schemata", return_value=mock_schemata
    )
    mocker.patch.dict("ethopy.core.Logger.config", config)
    mock_log_setup = mocker.patch(
        "ethopy.core.Logger.Logger._log_setup", return_value=None
    )
    mock_log_sync_setup_info = mocker.patch(
        "ethopy.core.Logger.Logger._sync_setup_info", return_value=True
    )
    mock_log_inserter = mocker.patch(
        "ethopy.core.Logger.Logger.inserter", return_value=True
    )

    mocker.patch(
        "ethopy.core.Logger.Logger._find_protocol_path",
        side_effect=mock_find_protocol_path,
    )

    logger = Logger()
    # assert logger.update_protocol() is False
    logger.manual_run = True
    logger.protocol_path = "non_existent_file"
    assert logger.update_protocol() is False


def test_protocol_path(mocker):
    mock_conn = mocker.patch("datajoint.Connection", return_value=None)
    mock_control = Mock()
    mock_control.__and__ = Mock(
        return_value=mock_control
    )  # add a __and__ method to the mock_control object
    mock_experiment = Mock()
    mock_experiment.Control = Mock(
        return_value=mock_control
    )  # set return_value to the mock_control object
    mock_schemata = {
        "experiment": mock_experiment,
        # add other keys if needed
    }
    mock_init_schemata = mocker.patch(
        "ethopy.core.Logger.Logger._initialize_schemata", return_value=mock_schemata
    )
    mocker.patch.dict("ethopy.core.Logger.config", config)
    mock_log_setup = mocker.patch(
        "ethopy.core.Logger.Logger._log_setup", return_value=None
    )
    mock_log_sync_setup_info = mocker.patch(
        "ethopy.core.Logger.Logger._sync_setup_info", return_value=True
    )
    mock_log_inserter = mocker.patch(
        "ethopy.core.Logger.Logger.inserter", return_value=True
    )

    mocker.patch(
        "ethopy.core.Logger.Logger._find_protocol_path",
        side_effect=mock_find_protocol_path,
    )

    logger = Logger()
    logger.protocol_path = "test_protocol"
    assert (
        logger.protocol_path[-(len("test_protocol") + 9) :] == "/../conf/test_protocol"
    )
    logger.protocol_path = "/path/to/test_protocol"
    assert logger.protocol_path == "/path/to/test_protocol"
