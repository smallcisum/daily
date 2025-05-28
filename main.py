import streamlit as st
import requests
import datetime
import pytz
import random
import os
import json

# ==== 設定 ====
API_KEY = os.getenv("OPENWEATHER_API_KEY", "11e1ae55357eb1c7ab1b8823783fa5c9")
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

# ==== 擴展的小語庫（100+句）====
quotes = [
    ("成功是每天積小步前進。", "Success is the sum of small efforts repeated every day."),
    ("相信自己，你比想像中更堅強。", "Believe in yourself, you are stronger than you think."),
    ("每天都是重新開始的機會。", "Every day is a chance to start anew."),
    ("你的夢想值得你努力。", "Your dreams are worth the effort."),
    ("你走的每一步都算數。", "Every step you take matters."),
    ("勇氣不是沒有恐懼，而是面對恐懼。", "Courage is not the absence of fear, but facing it."),
    ("今天的努力是明天的收穫。", "Today's effort is tomorrow's harvest."),
    ("困難是通往成功的階梯。", "Difficulties are stepping stones to success."),
    ("保持積極，吸引美好。", "Stay positive and attract good things."),
    ("每個結束都是新的開始。", "Every ending is a new beginning."),
    ("你有改變世界的力量。", "You have the power to change the world."),
    ("專注當下，活在此刻。", "Focus on the present, live in the moment."),
    ("微笑是最美的語言。", "A smile is the most beautiful language."),
    ("善待自己，你值得最好的。", "Be kind to yourself, you deserve the best."),
    ("每一天都是禮物。", "Every day is a gift."),
    ("堅持不懈，必有回報。", "Persistence always pays off."),
    ("你比昨天更進步了。", "You are better than you were yesterday."),
    ("機會總是留給準備好的人。", "Opportunity favors the prepared mind."),
    ("失敗是成功之母。", "Failure is the mother of success."),
    ("心懷感恩，生活更美好。", "Gratitude makes life more beautiful."),
    ("勇敢追求你的熱情。", "Bravely pursue your passion."),
    ("小小的改變，大大的不同。", "Small changes, big differences."),
    ("今天是你餘生的第一天。", "Today is the first day of the rest of your life."),
    ("相信過程，享受旅程。", "Trust the process, enjoy the journey."),
    ("你的態度決定你的高度。", "Your attitude determines your altitude."),
    ("做最好的自己。", "Be the best version of yourself."),
    ("永遠不要放棄希望。", "Never give up hope."),
    ("成長來自於挑戰。", "Growth comes from challenges."),
    ("你有無限的可能。", "You have infinite possibilities."),
    ("愛自己是一輩子的功課。", "Loving yourself is a lifelong lesson."),
    ("行動勝過千言萬語。", "Actions speak louder than words."),
    ("每個人都有自己的節奏。", "Everyone has their own rhythm."),
    ("困境中見真章。", "Character is revealed in adversity."),
    ("學習永遠不嫌晚。", "It's never too late to learn."),
    ("你的故事還在書寫中。", "Your story is still being written."),
    ("善良是最大的智慧。", "Kindness is the greatest wisdom."),
    ("今天比昨天勇敢一點。", "Be a little braver today than yesterday."),
    ("創造你想要的生活。", "Create the life you want."),
    ("快樂是一種選擇。", "Happiness is a choice."),
    ("專注解決方案，不是問題。", "Focus on solutions, not problems."),
    ("你的努力不會白費。", "Your efforts will not be in vain."),
    ("保持好奇心。", "Stay curious."),
    ("平凡中見不凡。", "Find the extraordinary in the ordinary."),
    ("你比你想像的更有能力。", "You are more capable than you imagine."),
    ("今天就是最好的時機。", "Today is the perfect time."),
    ("相信自己的直覺。", "Trust your intuition."),
    ("每個人都是獨一無二的。", "Everyone is unique."),
    ("擁抱不完美。", "Embrace imperfection."),
    ("你的價值不由他人定義。", "Your worth is not defined by others."),
    ("勇敢做自己。", "Dare to be yourself."),
    ("小小的進步也是進步。", "Small progress is still progress."),
    ("專注於你能控制的事。", "Focus on what you can control."),
    ("感謝今天的所有經歷。", "Be grateful for all of today's experiences."),
    ("你的聲音很重要。", "Your voice matters."),
    ("永遠保持學習的心。", "Always keep a learning mind."),
    ("今天的挫折是明天的智慧。", "Today's setbacks are tomorrow's wisdom."),
    ("你有權利快樂。", "You have the right to be happy."),
    ("相信時間的力量。", "Believe in the power of time."),
    ("做你害怕的事。", "Do what scares you."),
    ("你的夢想沒有期限。", "Your dreams have no expiration date."),
    ("善待他人，善待自己。", "Be kind to others and to yourself."),
    ("每天學會一件新事物。", "Learn something new every day."),
    ("你的存在就是意義。", "Your existence is meaningful."),
    ("擁抱改變，它帶來成長。", "Embrace change, it brings growth."),
    ("你比你的問題更強大。", "You are stronger than your problems."),
    ("保持內心的平靜。", "Maintain inner peace."),
    ("今天就開始行動。", "Start taking action today."),
    ("你的努力終將開花結果。", "Your efforts will eventually bear fruit."),
    ("相信美好即將發生。", "Believe that good things are coming."),
    ("每一次呼吸都是新的開始。", "Every breath is a new beginning."),
    ("你有權利犯錯。", "You have the right to make mistakes."),
    ("保持謙遜，持續成長。", "Stay humble, keep growing."),
    ("你的想法創造你的現實。", "Your thoughts create your reality."),
    ("今天比昨天更感恩。", "Be more grateful today than yesterday."),
    ("你的旅程獨一無二。", "Your journey is unique."),
    ("擁有耐心，等待花開。", "Have patience, wait for the flowers to bloom."),
    ("你的努力不需要別人理解。", "Your efforts don't need others' understanding."),
    ("保持好奇，保持熱情。", "Stay curious, stay passionate."),
    ("你有改變的勇氣。", "You have the courage to change."),
    ("每天都是學習的機會。", "Every day is an opportunity to learn."),
    ("相信自己的節奏。", "Trust your own pace."),
    ("你的光芒無法被掩蓋。", "Your light cannot be dimmed."),
    ("今天就是完美的一天。", "Today is a perfect day."),
    ("你有能力創造奇蹟。", "You have the ability to create miracles."),
    ("保持初心，方得始終。", "Keep your original intention and achieve your goal."),
    ("你的故事激勵著別人。", "Your story inspires others."),
    ("相信過程中的美好。", "Believe in the beauty of the process."),
    ("你值得所有美好的事物。", "You deserve all the beautiful things."),
    ("今天是充滿可能的一天。", "Today is a day full of possibilities."),
    ("你的心有多大，舞台就有多大。", "Your stage is as big as your heart."),
    ("保持熱愛，奔赴山海。", "Keep your passion and run to the mountains and seas."),
    ("你的努力終將被看見。", "Your efforts will eventually be seen."),
    ("每個當下都值得珍惜。", "Every moment is worth cherishing."),
    ("你有權利追求幸福。", "You have the right to pursue happiness."),
    ("相信生活的美好安排。", "Trust in life's beautiful arrangements."),
    ("你的價值不需要證明。", "Your value doesn't need to be proven."),
    ("今天就是最好的自己。", "Today you are the best version of yourself."),
    ("保持善良，世界因你而美好。", "Stay kind, the world is beautiful because of you."),
    ("你的每一天都很重要。", "Every day of yours matters."),
    ("相信未來會更好。", "Believe that the future will be better."),
    ("你有無限的創造力。", "You have unlimited creativity."),
    ("今天的你已經很棒了。", "You are already amazing today."),
    ("保持前進，永不放棄。", "Keep moving forward, never give up."),
    ("你的微笑能照亮世界。", "Your smile can light up the world."),
    ("每一次努力都有意義。", "Every effort has meaning."),
    ("你有權利做自己。", "You have the right to be yourself."),
    ("相信內心的聲音。", "Believe in your inner voice."),
    ("今天是新的開始。", "Today is a new beginning."),
    ("你的堅持終將勝利。", "Your persistence will ultimately triumph."),
    ("保持樂觀，擁抱希望。", "Stay optimistic and embrace hope."),
    ("你的存在就是禮物。", "Your existence is a gift."),
    ("每天都要愛自己一點。", "Love yourself a little more every day."),
]

