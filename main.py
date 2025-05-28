import streamlit as st
import requests
import datetime
import pytz
import random

# ==== OpenWeatherMap 設定 ====
API_KEY = "11e1ae55357eb1c7ab1b8823783fa5c9"
LANG = "zh_tw"
UNITS = "metric"

# ==== 中文星期對照 ====
weekdays = {
    0: "星期一", 1: "星期二", 2: "星期三",
    3: "星期四", 4: "星期五", 5: "星期六", 6: "星期日"
}

# ==== 自動取得使用者城市與時區 ====
def get_location():
    try:
        ip_info = requests.get("https://ipapi.co/json", timeout=5).json()
        city = ip_info.get("city", "Hsinchu")
        timezone_str = ip_info.get("timezone", "Asia/Taipei")
        tz = pytz.timezone(timezone_str)
    except Exception as e:
        st.warning(f"⚠️ 無法取得位置資訊，使用預設：Hsinchu\n（錯誤訊息：{e}）")
        city = "Hsinchu"
        tz = pytz.timezone("Asia/Taipei")
    return city, tz

CITY, TZ = get_location()

# ==== 取得時間 ====
now = datetime.datetime.now(TZ)
date_str = now.strftime("%Y/%m/%d")
weekday_ch = weekdays[now.weekday()]
time_str = now.strftime("%H:%M")

# ==== 取得天氣 ====
try:
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}&lang={LANG}"
    response = requests.get(weather_url)
    weather_data = response.json()
    weather_desc = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]
except Exception as e:
    weather_desc = f"天氣取得失敗：{e}"
    temp = "--"

# ==== 語錄清單（2 or 3 欄皆可）====
quotes_raw = [
    ("我靠著那加給我力量的，凡事都能做。", "I can do all things through Christ who strengthens me."),
    ("耶和華是我的牧者，我必不致缺乏。", "The Lord is my shepherd; I shall not want.", "詩篇 23:1"),
    # 可自行加入更多語錄
]

# ==== 語錄標準化 ====
def normalize_quotes(quotes):
    normalized = []
    for q in quotes:
        if len(q) == 2:
            zh, en = q
            ref = ""
        elif len(q) == 3:
            zh, en, ref = q
        else:
            zh, en, ref = "⚠️ 格式錯誤", "Invalid format", ""
        normalized.append((zh, en, ref))
    return normalized

quotes = normalize_quotes(quotes_raw)

# ==== 行動選項 ====
all_actions = [
    "努力", "奮起", "開心", "放鬆", "陪伴", "深呼吸", "快樂", "原諒自己", "學習新事物", "讚美別人"
]

# ==== 初次載入隨機設定 ====
if "quote" not in st.session_state:
    st.session_state.quote = random.choice(quotes)

if "options" not in st.session_state:
    st.session_state.options = random.sample(all_actions, 3)

quote_ch, quote_en, quote_ref = st.session_state.quote
options = st.session_state.options

# ==== 顯示畫面 ====
st.markdown(f"""
## 📍 位置：**{CITY}**
### 📅 {date_str}（{weekday_ch}）
### 🕰️ 時間：{time_str}
### 🌤️ 天氣：{weather_desc}，氣溫 {temp}°C
---
""")

st.subheader("✨ 今日小語：")
st.write(f"📖 {quote_ch}" + (f"（{quote_ref}）" if quote_ref else ""))
st.write(f"_🕊️ {quote_en}_")

st.markdown("---\n### 🎯 今日選項（請選擇你今天想實踐的行動）")
user_choice = st.radio("請選擇：", options)

if st.button("✨ 我決定了！"):
    st.success(f"🧡 我決定今天要：「{user_choice}」！一起加油吧 👑✨")
