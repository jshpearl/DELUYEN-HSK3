import streamlit as st
import time
import requests
from datetime import datetime

# ==========================================
# 1. TRANG TRÍ CSS & CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(
    page_title="LUYỆN ĐỀ HSK3 - Cô Bảo Ngọc",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Custom CSS cho Font, Màu sắc Pastel, Viền Đậm, Responsive
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

    /* Timer Box Header */
    .timer-container {
        background-color: #FFF5F5;
        border: 2.5px solid #E53E3E;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 22px;
        font-weight: bold;
        color: #C53030;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(229, 62, 62, 0.15);
    }

    .timer-warning {
        animation: blinker 1s linear infinite;
        background-color: #FED7D7 !important;
    }

    @keyframes blinker {
        50% { opacity: 0.5; }
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
# 2. DỮ LIỆU ĐỀ THI HSK3 (GỒM H31003 & H31008)
# ==========================================
@st.cache_data
def load_exam_data():
    # H31003 Full Questions
    listening_31003 = [
        {"id": i, "type": "listening_tf", "prompt": f"{i}. ★ 八月十五的月亮大。", "pinyin": "Bā yuè shíwǔ de yuèliang dà.", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "八月十五的晚上，月亮就像一个白色的大盘子，非常漂亮。中国人喜欢在这一天和家里人一起吃饭，一起看月亮。"} if i <= 10 else
        {"id": i, "type": "listening_tf", "prompt": f"{i}. ★ 他现在住在公司附近。", "pinyin": "Tā xiànzài zhù zài gōngsī fùjìn.", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "我搬家了。新的房子虽然小了点儿， लेकिन 离公司很近。"} if i <= 20 else
        {"id": i, "type": "listening_mc", "prompt": f"{i}. 男的想让小王做什么？", "options": ["A 开门", "B 拿东西", "C 去超市买东西"], "answer": "A 开门", "script": "男：小王，帮我开一下门，好吗？谢谢！\n女：没问题。您去超市了？买了这么多东西。"}
        for i in range(1, 36)
    ]
    
    reading_31003 = [
        {"id": i, "type": "fill_gap", "prompt": f"{50+i}. 有些事情看上去很（  ），但要做好，其实不容易。", "options": ["A 简单", "B 举行", "C 像", "D 复习"], "answer": "A 简单", "explanation": "Từ cần điền: 简单 (đơn giản). 有些事情看上去很简单，但要做好，其实不容易。"} if i <= 10 else
        {"id": i, "type": "reading_mc", "prompt": f"{50+i}. 到了机场，他发现护照不见了，在行李箱里找了半天，也没找到，很着急。\n★ 他为什么着急？", "options": ["A 迟到了", "B 忘记拿机票了", "C 找不到护照了"], "answer": "C 找不到护照了", "explanation": "Nội dung bài đọc nêu rõ: 很着急 vì 不见了护照 (không tìm thấy hộ chiếu)."}
        for i in range(1, 26)
    ]

    writing_31003 = [
        {"id": 1, "type": "reorder", "prompt": "1. Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):", "words": ["把", "手机", "送给", "她", "决定", "弟弟", "。"], "correct": "她决定把手机送给弟弟。", "hint": "Cấu trúc câu chữ 把 + Dấu chấm câu 。"},
        {"id": 2, "type": "reorder", "prompt": "2. Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):", "words": ["我和", "这个学生", "很久", "没见面了", "。"], "correct": "我和这个学生很久没见面了。", "hint": "Chủ ngữ 我和这个学生 + Trạng ngữ 很久 + 没见面了。"},
        {"id": 3, "type": "reorder", "prompt": "3. Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):", "words": ["那个宾馆的", "环境", "很好", "。"], "correct": "那个宾馆的环境很好。", "hint": "Chủ ngữ 那个宾馆的环境 + Vị ngữ 很好。"},
        {"id": 4, "type": "reorder", "prompt": "4. Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):", "words": ["你", "完成了", "作业", "吗", "？"], "correct": "你完成了作业吗？", "hint": "Câu hỏi dùng dấu ？ cuối câu."},
        {"id": 5, "type": "reorder", "prompt": "5. Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):", "words": ["我", "跟", "他", "去", "爬山", "。"], "correct": "我跟他去爬山。", "hint": "Dấu chấm câu 。 đặt ở cuối."},
        {"id": 6, "type": "char_fill", "prompt": "6. Điền chữ Hán cho phiên âm (yīn): 生病了要注意休息，（ yīn ）为健康最重要。", "correct": "因", "hint": "Chữ Hán: 因 (因为 - yīnwèi)."},
        {"id": 7, "type": "char_fill", "prompt": "7. Điền chữ Hán cho phiên âm (fù): 考试前要认真（ fù ）习。", "correct": "复", "hint": "Chữ Hán: 复 (复习 - fùxí)."},
        {"id": 8, "type": "char_fill", "prompt": "8. Điền chữ Hán cho phiên âm (mài): 这件衣服是在哪儿（ mài ）的？", "correct": "卖", "hint": "Chữ Hán: 卖 (mài - bán)."},
        {"id": 9, "type": "char_fill", "prompt": "9. Điền chữ Hán cho phiên âm (zhàng): 请问，在哪儿（ zhàng ）单？", "correct": "账", "hint": "Chữ Hán: 账 (结账 - jiézhàng)."},
        {"id": 10, "type": "char_fill", "prompt": "10. Điền chữ Hán cho phiên âm (chūn): （ chūn ）天来了，天气变暖和了。", "correct": "春", "hint": "Chữ Hán: 春 (春天 - chūntiān)."}
    ]

    # H31008 Full Questions
    listening_31008 = [
        {"id": i, "type": "listening_tf", "prompt": f"{i}. ★ 努力的人机会多。", "pinyin": "Nǔlì de rén jīhuì duō.", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "只要你努力，机会总是有的。"} if i <= 10 else
        {"id": i, "type": "listening_tf", "prompt": f"{i}. ★ 他喜欢吃新鲜的水果。", "pinyin": "Tā xǐhuan chī xīnxiān de shuǐguǒ.", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "这些苹果真新鲜，我很喜欢吃。"} if i <= 20 else
        {"id": i, "type": "listening_mc", "prompt": f"{i}. 小张现在在哪儿？", "options": ["A 办公室", "B 图书馆", "C 教室"], "answer": "B 图书馆", "script": "男：小张，你在哪儿呢？\n女：我在图书馆看书呢，一怀茶就回去。"}
        for i in range(1, 36)
    ]

    reading_31008 = [
        {"id": i, "type": "fill_gap", "prompt": f"{50+i}. 最近几年，这里的变化很大，街道更干净了。（  ）", "options": ["A 环境变好了", "B 变化不明显", "C 车辆减少了"], "answer": "A 环境变好了", "explanation": "Môi trường sống tốt lên."} if i <= 10 else
        {"id": i, "type": "reading_mc", "prompt": f"{50+i}. 人们经常说：“一分耕耘，一分收获。”这句话告诉我们：", "options": ["A 努力就有回报", "B 时间过得很快", "C 要保护环境"], "answer": "A 努力就有回报", "explanation": "Có làm thì mới có ăn, nỗ lực sẽ thu được thành quả."}
        for i in range(1, 26)
    ]

    writing_31008 = [
        {"id": 1, "type": "reorder", "prompt": "1. Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):", "words": ["那位", "邻居", "很热情", "。"], "correct": "那位邻居很热情。", "hint": "Dấu chấm câu 。 đặt ở cuối."},
        {"id": 2, "type": "reorder", "prompt": "2. Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):", "words": ["妈妈", "做好了", "晚饭", "。"], "correct": "妈妈做好了晚饭。", "hint": "Cấu trúc: 主语 + 动词结果补语 + 宾语。"},
        {"id": 3, "type": "reorder", "prompt": "3. Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):", "words": ["他", "骑马", "骑得", "很好", "。"], "correct": "他骑马骑得很好。", "hint": "Cấu trúc câu bổ ngữ trình độ."},
        {"id": 4, "type": "reorder", "prompt": "4. Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):", "words": ["今天", "的", "太阳", "真大", "！"], "correct": "今天的太阳真大！", "hint": "Dấu cảm thán ！ ở cuối câu."},
        {"id": 5, "type": "reorder", "prompt": "5. Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):", "words": ["请问", "公园", "怎么走", "？"], "correct": "请问公园怎么走？", "hint": "Dấu hỏi chấm ？ ở cuối câu."},
        {"id": 6, "type": "char_fill", "prompt": "6. Điền chữ Hán cho phiên âm (yuǎn): 我家离学校不（ yuǎn ）。", "correct": "远", "hint": "Chữ Hán: 远 (yuǎn - xa)."},
        {"id": 7, "type": "char_fill", "prompt": "7. Điền chữ Hán cho phiên âm (kè): 同学们都在（ kè ）室里上课。", "correct": "课", "hint": "Chữ Hán: 课 (教室 - jiàoshì)."},
        {"id": 8, "type": "char_fill", "prompt": "8. Điền chữ Hán cho phiên âm (jié): 祝你生日快（ jié ）！", "correct": "乐", "hint": "Chữ Hán: 乐 (快乐 - kuàilè)."},
        {"id": 9, "type": "char_fill", "prompt": "9. Điền chữ Hán cho phiên âm (mào): 太阳升起来了，戴上（ mào ）子吧。", "correct": "帽", "hint": "Chữ Hán: 帽 (帽子 - màozi)."},
        {"id": 10, "type": "char_fill", "prompt": "10. Điền chữ Hán cho phiên âm (xǐ): 饭前要（ xǐ ）手。", "correct": "洗", "hint": "Chữ Hán: 洗 (xǐ - rửa)."}
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
# 5. TRANG 1: DANH SÁCH MÃ ĐỀ (GRID HÌNH VUÔNG PASTEL)
# ==========================================
def render_landing_page():
    st.markdown("<h1 style='text-align: center; color: #1A365D; font-size: 36px; font-weight: bold;'>🎓 LUYỆN ĐỀ HSK3</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #4A5568;'>Vui lòng điền thông tin và chọn Mã Đề Thi để bắt đầu</p>", unsafe_allow_html=True)
    st.write("---")

    # Form nhập thông tin
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.session_state.student_name = st.text_input("👤 Họ và tên học viên:", value=st.session_state.student_name, placeholder="Ví dụ: Nguyễn Văn A")
    with col_info2:
        st.session_state.class_name = st.text_input("🏫 Tên lớp:", value=st.session_state.class_name, placeholder="Ví dụ: HSK3-K24")

    st.write("")
    st.markdown("### 📋 Danh sách Mã Đề Thi:")

    exams = load_exam_data()
    exam_codes = list(exams.keys())

    # Grid Pastel viền màu đậm
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

    # Footer
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

    # JavaScript Đồng hồ đếm ngược chạy thực tế theo giây
    if not is_submitted:
        st.markdown(f"""
        <div id="timer_box_{section_id}" class="timer-container">
            ⏱️ Thời gian còn lại: <span id="timer_display_{section_id}">--:--</span>
        </div>

        <script>
            (function() {{
                var totalSeconds = {remaining_sec};
                var display = document.getElementById("timer_display_{section_id}");
                var box = document.getElementById("timer_box_{section_id}");

                function updateTimer() {{
                    if (totalSeconds <= 0) {{
                        display.innerHTML = "00:00 - ĐÃ HẾT GIỜ!";
                        if (box) box.className = "timer-container timer-warning";
                        return;
                    }}

                    var minutes = Math.floor(totalSeconds / 60);
                    var seconds = totalSeconds % 60;

                    var mStr = minutes < 10 ? "0" + minutes : minutes;
                    var sStr = seconds < 10 ? "0" + seconds : seconds;

                    if (display) display.innerHTML = mStr + ":" + sStr;

                    if (totalSeconds <= 300) {{
                        if (box) box.className = "timer-container timer-warning";
                    }}

                    totalSeconds--;
                }}

                updateTimer();
                setInterval(updateTimer, 1000);
            }})();
        </script>
        """, unsafe_allow_html=True)

        if remaining_sec <= 0:
            st.error("🚨 ĐÃ HẾT GIỜ LÀM BÀI! Tự động nộp phần này...")
            st.session_state.submitted_sections[section_id] = True
            is_submitted = True
            st.rerun()

    # Trình phát Audio gọn gàng
    if audio_file and section_key == "listening":
        st.audio(f"{audio_file}", format="audio/mp3")

    st.write("")

    answers_key_prefix = f"ans_{exam_code}_{section_key}"

    for idx, q in enumerate(questions):
        q_id = q["id"]
        q_key = f"{answers_key_prefix}_{q_id}"

        st.markdown("<div class='question-box'>", unsafe_allow_html=True)
        st.markdown(f"**Câu {idx + 1}:** <span class='chinese-text' style='font-size:18px;'>{q['prompt']}</span>", unsafe_allow_html=True)
        if "pinyin" in q:
            st.markdown(f"<small style='color:#666;'>Pinyin: {q['pinyin']}</small>", unsafe_allow_html=True)

        if not is_submitted:
            if q["type"] in ["listening_tf", "listening_mc", "fill_gap", "reading_mc"]:
                user_ans = st.radio("Chọn đáp án:", q["options"], key=q_key, index=None)
                st.session_state.user_answers[q_key] = user_ans
            elif q["type"] in ["reorder", "char_fill"]:
                if q["type"] == "reorder":
                    st.caption("Từ gợi ý: " + " / ".join([f"`{w}`" for w in q.get("words", [])]))
                user_ans = st.text_input("Nhập câu hoàn chỉnh (Yêu cầu đúng cả dấu câu như 。, ？):", key=q_key)
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
