import os
import pytest
from unittest.mock import patch, MagicMock


def test_main_uses_environment_variables():
    """データベース接続情報が環境変数から取得されることをテスト"""
    # 環境変数を設定
    test_env = {
        "DB_HOST": "test-host",
        "DB_NAME": "test-database",
        "DB_USER": "test-user",
        "DB_PASSWORD": "test-password",
        "DB_PORT": "5433"
    }
    
    with patch.dict(os.environ, test_env, clear=False):
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value = MagicMock()
            
            # Import inside test to ensure environment variables are set before module loads
            from app import main
            main()
            
            # psycopg2.connectが正しい引数で呼ばれたことを確認
            mock_connect.assert_called_once_with(
                host="test-host",
                database="test-database",
                user="test-user",
                password="test-password",
                port="5433"
            )


def test_main_uses_default_values():
    """デフォルト値が正しく使用されることをテスト"""
    # DB_HOSTとDB_PORTを設定せずに、その他の必須環境変数のみ設定
    test_env = {
        "DB_NAME": "test-database",
        "DB_USER": "test-user",
        "DB_PASSWORD": "test-password"
    }
    
    # DB_HOSTとDB_PORTが環境変数に存在しないことを確認するため、明示的に削除
    env_without_defaults = os.environ.copy()
    env_without_defaults.pop("DB_HOST", None)
    env_without_defaults.pop("DB_PORT", None)
    env_without_defaults.update(test_env)
    
    with patch.dict(os.environ, env_without_defaults, clear=True):
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value = MagicMock()
            
            # Import inside test to ensure environment variables are set before module loads
            from app import main
            main()
            
            # デフォルト値が使用されることを確認
            mock_connect.assert_called_once_with(
                host="localhost",  # デフォルト値
                database="test-database",
                user="test-user",
                password="test-password",
                port="5432"  # デフォルト値
            )


def test_main_with_custom_port():
    """カスタムポート番号が正しく使用されることをテスト"""
    test_env = {
        "DB_HOST": "custom-host",
        "DB_NAME": "test-database",
        "DB_USER": "test-user",
        "DB_PASSWORD": "test-password",
        "DB_PORT": "3306"  # 非標準ポート
    }
    
    with patch.dict(os.environ, test_env, clear=False):
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value = MagicMock()
            
            # Import inside test to ensure environment variables are set before module loads
            from app import main
            main()
            
            mock_connect.assert_called_once_with(
                host="custom-host",
                database="test-database",
                user="test-user",
                password="test-password",
                port="3306"
            )
