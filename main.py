import streamlit as st
import requests
import datetime
import pytz
import random

# === API 設定 ===
API_KEY = "11e1ae55357eb1c7ab1b8823783fa5c9"
LANG = "zh_tw"
UNITS = "metric"

# === 語錄來源（GitHub JSON）===
JSON_URL = "https://raw.githubusercontent.com/smallcisum/bible/main/bible.json"

def load_quotes_from_json(url):
    try:
        res = requests.get(url, timeout=5)
        raw_data = res.json()
    except:
        return [("⚠️ 無法載入資料", "Failed to load data", "", "")]

    normalized = []
    for q in raw_data:
        zh = q.get("zh", "").strip()
        en = q.get("en", "").strip()
        ref = q.get("zh_ref", "").strip()
        tag = q.get("topic", "").strip()
        normalized.append((zh, en, ref, tag))
    return normalized

quotes = load_quotes_from_json(JSON_URL)

# === 行動選項 ===
all_actions = [
    "努力", "奮起", "開心", "積極", "有效率", "放鬆", "溫柔", "專注", "快樂", "冒險",
    "深呼吸", "陪伴", "關懷", "觀察自己", "讚美別人", "早睡", "喝水", "多走路", "不抱怨", "大笑",
    "學習新事物", "吃得健康", "整理空間", "耐心聽人說話", "說實話", "讚美自己", "敢於嘗試", "不逃避", "完成一件小事"
]

# === 手動選城市 ===
city_options = ["Hsinchu", "Taipei", "Taichung", "Tainan", "Kaohsiung"]
CITY = st.selectbox("請選擇城市：", city_options, index=0)
TZ = pytz.timezone("Asia/Taipei")

# === 時間處理 ===
now = datetime.datetime.now(TZ)
weekday_ch = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
time_str = now.strftime("%Y/%m/%d (%H:%M)")

# === 天氣資料 ===
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}&lang={LANG}"
try:
    res = requests.get(weather_url, timeout=3)
    data = res.json()
    weather_desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
except:
    weather_desc = "取得失敗"
    temp = "--"

# === 固定每日語錄與選項 ===
today_seed = int(now.strftime("%Y%m%d"))
random.seed(today_seed)
quote = random.choice(quotes)
options = random.sample(all_actions, 3)
quote_ch, quote_en, quote_ref, quote_tag = quote

# === 畫面呈現 ===
st.subheader("✨ 今日資訊")
st.markdown(f"#### 🌤️ 天氣：{CITY} {weather_desc}，氣溫 {temp}°C")
st.markdown(f"#### 📅 時間：{time_str}（{weekday_ch}）")
st.markdown("---")

st.subheader("✨ 今日小語")
st.write(f"📖 {quote_ch}" + (f"（{quote_ref}）" if quote_ref else "") + (f" [{quote_tag}]" if quote_tag else ""))
st.write(f"_🕊️ {quote_en}_")

st.markdown("---")
st.subheader("🎯 今日選項（請選擇你今天想實踐的行動）")
user_choice = st.radio("請選擇：", options)

if st.button("✨ 我決定了！"):
    st.success(f"🧡 我決定今天要：「{user_choice}」！一起加油吧 👑✨")
