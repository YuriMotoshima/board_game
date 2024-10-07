import os
import shutil
from datetime import datetime

from app.config.log import loginit


def test_loginit_injection():
    loginit(name_file_log="TestLog/../Evil", dev_env="DEV", disable_log=False)
    assert not os.path.exists(os.path.join(os.getcwd(), "logs", f"{os.getcwd()}\\logs", f"[DEV] TestLog/../Evil - {datetime.now().strftime('%d-%m-%Y %H')}.log"))
    # shutil.rmtree('./logs')

