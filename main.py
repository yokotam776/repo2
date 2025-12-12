from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/datetime")
async def get_current_datetime():
    """現在の日時を返すAPIエンドポイント"""
    current_time = datetime.now()
    return {
        "datetime": current_time.isoformat(),
        "timestamp": current_time.timestamp()
    }
