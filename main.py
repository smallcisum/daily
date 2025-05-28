import streamlit as st
import requests
import datetime
import pytz
import random

# ==== 設定 OpenWeatherMap ====
API_KEY = "11e1ae55357eb1c7ab1b8823783fa5c9"  # OpenWeatherMap API Key
LANG = "zh_tw"
UNITS = "metric"

# ==== 中文星期對照表 ====
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
    # ...（繼續加到 100 句）
]

# ==== 行動選項 ====
all_actions = [
    "努力", "奮起", "開心", "積極", "有效率", "放鬆", "溫柔", "專注", "快樂", "冒險",
    "深呼吸", "陪伴", "關懷", "觀察自己", "讚美別人", "早睡", "喝水", "多走路", "不抱怨", "大笑",
    "學習新事物", "吃得健康", "整理空間", "耐心聽人說話", "說實話", "讚美自己", "敢於嘗試", "不逃避", "完成一件小事",
    "勇敢", "傾聽", "關心周遭", "提升自己", "看別人優點", "早點行動", "做運動", "跳躍", "不傷心", "玩遊戲",
    "學習冒險", "吃得開心", "保持整潔", "有同理心", "想像未來", "讚美小事物", "敢於挑戰", "不害怕", "完成工作",
"深深感受", "有愛心", "憐憫別人", "原諒自己", "原諒別人", "靜下來想想", "多動動", "多嘗試", "不退縮", "大哭一場",
    "試著了解", "用心思考", "斷捨離", "發掘自己優點", "接受自己", "和朋友說話", "追求夢想", "解決現實問題", "療癒自己"
]

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

# ==== 小語與選項狀態保存 ====
if "quote" not in st.session_state:
    st.session_state.quote = random.choice(quotes)

if "options" not in st.session_state:
    st.session_state.options = random.sample(all_actions, 3)

quote_ch, quote_en = st.session_state.quote
options = st.session_state.options

# ==== 畫面顯示 ====
st.markdown(f"""
## 📍 根據您目前的位置：**{CITY}**
## 📅 日期：{date_str}（{weekday_ch}）
### 🕰️ 當地時間：{time_str}
### 🌤️ 天氣：{weather_desc}，氣溫 {temp}°C

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
