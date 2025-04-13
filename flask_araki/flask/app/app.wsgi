import sys
import os

# Flaskアプリのパスを設定
sys.path.insert(0, "C:/Users/kogaa/myproject/flask/app")

# 環境変数を設定（必要に応じて）
os.environ['PYTHON_EGG_CACHE'] = 'C:/Users/kogaa/myproject/flask/app/.egg-cache'

# Flaskアプリをインポート
from app import app as application  # Flaskアプリをインポート
