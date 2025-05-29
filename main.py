import streamlit as st
import requests
import datetime
import pytz
import random

# === API 設定 ===
API_KEY = "11e1ae55357eb1c7ab1b8823783fa5c9"
LANG = "zh_tw"
UNITS = "metric"

# === 語錄來源（GitHub JSON） ===
JSON_URL = "https://raw.githubusercontent.com/smallcisum/bible/main/bible.json"
def load_quotes_from_json(url):
      normalized = []
    for q in raw_data:
        if len(q) == 2:
            zh, en = q
            ref, tag = "", ""
        elif len(q) == 3:
            zh, en, ref = q
            tag = ""
        elif len(q) == 4:
            zh, en, ref, tag = q
        else:
            zh, en, ref, tag = "⚠️ 格式錯誤", "Invalid format", "", ""
        normalized.append((zh.strip(), en.strip(), ref.strip(), tag.strip()))
    return normalized


# === 行動選項 ===
all_actions = [
    "努力", "奮起", "開心", "積極", "有效率", "放鬆", "溫柔", "專注", "快樂", "冒險",
    "深呼吸", "陪伴", "關懷", "觀察自己", "讚美別人", "早睡", "喝水", "多走路", "不抱怨", "大笑",
    "學習新事物", "吃得健康", "整理空間", "耐心聽人說話", "說實話", "讚美自己", "敢於嘗試", "不逃避", "完成一件小事"
]

# === 抓取地點與時區 ===
def get_location():
    try:
        res = requests.get("http://ip-api.com/json", timeout=3)
        data = res.json()
        city = data.get("city", "Hsinchu")
        timezone_str = data.get("timezone", "Asia/Taipei")
        tz = pytz.timezone(timezone_str)
    except:
        city = "Hsinchu"
        tz = pytz.timezone("Asia/Taipei")
    return city, tz

CITY, TZ = get_location()


# 直接顯示用戶地點的時間和天氣
st.markdown(f"""
### 🌤️ 天氣：{CITY} {weather_desc}，氣溫 {temp}°C  
### 📅 時間：{time_str}（{weekday_ch}）
---
""")

# 今日小語
st.subheader("✨ 今日小語：")
st.write(f"📖 {quote_ch}" + (f"（{quote_ref}）" if quote_ref else "") + (f" [{quote_tag}]" if quote_tag else ""))
st.write(f"_🕊️ {quote_en}_")

st.markdown("---\n### 🎯 今日選項（請選擇你今天想實踐的行動）")
user_choice = st.radio("請選擇：", options)

if st.button("✨ 我決定了！"):
    st.success(f"🧡 我決定今天要：「{user_choice}」！一起加油吧 👑✨")
