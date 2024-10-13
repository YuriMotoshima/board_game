
import os
import tempfile
from datetime import datetime

from app.config.log import loginit


def test_loginit_injection():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Use um caminho válido dentro do diretório temporário
        log_file_name = os.path.join(temp_dir, "TestLog")
        loginit(name_file_log=log_file_name, dev_env="DEV", disable_log=False)

        log_file_path = os.path.join(
            temp_dir, "logs", f"[DEV] TestLog - {datetime.now().strftime('%d-%m-%Y %H')}.log"
        )

        assert not os.path.exists(log_file_path)
