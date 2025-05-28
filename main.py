import streamlit as st
import requests
import datetime
import pytz
import random

# ==== OpenWeatherMap 設定 ====
API_KEY = "你的API金鑰"  # 請自行填入
LANG = "zh_tw"
UNITS = "metric"

# ==== 中文星期對照 ====
weekdays = {
    0: "星期一", 1: "星期二", 2: "星期三",
    3: "星期四", 4: "星期五", 5: "星期六", 6: "星期日"
}

# ==== 取得使用者地理位置與時區 ====
def get_location():
    try:
        ip_info = requests.get("https://ipapi.co/json").json()
        city = ip_info.get("city", "Hsinchu")
        timezone_str = ip_info.get("timezone", "Asia/Taipei")
        tz = pytz.timezone(timezone_str)
    except:
        city = "Hsinchu"
        tz = pytz.timezone("Asia/Taipei")
    return city, tz

CITY, TZ = get_location()

# ==== 時間處理 ====
now = datetime.datetime.now(TZ)
date_str = now.strftime("%Y/%m/%d")
weekday_ch = weekdays[now.weekday()]
time_str = now.strftime("%H:%M")

# ==== 天氣資料 ====
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}&lang={LANG}"
try:
    response = requests.get(weather_url)
    weather_data = response.json()
    weather_desc = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]
except:
    weather_desc = "取得失敗"
    temp = "--"

# ==== 語錄清單（可為2欄或3欄）====
quotes_raw = [
    ("我靠著那加給我力量的，凡事都能做。", "I can do all things through Christ who strengthens me."),
    ("耶和華是我的牧者，我必不致缺乏。", "The Lord is my shepherd; I shall not want.", "詩篇 23:1"),
    # ... ← 這裡請貼入你所有語錄資料
]

# ==== 語錄標準化處理 ====
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
    # ... 可加到更多
]

# ==== 隨機狀態儲存 ====
if "quote" not in st.session_state:
    st.session_state.quote = random.choice(quotes)

if "options" not in st.session_state:
    st.session_state.options = random.sample(all_actions, 3)

quote_ch, quote_en, quote_ref = st.session_state.quote
options = st.session_state.options

# ==== 畫面顯示 ====
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