# ==== 行動選項庫 ====
all_actions = [
    "努力", "奮起", "開心", "積極", "有效率", "放鬆", "溫柔", "專注", "快樂", "冒險",
    "深呼吸", "陪伴", "關懷", "觀察自己", "讚美別人", "早睡", "喝水", "多走路", "不抱怨", "大笑",
    "學習新事物", "吃得健康", "整理空間", "耐心聽人說話", "說實話", "讚美自己", "敢於嘗試", "積極", "不逃避", "完成一件小事",
    "寫日記", "聽音樂", "看書", "運動", "冥想", "做飯", "打電話給朋友", "整理房間", "種植物", "畫畫",
    "唱歌", "跳舞", "散步", "做志工", "學語言", "練字", "攝影", "做手工", "泡茶", "看電影",
    "寫信", "做瑜伽", "騎腳踏車", "游泳", "爬山", "看日出", "數星星", "做烘焙", "學樂器", "做拼圖"
]

@st.cache_data(ttl=300)  # 快取5分鐘
def get_weather_data_by_coords(lat, lon):
    """根據座標取得天氣資料"""
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={UNITS}&lang={LANG}"
    try:
        response = requests.get(weather_url, timeout=10)
        response.raise_for_status()
        weather_data = response.json()
        weather_desc = weather_data["weather"][0]["description"]
        temp = weather_data["main"]["temp"]
        city_name = weather_data["name"]
        country = weather_data["sys"]["country"]
        return weather_desc, temp, city_name, country
    except requests.exceptions.RequestException as e:
        st.error(f"無法取得天氣資料：{e}")
        return "無法取得天氣資料", "--", "未知位置", ""
    except KeyError as e:
        st.error(f"天氣資料格式錯誤：{e}")
        return "天氣資料格式錯誤", "--", "未知位置", ""
    except Exception as e:
        st.error(f"發生未知錯誤：{e}")
        return "取得失敗", "--", "未知位置", ""

