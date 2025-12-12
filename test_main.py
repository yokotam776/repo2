from fastapi.testclient import TestClient
from datetime import datetime
from main import app

client = TestClient(app)


def test_get_current_datetime():
    """現在の日時を返すAPIのテスト"""
    response = client.get("/datetime")
    
    # ステータスコードのチェック
    assert response.status_code == 200
    
    # レスポンスのJSONデータを取得
    data = response.json()
    
    # 必要なフィールドが含まれているかチェック
    assert "datetime" in data
    assert "timestamp" in data
    
    # datetimeフィールドがISO形式であることを確認
    datetime_str = data["datetime"]
    parsed_datetime = datetime.fromisoformat(datetime_str)
    assert isinstance(parsed_datetime, datetime)
    
    # timestampが数値であることを確認
    assert isinstance(data["timestamp"], (int, float))
    
    # timestampが現在時刻に近いことを確認（過去1分以内）
    current_timestamp = datetime.now().timestamp()
    assert abs(current_timestamp - data["timestamp"]) < 60


def test_datetime_format():
    """返される日時形式のテスト"""
    response = client.get("/datetime")
    data = response.json()
    
    # ISO形式の日時文字列をパース
    datetime_obj = datetime.fromisoformat(data["datetime"])
    
    # 年、月、日が妥当な範囲であることを確認
    assert 2000 <= datetime_obj.year <= 3000
    assert 1 <= datetime_obj.month <= 12
    assert 1 <= datetime_obj.day <= 31


def test_multiple_requests():
    """複数回リクエストして異なる時刻が返されることを確認"""
    import time
    
    response1 = client.get("/datetime")
    time.sleep(0.1)  # 少し待つ
    response2 = client.get("/datetime")
    
    data1 = response1.json()
    data2 = response2.json()
    
    # 2回目のリクエストのタイムスタンプが1回目以降であることを確認
    assert data2["timestamp"] >= data1["timestamp"]
