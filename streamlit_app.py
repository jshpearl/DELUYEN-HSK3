import streamlit as st
import time
import requests
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================
# 1. TRANG TRÍ CSS & CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(
    page_title="LUYỆN ĐỀ HSK3 - Cô Bảo Ngọc",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tahoma&display=swap');
    
    html, body, [class*="css"], div, p, span, label {
        font-family: 'Tahoma', sans-serif;
        color: #2D3748;
        line-height: 1.6;
    }

    .zh, .chinese-text, h1, h2, h3, .stRadio label, .stMarkdown {
        font-family: 'SimSun', '宋体', 'Tahoma', serif;
    }

    .stApp {
        background-color: #F8F9FA;
    }

    .question-box {
        background-color: #FFFFFF;
        border-left: 5px solid #4A5568;
        border-right: 1px solid #E2E8F0;
        border-top: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }

    .word-token {
        font-family: 'SimSun', '宋体', serif;
        font-size: 28px;
        font-weight: bold;
        color: #1A365D;
        background-color: #EDF2F7;
        padding: 8px 18px;
        border-radius: 8px;
        display: inline-block;
        margin: 6px;
        border: 2px solid #CBD5E0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }

    .correct-answer {
        background-color: #F0FFF4;
        border-left: 5px solid #38A169;
        padding: 12px;
        border-radius: 6px;
        margin-top: 10px;
    }

    .wrong-answer {
        background-color: #FFF5F5;
        border-left: 5px solid #E53E3E;
        padding: 12px;
        border-radius: 6px;
        margin-top: 10px;
    }

    .congrats-banner {
        background-color: #EBF8FF;
        border: 2px solid #3182CE;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        text-align: center;
    }

    .teacher-footer {
        text-align: center;
        padding: 30px 0 15px 0;
        margin-top: 50px;
        border-top: 1.5px solid #E2E8F0;
        font-size: 24px;
        font-weight: bold;
        color: #2B6CB0;
        font-family: 'SimSun', '宋体', serif;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. DỮ LIỆU ĐỀ THI HSK3 (H31003 & H31008)
# ==========================================
@st.cache_data
def load_exam_data():
    listening_31003 = [
        {"id": i, "type": "listening_tf", "prompt": "★ 八月十五的月亮大。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "八月十五的晚上，月亮就像一个白色的大盘子，非常漂亮。中国人喜欢在这一天和家里人一起吃饭，一起看月亮。"} if i <= 10 else
        {"id": i, "type": "listening_tf", "prompt": "★ 他现在住在公司附近。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "我搬家了。新的房子虽然小了点儿，但是离公司很近。"} if i <= 20 else
        {"id": i, "type": "listening_mc", "prompt": "男的想让小王做什么？", "options": ["A 开门", "B 拿东西", "C 去超市买东西"], "answer": "A 开门", "script": "男：小王，帮我开一下门，好吗？谢谢！\n女：没问题。您去超市了？买了这么多东西。"}
        for i in range(1, 36)
    ]
    
    reading_31003 = [
        {"id": 40 + i, "type": "fill_gap", "prompt": "有些事情看上去很（  ），但要做好，其实不容易。", "options": ["A 简单", "B 举行", "C 像", "D 复习"], "answer": "A 简单", "explanation": "Từ cần điền: 简单 (đơn giản). 有些事情看上去很简单，但要做好，其实不容易。"} if i <= 10 else
        {"id": 40 + i, "type": "reading_mc", "prompt": "到了机场，他发现护照不见了，在行李箱里找了半天，也没找到，很着急。\n★ 他为什么着急？", "options": ["A 迟到了", "B 忘记拿机票了", "C 找不到护照了"], "answer": "C 找不到护照了", "explanation": "Nội dung bài đọc nêu rõ: 很着急 vì 不见了护照 (không tìm thấy hộ chiếu)."}
        for i in range(1, 26)
    ]

    writing_31003 = [
        {"id": 71, "type": "reorder", "prompt": "", "words": ["把", "手机", "送给", "她", "决定", "弟弟", "。"], "correct": "她决定把手机送给弟弟。", "hint": "Cấu trúc câu chữ 把 + Dấu chấm câu 。"},
        {"id": 72, "type": "reorder", "prompt": "", "words": ["我和", "这个学生", "很久", "没见面了", "。"], "correct": "我和这个学生很久没见面了。", "hint": "Chủ ngữ 我和这个学生 + Trạng ngữ 很久 + 没见面了。"},
        {"id": 73, "type": "reorder", "prompt": "", "words": ["这个城市的", "春天", "经常", "刮风", "。"], "correct": "这个城市的春天经常刮风。", "hint": "Chủ ngữ 这个城市的春天 + Vị ngữ 经常刮风。"},
        {"id": 74, "type": "reorder", "prompt": "", "words": ["他的", "汉字", "写得", "很漂亮", "。"], "correct": "他的汉字写得很漂亮。", "hint": "Cấu trúc bổ ngữ trình độ + Dấu chấm 。"},
        {"id": 75, "type": "reorder", "prompt": "", "words": ["叔叔的", "太阳镜", "花了", "900块钱", "。"], "correct": "叔叔的太阳镜花了900块钱。", "hint": "Dấu chấm câu 。 đặt ở cuối."},
        {"id": 76, "type": "char_fill", "prompt": "那轮（ yuè ）亮又大又圆。", "correct": "月", "hint": "Chữ Hán: 月 (月亮 - yuèliang)."},
        {"id": 77, "type": "char_fill", "prompt": "太阳就像一个（ bái ）色的盘子。", "correct": "白", "hint": "Chữ Hán: 白 (白色 - báisè)."},
        {"id": 78, "type": "char_fill", "prompt": "一（ qiān ）万年前，动物们出现了吗？", "correct": "千", "hint": "Chữ Hán: 千 (一千万 - yī qiān wàn)."},
        {"id": 79, "type": "char_fill", "prompt": "外面下雪了，你让孩子路上小（ xīn ）点儿。", "correct": "心", "hint": "Chữ Hán: 心 (小心 - xiǎoxīn)."},
        {"id": 80, "type": "char_fill", "prompt": "生病了要注意休息，（ yīn ）为健康最重要。", "correct": "因", "hint": "Chữ Hán: 因 (因为 - yīnwèi)."}
    ]

    listening_31008 = [
        {"id": i, "type": "listening_tf", "prompt": "★ 努力的人机会多。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "只要你努力，机会总是有的。"} if i <= 10 else
        {"id": i, "type": "listening_tf", "prompt": "★ 他喜欢吃新鲜的水果。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "这些苹果真新鲜，我很喜欢吃。"} if i <= 20 else
        {"id": i, "type": "listening_mc", "prompt": "小张现在在哪儿？", "options": ["A 办公室", "B 图书馆", "C 教室"], "answer": "B 图书馆", "script": "男：小张，你在哪儿呢？\n女：我在图书馆看书呢，一杯茶就回去。"}
        for i in range(1, 36)
    ]

    reading_31008 = [
        {"id": 40 + i, "type": "fill_gap", "prompt": "最近几年，这里的变化很大，街道更干净了。（  ）", "options": ["A 环境变好了", "B 变化不明显", "C 车辆减少了"], "answer": "A 环境变好了", "explanation": "Môi trường sống tốt lên。"} if i <= 10 else
        {"id": 40 + i, "type": "reading_mc", "prompt": "人们经常说：“一分耕耘，一分收获。”这句话告诉我们：", "options": ["A 努力就有回报", "B 时间过得很快", "C 要保护环境"], "answer": "A 努力就有回报", "explanation": "Có làm thì mới có ăn, nỗ lực sẽ thu được thành quả。"}
        for i in range(1, 26)
    ]

    writing_31008 = [
        {"id": 71, "type": "reorder", "prompt": "", "words": ["那位", "邻居", "很热情", "。"], "correct": "那位邻居很热情。", "hint": "Dấu chấm câu 。 đặt ở cuối."},
        {"id": 72, "type": "reorder", "prompt": "", "words": ["这个楼", "一共", "三层", "。"], "correct": "这个楼一共三层。", "hint": "Chủ ngữ 这个楼 + 一共三层。"},
        {"id": 73, "type": "reorder", "prompt": "", "words": ["菜单", "被", "服务员", "拿走了", "。"], "correct": "菜单被服务员拿走了。", "hint": "Câu chữ 被 + Dấu chấm 。"},
        {"id": 74, "type": "reorder", "prompt": "", "words": ["中国南方的雨水", "比", "北方", "多", "。"], "correct": "中国南方的雨水比北方多。", "hint": "Câu so sánh 比 + Dấu chấm 。"},
        {"id": 75, "type": "reorder", "prompt": "", "words": ["把", "冰箱", "放", "厨房里吧", "。"], "correct": "把冰箱放厨房里吧。", "hint": "Câu chữ 把 + Dấu chấm 。"},
        {"id": 76, "type": "char_fill", "prompt": "你姐姐的孩子上（ jǐ ）年级？", "correct": "几", "hint": "Chữ Hán: 几 (jǐ - mấy)."},
        {"id": 77, "type": "char_fill", "prompt": "马小姐，谢谢关（ xīn ），我不发烧了。", "correct": "心", "hint": "Chữ Hán: 心 (关心 - guānxīn)."},
        {"id": 78, "type": "char_fill", "prompt": "对不起，（ xià ）午有个重要的会议。", "correct": "下", "hint": "Chữ Hán: 下 (下午 - xiàwǔ)."},
        {"id": 79, "type": "char_fill", "prompt": "叔叔的普通话水平有了很（ dà ）提高。", "correct": "大", "hint": "Chữ Hán: 大 (dà - lớn)."},
        {"id": 80, "type": "char_fill", "prompt": "这个小太阳表示晴天，（ yún ）表示阴天。", "correct": "云", "hint": "Chữ Hán: 云 (yún - mây)."}
    ]

    return {
        "H31003": {
            "title": "H31003",
            "audio_file": "H31003.mp3",
            "listening": listening_31003,
            "reading": reading_31003,
            "writing": writing_31003
        },
        "H31008": {
            "title": "H31008",
            "audio_file": "H31008.mp3",
            "listening": listening_31008,
            "reading": reading_31008,
            "writing": writing_31008
        }
    }


# ==========================================
# 3. HÀM GỬI ĐIỂM VỀ GOOGLE SHEET CÔ BẢO NGỌC
# ==========================================
def send_score_to_google_sheet(student_name, class_name, exam_code, section, score, total_questions):
    DEFAULT_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycby7XFJf1fV5aL5UiRY0h-kAxHVszQvUnAgSt5brar-K7Fe7-BV9_ifRTZ7suCPEC1BoHg/exec"
    webhook_url = st.secrets.get("SHEET_WEBHOOK_URL", DEFAULT_WEBHOOK_URL)
    
    payload = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "student_name": student_name,
        "class_name": class_name,
        "exam_code": exam_code,
        "section": section,
        "score": score,
        "total": total_questions,
        "percentage": round((score / total_questions) * 100, 1) if total_questions > 0 else 0
    }
    
    if webhook_url:
        try:
            requests.post(webhook_url, json=payload, timeout=5)
            return True
        except Exception:
            pass
            
    if "sheet_history" not in st.session_state:
        st.session_state.sheet_history = []
    st.session_state.sheet_history.append(payload)
    return True


# ==========================================
# 4. QUẢN LÝ SESSION STATE
# ==========================================
if "selected_exam" not in st.session_state:
    st.session_state.selected_exam = None

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "class_name" not in st.session_state:
    st.session_state.class_name = ""

if "submitted_sections" not in st.session_state:
    st.session_state.submitted_sections = {}

if "exam_start_times" not in st.session_state:
    st.session_state.exam_start_times = {}

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}


# ==========================================
# 5. TRANG 1: DANH SÁCH MÃ ĐỀ (GRID PASTEL)
# ==========================================
def render_landing_page():
    st.markdown("<h1 style='text-align: center; color: #1A365D; font-size: 36px; font-weight: bold;'>🎓 LUYỆN ĐỀ HSK3</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #4A5568;'>Vui lòng điền thông tin và chọn Mã Đề Thi để bắt đầu</p>", unsafe_allow_html=True)
    st.write("---")

    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.session_state.student_name = st.text_input("👤 Họ và tên học viên:", value=st.session_state.student_name, placeholder="Ví dụ: Nguyễn Văn A")
    with col_info2:
        st.session_state.class_name = st.text_input("🏫 Tên lớp:", value=st.session_state.class_name, placeholder="Ví dụ: HSK3-K24")

    st.write("")
    st.markdown("### 📋 Danh sách Mã Đề Thi:")

    exams = load_exam_data()
    exam_codes = list(exams.keys())

    cols = st.columns(2)
    pastel_colors = ["#E8F0FE", "#E6F4EA"]
    border_colors = ["#1A365D", "#137333"]

    for idx, code in enumerate(exam_codes):
        with cols[idx % 2]:
            p_bg = pastel_colors[idx % len(pastel_colors)]
            p_border = border_colors[idx % len(border_colors)]
            
            st.markdown(f"""
            <div style="background-color: {p_bg}; border: 3px solid {p_border}; border-radius: 14px; padding: 25px 15px; text-align: center; margin-bottom: 15px;">
                <div style="font-size: 32px; font-weight: bold; color: {p_border}; font-family: 'Tahoma', sans-serif;">{code}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"👉 Vào làm đề {code}", key=f"btn_{code}", use_container_width=True):
                if not st.session_state.student_name.strip():
                    st.error("⚠️ Vui lòng nhập Họ và tên trước khi vào thi!")
                elif not st.session_state.class_name.strip():
                    st.error("⚠️ Vui lòng nhập Tên lớp trước khi vào thi!")
                else:
                    st.session_state.selected_exam = code
                    st.rerun()

    st.markdown("<div class='teacher-footer'>黄宝玉老师</div>", unsafe_allow_html=True)


# ==========================================
# 6. TRANG 2: TRANG LÀM BÀI CÁC PHẦN (3 TABS)
# ==========================================
def render_exam_page(exam_code):
    exams = load_exam_data()
    exam = exams[exam_code]

    col_head1, col_head2 = st.columns([3, 1])
    with col_head1:
        st.markdown(f"## 📝 Đề Thi: <span style='color:#1A365D;'>{exam_code}</span>", unsafe_allow_html=True)
        st.markdown(f"**Học viên:** `{st.session_state.student_name}` | **Lớp:** `{st.session_state.class_name}`")
    with col_head2:
        if st.button("⬅️ Trở về chọn đề khác"):
            st.session_state.selected_exam = None
            st.rerun()

    st.write("---")

    SECTION_TIMES = {
        "listening": 35 * 60,
        "reading": 30 * 60,
        "writing": 15 * 60
    }

    if exam_code not in st.session_state.exam_start_times:
        st.session_state.exam_start_times[exam_code] = {
            "listening": time.time(),
            "reading": time.time(),
            "writing": time.time()
        }

    tab_listen, tab_read, tab_write = st.tabs(["🎧 PHẦN NGHE (Listening)", "📖 PHẦN ĐỌC (Reading)", "✍️ PHẦN VIẾT (Writing)"])

    with tab_listen:
        render_section_tab(
            exam_code=exam_code,
            section_key="listening",
            section_title="PHẦN NGHE (听力)",
            questions=exam["listening"],
            max_time_sec=SECTION_TIMES["listening"],
            audio_file=exam["audio_file"]
        )

    with tab_read:
        render_section_tab(
            exam_code=exam_code,
            section_key="reading",
            section_title="PHẦN ĐỌC (阅读)",
            questions=exam["reading"],
            max_time_sec=SECTION_TIMES["reading"]
        )

    with tab_write:
        render_section_tab(
            exam_code=exam_code,
            section_key="writing",
            section_title="PHẦN VIẾT (书写)",
            questions=exam["writing"],
            max_time_sec=SECTION_TIMES["writing"]
        )

    st.markdown("<div class='teacher-footer'>黄宝玉老师</div>", unsafe_allow_html=True)


# ==========================================
# 7. HÀM HIỂN THỊ CHI TIẾT TỪNG PHẦN THI
# ==========================================
def render_section_tab(exam_code, section_key, section_title, questions, max_time_sec, audio_file=None):
    st.subheader(f"📌 {section_title}")

    section_id = f"{exam_code}_{section_key}"
    is_submitted = st.session_state.submitted_sections.get(section_id, False)

    start_time = st.session_state.exam_start_times[exam_code][section_key]
    elapsed = time.time() - start_time
    remaining_sec = max(0, int(max_time_sec - elapsed))

    # JavaScript Đồng hồ đếm ngược chạy thực tế trong IFrame (components.html)
    if not is_submitted:
        timer_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Tahoma:wght@700&display=swap');
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Tahoma', sans-serif;
                background-color: transparent;
            }}
            .timer-container {{
                background-color: #FFF5F5;
                border: 2.5px solid #E53E3E;
                padding: 10px 15px;
                border-radius: 10px;
                font-size: 20px;
                font-weight: bold;
                color: #C53030;
                text-align: center;
                box-shadow: 0 2px 8px rgba(229, 62, 62, 0.15);
            }}
            .timer-warning {{
                background-color: #FED7D7 !important;
                animation: blinker 1s linear infinite;
            }}
            @keyframes blinker {{
                50% {{ opacity: 0.5; }}
            }}
        </style>
        </head>
        <body>
        <div id="timer_box" class="timer-container">
            ⏱️ Thời gian còn lại: <span id="timer_display">--:--</span>
        </div>
        <script>
            var totalSeconds = {remaining_sec};
            function updateTimer() {{
                if (totalSeconds <= 0) {{
                    document.getElementById("timer_display").innerText = "00:00 - ĐÃ HẾT GIỜ!";
                    document.getElementById("timer_box").className = "timer-container timer-warning";
                    return;
                }}
                var minutes = Math.floor(totalSeconds / 60);
                var seconds = totalSeconds % 60;
                var mStr = minutes < 10 ? "0" + minutes : minutes;
                var sStr = seconds < 10 ? "0" + seconds : seconds;
                document.getElementById("timer_display").innerText = mStr + ":" + sStr;
                if (totalSeconds <= 300) {{
                    document.getElementById("timer_box").className = "timer-container timer-warning";
                }}
                totalSeconds--;
            }}
            updateTimer();
            setInterval(updateTimer, 1000);
        </script>
        </body>
        </html>
        """
        components.html(timer_html, height=65)

        if remaining_sec <= 0:
            st.error("🚨 ĐÃ HẾT GIỜ LÀM BÀI! Tự động nộp phần này...")
            st.session_state.submitted_sections[section_id] = True
            is_submitted = True
            st.rerun()

    if audio_file and section_key == "listening":
        st.audio(f"{audio_file}", format="audio/mp3")

    st.write("")

    answers_key_prefix = f"ans_{exam_code}_{section_key}"

    for idx, q in enumerate(questions):
        q_id = q["id"]
        q_key = f"{answers_key_prefix}_{q_id}"

        st.markdown("<div class='question-box'>", unsafe_allow_html=True)
        
        # Hiển thị STT câu thực tế
        if q["prompt"]:
            st.markdown(f"**Câu {q_id}:** <span class='chinese-text' style='font-size:19px;'>{q['prompt']}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"**Câu {q_id}:**", unsafe_allow_html=True)

        # Chữ Hán phần sắp xếp to rõ ràng (28px)
        if q["type"] == "reorder":
            words_html = "".join([f"<span class='word-token'>{w}</span>" for w in q.get("words", [])])
            st.markdown(f"<div style='margin: 12px 0 18px 0; line-height: 2.2;'>{words_html}</div>", unsafe_allow_html=True)

        if not is_submitted:
            if q["type"] in ["listening_tf", "listening_mc", "fill_gap", "reading_mc"]:
                user_ans = st.radio("Chọn đáp án:", q["options"], key=q_key, index=None)
                st.session_state.user_answers[q_key] = user_ans
            elif q["type"] in ["reorder", "char_fill"]:
                user_ans = st.text_input("Nhập câu trả lời:", key=q_key)
                st.session_state.user_answers[q_key] = user_ans
        else:
            user_ans = st.session_state.user_answers.get(q_key, "")
            
            if q["type"] in ["reorder", "char_fill"]:
                is_correct = (user_ans.strip() == q["correct"].strip())
                expected = q["correct"]
            else:
                is_correct = (user_ans == q["answer"])
                expected = q["answer"]

            if is_correct:
                st.markdown(f"<div class='correct-answer'>✅ <b>Chính xác!</b> Đáp án của bạn: <code>{user_ans}</code></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='wrong-answer'>
                    ❌ <b>Chưa đúng!</b><br>
                    • Đáp án của bạn: <code style='color:red;'>{user_ans if user_ans else '(Chưa trả lời)'}</code><br>
                    • Đáp án chuẩn: <code style='color:green;'>{expected}</code>
                </div>
                """, unsafe_allow_html=True)

            if "script" in q:
                with st.expander("📝 Xem Script bài nghe"):
                    st.write(q["script"])
            if "explanation" in q:
                with st.expander("💡 Giải thích đáp án"):
                    st.write(q["explanation"])

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    if not is_submitted:
        if st.button(f"🚀 NỘP BÀI {section_title.upper()}", key=f"sub_btn_{section_id}", type="primary"):
            st.session_state.submitted_sections[section_id] = True

            correct_count = 0
            for q in questions:
                q_key = f"{answers_key_prefix}_{q['id']}"
                u_a = st.session_state.user_answers.get(q_key, "")
                if q["type"] in ["reorder", "char_fill"]:
                    if u_a.strip() == q["correct"].strip():
                        correct_count += 1
                else:
                    if u_a == q["answer"]:
                        correct_count += 1

            send_score_to_google_sheet(
                student_name=st.session_state.student_name,
                class_name=st.session_state.class_name,
                exam_code=exam_code,
                section=section_key,
                score=correct_count,
                total_questions=len(questions)
            )

            st.rerun()
    else:
        correct_count = sum([
            1 for q in questions if (
                (st.session_state.user_answers.get(f"{answers_key_prefix}_{q['id']}", "").strip() == q["correct"].strip())
                if q["type"] in ["reorder", "char_fill"]
                else (st.session_state.user_answers.get(f"{answers_key_prefix}_{q['id']}", "") == q["answer"])
            )
        ])
        total_q = len(questions)
        pct = round((correct_count / total_q) * 100, 1)

        st.markdown(f"""
        <div class="congrats-banner">
            <h3 style="color: #2B6CB0; margin-bottom: 10px;">🎉 Chúc mừng <b>"{st.session_state.student_name}"</b> đã hoàn thành đề <b>"{exam_code}"</b> ({section_title})</h3>
            <p style="font-size: 20px; color: #2D3748; margin: 0;">📊 Điểm số của bạn là: <b style="color: #2B6CB0; font-size: 24px;">{correct_count}/{total_q}</b> câu đúng (<b>{pct}%</b>)</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    if st.session_state.selected_exam is None:
        render_landing_page()
    else:
        render_exam_page(st.session_state.selected_exam)

if __name__ == "__main__":
    main()