@st.cache_data(ttl=300)  # 快取5分鐘
def get_timezone_by_coords(lat, lon):
    """根據座標取得時區資訊"""
    try:
        # 簡單的時區偵測：根據經度估算時區
        timezone_offset = round(lon / 15)  # 每15度約1小時
        # 限制在合理範圍內
        timezone_offset = max(-12, min(12, timezone_offset))
        
        # 建立時區
        if timezone_offset >= 0:
            tz_name = f"Etc/GMT-{timezone_offset}"
        else:
            tz_name = f"Etc/GMT+{abs(timezone_offset)}"
        
        try:
            user_tz = pytz.timezone(tz_name)
            return user_tz
        except:
            # 如果時區名稱無效，回到 UTC
            return pytz.UTC
    except:
        # 發生錯誤時使用 UTC
        return pytz.UTC

def get_current_time_info(user_tz=None):
    """取得當前時間資訊"""
    if user_tz:
        now = datetime.datetime.now(user_tz)
    else:
        now = datetime.datetime.now(TZ)
    date_str = now.strftime("%Y/%m/%d")
    weekday_ch = weekdays[now.weekday()]
    time_str = now.strftime("%H:%M")
    return date_str, weekday_ch, time_str

def main():
    st.set_page_config(
        page_title="每日成長小站",
        page_icon="✨",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # 標題
    st.title("✨ 每日成長小站")
    st.markdown("### 讓每一天都充滿正能量！")
    
    # 位置按鈕和說明
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("📍 偵測位置", help="根據您的位置顯示當地時間和天氣"):
            # 使用JavaScript獲取位置
            st.markdown("""
            <script>
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    // 將位置資訊傳送到Streamlit
                    const coords = {
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    };
                    
                    // 使用fetch API將資料傳送到後端
                    fetch(window.location.href, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({location: coords})
                    }).then(() => {
                        window.location.reload();
                    });
                }, function(error) {
                    alert('無法取得位置資訊：' + error.message);
                });
            } else {
                alert('您的瀏覽器不支援地理位置功能');
            }
            </script>
            """, unsafe_allow_html=True)
            
    with col2:
        # 提供手動輸入選項
        location_option = st.selectbox(
            "或選擇城市：",
            ["使用預設位置 (台北)", "台北", "台中", "高雄", "台南", "新竹", "其他"]
        )
    
    # 根據選擇設定座標
    if location_option == "台北":
        user_coords = {"lat": 25.0330, "lon": 121.5654}
        location_name = "台北"
    elif location_option == "台中":
        user_coords = {"lat": 24.1477, "lon": 120.6736}
        location_name = "台中"
    elif location_option == "高雄":
        user_coords = {"lat": 22.6273, "lon": 120.3014}
        location_name = "高雄"
    elif location_option == "台南":
        user_coords = {"lat": 22.9999, "lon": 120.2269}
        location_name = "台南"
    elif location_option == "新竹":
        user_coords = {"lat": 24.8138, "lon": 120.9675}
        location_name = "新竹"
    else:
        user_coords = {"lat": 25.0330, "lon": 121.5654}  # 預設台北
        location_name = "台北"
    
    # 取得時區和時間資訊
    if user_coords:
        user_tz = get_timezone_by_coords(user_coords['lat'], user_coords['lon'])
        date_str, weekday_ch, time_str = get_current_time_info(user_tz)
        location_status = f"🌍 {location_name}當地時間"
    else:
        date_str, weekday_ch, time_str = get_current_time_info()
        location_status = "🕰️ 台北時間"
    
    # 顯示位置狀態
    st.caption(location_status)
    
    # 建立三欄布局顯示日期時間
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 日期", date_str)
    with col2:
        st.metric("📆 星期", weekday_ch)
    with col3:
        st.metric("🕰️ 時間", time_str)
    
    st.divider()
    
    # 天氣資訊
    if user_coords:
        st.subheader(f"🌤️ {location_name}天氣")
        weather_desc, temp, city_name, country = get_weather_data_by_coords(
            user_coords['lat'], user_coords['lon']
        )
        weather_location = f"{city_name}, {country}"
    else:
        st.subheader("🌤️ 台北天氣")
        weather_desc, temp, city_name, country = get_weather_data_by_coords(25.0330, 121.5654)
        weather_location = "台北, TW"
    
    # 顯示天氣位置
    st.caption(f"📍 {weather_location}")
    
    # 天氣顯示
    weather_col1, weather_col2 = st.columns(2)
    with weather_col1:
        st.metric("天氣狀況", weather_desc)
    with weather_col2:
        if temp != "--":
            st.metric("氣溫", f"{temp}°C")
        else:
            st.metric("氣溫", temp)
    
    st.divider()
    
    # 今日小語
    st.subheader("✨ 今日小語")
    if 'daily_quote' not in st.session_state:
        st.session_state.daily_quote = random.choice(quotes)
    
    quote_ch, quote_en = st.session_state.daily_quote
    
    # 使用引言格式顯示，加大字體
    st.markdown(f"""
    <div style='padding: 20px; background-color: #f0f2f6; border-radius: 10px; border-left: 5px solid #ff6b6b;'>
        <h3 style='color: #2c3e50; margin-bottom: 10px; font-size: 1.4em;'>{quote_ch}</h3>
        <p style='color: #7f8c8d; font-style: italic; font-size: 1.1em; margin: 0;'>{quote_en}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 更換小語按鈕
    if st.button("🔄 更換小語", type="secondary"):
        st.session_state.daily_quote = random.choice(quotes)
        st.rerun()
    
    st.divider()
    
    # 今日行動選項
    st.subheader("🎯 今日行動選項")
    st.markdown("請選擇你今天想實踐的行動：")
    
    # 初始化行動選項
    if 'daily_actions' not in st.session_state:
        st.session_state.daily_actions = random.sample(all_actions, 3)
    
    # 顯示選項按鈕
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button(f"1️⃣ {st.session_state.daily_actions[0]}", key="action1", use_container_width=True):
            st.session_state.selected_action = st.session_state.daily_actions[0]
            st.session_state.action_selected = True
    
    with action_col2:
        if st.button(f"2️⃣ {st.session_state.daily_actions[1]}", key="action2", use_container_width=True):
            st.session_state.selected_action = st.session_state.daily_actions[1]
            st.session_state.action_selected = True
    
    with action_col3:
        if st.button(f"3️⃣ {st.session_state.daily_actions[2]}", key="action3", use_container_width=True):
            st.session_state.selected_action = st.session_state.daily_actions[2]
            st.session_state.action_selected = True
    
    # 重新選擇行動按鈕
    if st.button("🎲 重新選擇行動", type="secondary"):
        st.session_state.daily_actions = random.sample(all_actions, 3)
        if 'action_selected' in st.session_state:
            del st.session_state.action_selected
        if 'selected_action' in st.session_state:
            del st.session_state.selected_action
        st.rerun()
    
    # 顯示選擇結果
    if st.session_state.get('action_selected', False):
        st.success(f"🧡 太棒了！我決定今天要：「{st.session_state.selected_action}」！")
        st.balloons()
        
        # 鼓勵訊息
        encouragement_messages = [
            "一起加油吧！ 👑✨",
            "你一定可以做到的！ 💪✨",
            "相信自己，勇敢前進！ 🌟",
            "每一步都是進步！ 🚀",
            "今天會是美好的一天！ 🌈"
        ]
        st.markdown(f"### {random.choice(encouragement_messages)}")
    
    # 頁腳
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            💝 願每一天都充滿愛與希望 💝<br>
            <small>記住：你比想像中更堅強，每一天都是新的開始！</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
