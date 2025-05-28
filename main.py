import streamlit as st
import requests
import datetime
import pytz
import random

# ==== 設定 ====
API_KEY = "11e1ae55357eb1c7ab1b8823783fa5c9"  # OpenWeatherMap API Key
CITY = "Hsinchu"
LANG = "zh_tw"
UNITS = "metric"
TZ = pytz.timezone("Asia/Taipei")

# ==== 中文星期對照 ====
weekdays = {
    0: "星期一",
    1: "星期二",
    2: "星期三",
    3: "星期四",
    4: "星期五",
    5: "星期六",
    6: "星期日"
}

# ==== 小語庫 ====
quotes = [
    ("成功是每天積小步前進。", "Success is the sum of small efforts repeated every day."),
    ("相信自己，你比想像中更堅強。", "Believe in yourself, you are stronger than you think."),
    ("每天都是重新開始的機會。", "Every day is a chance to start anew."),
    ("你的夢想值得你努力。", "Your dreams are worth the effort."),
    ("你走的每一步都算數。", "Every step you take matters."),
    # ...（繼續加滿 100 句）
]

# ==== 行動選項 ====
all_actions = [
    "努力", "奮起", "開心", "積極", "有效率", "放鬆", "溫柔", "專注", "快樂", "冒險",
    "深呼吸", "陪伴", "關懷", "觀察自己", "讚美別人", "早睡", "喝水", "多走路", "不抱怨", "大笑",
    "學習新事物", "吃得健康", "整理空間", "耐心聽人說話", "說實話", "讚美自己", "敢於嘗試", "不逃避", "完成一件小事"
]

# ==== 固定語錄與選項 ====
if "quote" not in st.session_state:
    st.session_state.quote = random.choice(quotes)

if "options" not in st.session_state:
    st.session_state.options = random.sample(all_actions, 3)

quote_ch, quote_en = st.session_state.quote
options = st.session_state.options

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

# ==== 畫面顯示 ====
st.markdown(f"""
## 📅 日期：{date_str}（{weekday_ch}）
### 🕰️ 時間：{time_str}
### 🌤️ 新竹天氣：{weather_desc}，氣溫 {temp}°C

---

### ✨ 今日小語：
> {quote_ch}  
> _{quote_en}_

---

### 🎯 今日選項（請選擇你今天想實踐的行動）：
""")

user_choice = st.radio("請選擇：", options)

if st.button("✨ 我決定了！"):
    st.success(f"🧡 我決定今天要：「{user_choice}」！一起加油吧 👑✨")
