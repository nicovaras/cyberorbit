from core.streak import update_streak
from datetime import datetime

def test_update_streak_advances():
    updated = update_streak()
    assert "streak" in updated
    assert "last_used" in updated
    assert updated["streak"] in [1, 3]  # reset or increment depending on current date
    datetime.strptime(updated["last_used"], "%Y-%m-%d")
