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
    try:
        res = requests.get(url, timeout=5)
        raw_data = res.json()
        verses = raw_data.get("verses", [])  # ✅ 只處理有章節與翻譯的經文
    except:
        return [("⚠️ 無法載入資料", "Failed to load data", "", "")]

    normalized = []
    for q in verses:
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
    "學習新事物", "吃得健康", "整理空間", "耐心聽人說話", "說實話", "讚美自己", "敢於嘗試", "不逃避", "完成一件小事",
    "勇敢", "奉獻", "禱告", "傾聽", "尋求", "讚頌", "專心仰望主", "讚美神", "感恩禱告", "禁食禱告",
    "不停讚美", "活出主心意", "成為榜樣", "做美好的事情", "尋求真善美", "渴慕主", "理解他人", "愛自己", "愛別人", "更親近主",
    "衝破攔阻", "克服困難", "保守己心", "滿懷盼望", "堅定信心", "不斷禱告", "帶領別人", "幫助別人", "讀經",
    "幫助他人", "傳福音", "做見證", "慈善捐款", "做義工", "不放棄", "思想神的話", "多聚會", "彼此討論聖經", "勇於嘗試",
    "渴望", "相信", "原諒", "成全別人", "忍耐", "思考主會怎麼做", "聽神的話語", "說讚美的話語", "做一件善事", "同理心",
    "朝夢想邁進", "認真", "改善", "轉變", "積極", "奮鬥", "協助", "多觀察", "多聽少說",
    "深度思考", "尋找方法", "思想", "有效率", "認真規劃", "節制", "控制飲食", "深度放鬆", "保持健康", "多動少吃",
    "聽音樂", "散步", "玩遊戲", "減少3c", "和朋友聊天", "給家人關懷", "關心家人", "說出愛的語言", "道歉", "做勇敢的行動",
    "斷捨離", "收拾房間", "調整自己", "聽講道", "聆聽解經", "查看聖經", "尋求主", "渴慕主", "尋找方法"
]

# === 地點與時間 ===
city_list = ["Hsinchu", "Taipei", "Taichung", "Tainan", "Kaohsiung"]
CITY = st.selectbox("請選擇城市：", city_list)
TZ = pytz.timezone("Asia/Taipei")
now = datetime.datetime.now(TZ)

weekday_ch = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
time_str = now.strftime("%Y/%m/%d (%H:%M)")

# === 天氣資訊 ===
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}&lang={LANG}"
try:
    res = requests.get(weather_url, timeout=3)
    data = res.json()
    weather_desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
except:
    weather_desc = "取得失敗"
    temp = "--"

# === 每日語錄與選項（固定種子）===
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
st.markdown(f"#### 📖 {quote_ch}" + (f"（{quote_ref}）" if quote_ref else "") + (f" [{quote_tag}]" if quote_tag else ""))
st.markdown(f"#### _🕊️ {quote_en}_")
st.markdown("---")

st.subheader("🎯 今日選項（請選擇你今天想實踐的行動）")
user_choice = st.radio("請選擇：", options)

if st.button("✨ 我決定了！"):
    st.success(f"🧡 我決定今天要：「{user_choice}」！一起加油吧 👑✨")
