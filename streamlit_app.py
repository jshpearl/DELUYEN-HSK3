import streamlit as st
import time
import requests
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================
# 1. TRANG TRÍ CSS & CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(
    page_title="LUYỆN ĐỀ HSK3",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Custom CSS cho Font, Màu sắc Pastel, Viền Đậm, Responsive
st.markdown("""
<style>
    /* Font Tahoma cho Tiếng Việt / Pinyin & SimSun cho Chữ Hán */
    @import url('https://fonts.googleapis.com/css2?family=Tahoma&display=swap');
    
    html, body, [class*="css"], div, p, span, label {
        font-family: 'Tahoma', sans-serif;
        color: #2D3748;
        line-height: 1.6;
    }

    /* Target Chữ Hán */
    .zh, .chinese-text, h1, h2, h3, .stRadio label, .stMarkdown {
        font-family: 'SimSun', '宋体', 'Tahoma', serif;
    }

    /* Container chung nền pastel */
    .stApp {
        background-color: #F8F9FA;
    }

    /* Card Mã đề hình vuông, nền pastel, viền đậm */
    .exam-card {
        background-color: #E8F0FE;
        border: 2.5px solid #1A365D;
        border-radius: 12px;
        padding: 25px 15px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 20px;
    }

    /* CSS cho Bảng điểm & Câu hỏi */
    .question-box {
        background-color: #FFFFFF;
        border-left: 5px solid #4A5568;
        border-right: 1px solid #E2E8F0;
        border-top: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 18px;
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

    /* Success Card Banner khi hoàn thành */
    .completion-banner {
        background-color: #E6F4EA;
        border: 2.5px solid #137333;
        border-radius: 12px;
        padding: 22px 18px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(19, 115, 51, 0.1);
    }

    /* Footer Cô Bảo Ngọc */
    .teacher-footer {
        text-align: center;
        padding: 25px 0;
        margin-top: 40px;
        border-top: 1.5px solid #E2E8F0;
        font-size: 22px;
        font-weight: bold;
        color: #2B6CB0;
        font-family: 'SimSun', '宋体', serif;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. DỮ LIỆU ĐỀ THI HSK3
# ==========================================
@st.cache_data
def load_exam_data():
    return {
        "H31003": {
            "title": "Mã đề H31003",
            "audio_file": "H31003.mp3",
            "listening": [
                {
                    "id": 1,
                    "type": "listening_tf",
                    "prompt": "14. ★ 八月十五的月亮大。",
                    "pinyin": "Bā yuè shíwǔ de yuèliang dà.",
                    "options": ["Đúng (√)", "Sai (×)"],
                    "answer": "Đúng (√)",
                    "script": "八月十五的晚上，月亮就像一个白色的大盘子，非常漂亮。中国人喜欢在这一天和家里人一起吃饭，一起看月亮。"
                },
                {
                    "id": 2,
                    "type": "listening_tf",
                    "prompt": "15. ★ 他现在住在公司附近。",
                    "pinyin": "Tā xiànzài zhù zài gōngsī fùjìn.",
                    "options": ["Đúng (√)", "Sai (×)"],
                    "answer": "Đúng (√)",
                    "script": "我搬家了。新的房子虽然小了点儿，但是离公司很近。"
                },
                {
                    "id": 3,
                    "type": "listening_mc",
                    "prompt": "21. 男的想让小王做什么？",
                    "options": ["A 开门", "B 拿东西", "C 去超市买东西"],
                    "answer": "A 开门",
                    "script": "男：小王，帮我开一下门，好吗？谢谢！\n女：没问题。您去超市了？买这么多东西。"
                },
                {
                    "id": 4,
                    "type": "listening_mc",
                    "prompt": "31. 小李现在最可能在哪儿？",
                    "options": ["A 超市", "B 机场", "C 车站"],
                    "answer": "A 超市",
                    "script": "男：喂，请问小李在家吗？\n女：他出去了。他去超市买点儿东西，可能十分钟就回来了。"
                }
            ],
            "reading": [
                {
                    "id": 1,
                    "type": "fill_gap",
                    "prompt": "51. 有些事情看上去很（  ），但要做好，其实不容易。",
                    "options": ["A 简单", "B 举行", "C 像", "D 复习"],
                    "answer": "A 简单",
                    "explanation": "Từ cần điền: 简单 (đơn giản). Có những việc nhìn đơn giản nhưng làm không dễ."
                },
                {
                    "id": 2,
                    "type": "fill_gap",
                    "prompt": "52. 听张先生说，机场（  ）那个宾馆的环境不错。",
                    "options": ["A 简单", "B 附近", "C 像", "D 复习"],
                    "answer": "B 附近",
                    "explanation": "Từ cần điền: 附近 (gần/lân cận). Khách sạn ở gần sân bay."
                },
                {
                    "id": 3,
                    "type": "reading_mc",
                    "prompt": "61. 到了机场，他发现护照不见了，在行李箱里找了半天，也没找到，很着急。\n★ 他为什么着急？",
                    "options": ["A 迟到了", "B 忘记拿机票了", "C 找不到护照了"],
                    "answer": "C 找不到护照了",
                    "explanation": "Nội dung bài đọc nêu rõ: 很着急 vì 不见了护照 (không tìm thấy hộ chiếu)."
                },
                {
                    "id": 4,
                    "type": "reading_mc",
                    "prompt": "62. 人们经常说：“面包会有的，牛奶也会有的。”是的，如果努力，什么都会有的。\n★ 这句话主要想告诉我们：",
                    "options": ["A 要相信别人", "B 兴趣最重要", "C 努力才有希望"],
                    "answer": "C 努力才有希望",
                    "explanation": "Chủ đề chính: 如果努力，什么都会有的 (Nỗ lực mới có hy vọng)."
                }
            ],
            "writing": [
                {
                    "id": 1,
                    "type": "reorder",
                    "prompt": "Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):",
                    "words": ["把", "手机", "送给", "她", "决定", "弟弟", "。"],
                    "correct": "她决定把手机送给弟弟。",
                    "hint": "Chú ý cấu trúc câu chữ 把 và dấu chấm câu 。 cuối câu."
                },
                {
                    "id": 2,
                    "type": "reorder",
                    "prompt": "Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):",
                    "words": ["这个学生", "我和", "很久", "没见面了", "。"],
                    "correct": "我和这个学生很久没见面了。",
                    "hint": "Chủ ngữ 我和这个学生 + Trạng ngữ 很久 + 没见面了。"
                },
                {
                    "id": 3,
                    "type": "char_fill",
                    "prompt": "Điền chữ Hán chính xác cho phiên âm (yīn): 生病了要注意休息，（ yīn ）为健康最重要。",
                    "correct": "因",
                    "hint": "Chữ Hán: 因 (因为 - yīnwèi)."
                }
            ]
        },
        "H31006": {
            "title": "Mã đề H31006",
            "audio_file": "H31006.mp3",
            "listening": [
                {
                    "id": 1,
                    "type": "listening_tf",
                    "prompt": "16. ★ 他在眼镜店里。",
                    "options": ["Đúng (√)", "Sai (×)"],
                    "answer": "Đúng (√)",
                    "script": "这家眼镜店的服务很好，我的眼镜就是在他们家买的。"
                }
            ],
            "reading": [
                {
                    "id": 1,
                    "type": "fill_gap",
                    "prompt": "51. 这个城市已经有 900 多年的历史了，非常（  ）。",
                    "options": ["A 有名", "B 变化", "C 瘦"],
                    "answer": "A 有名",
                    "explanation": "Có lịch sử hơn 900 năm nên rất 有名 (nổi tiếng)."
                }
            ],
            "writing": [
                {
                    "id": 1,
                    "type": "reorder",
                    "prompt": "Sắp xếp từ thành câu đúng (Yêu cầu chính xác 100% cả dấu câu):",
                    "words": ["咖啡里", "放糖", "不要", "。"],
                    "correct": "咖啡里不要放糖。",
                    "hint": "Cấu trúc: 咖啡里不要放糖。"
                }
            ]
        },
        "H31008": {
            "title": "Mã đề H31008",
            "audio_file": "H31008.mp3",
            "listening": [
                {
                    "id": 1,
                    "type": "listening_tf",
                    "prompt": "18. ★ 努力的人机会多。",
                    "options": ["Đúng (√)", "Sai (×)"],
                    "answer": "Đúng (√)",
                    "script": "只要你努力，机会总是有的。"
                }
            ],
            "reading": [
                {
                    "id": 1,
                    "type": "reading_mc",
                    "prompt": "61. 最近几年，这里的变化很大，车辆更多了，街道更干净了，天更蓝了。\n★ 这里最近几年怎么样？",
                    "options": ["A 环境变好了", "B 和过去相同", "C 变得更差了"],
                    "answer": "A 环境变好了",
                    "explanation": "Môi trường tốt lên."
                }
            ],
            "writing": [
                {
                    "id": 1,
                    "type": "reorder",
                    "prompt": "Sắp xếp câu chính xác (gồm cả dấu câu):",
                    "words": ["那位", "邻居", "很热情", "。"],
                    "correct": "那位邻居很热情。",
                    "hint": "Dấu chấm câu 。 đặt ở cuối."
                }
            ]
        },
        "H31111": {
            "title": "Mã đề H31111",
            "audio_file": "H31111.mp3",
            "listening": [
                {
                    "id": 1,
                    "type": "listening_tf",
                    "prompt": "11. ★ 校长还认识他。",
                    "options": ["Đúng (√)", "Sai (×)"],
                    "answer": "Đúng (√)",
                    "script": "没想到过了这么多年，校长依然能叫出他的名字。"
                }
            ],
            "reading": [
                {
                    "id": 1,
                    "type": "reading_mc",
                    "prompt": "61. 昨天，我送给妻子一个礼物，是一辆红色的汽车，她高兴极了。\n★ 妻子为什么很高兴？",
                    "options": ["A 搬新家了", "B 换了辆新车", "C 把旧车卖了"],
                    "answer": "B 换了辆新车",
                    "explanation": "Được tặng xe ô tô mới."
                }
            ],
            "writing": [
                {
                    "id": 1,
                    "type": "reorder",
                    "prompt": "Sắp xếp từ thành câu đúng (Bắt buộc đúng dấu câu):",
                    "words": ["完成", "了", "你的作业", "吗", "？"],
                    "correct": "完成了你的作业吗？",
                    "hint": "Cuối câu dùng dấu hỏi chấm ？"
                }
            ]
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
        "student_id": class_name,  # Lưu tên lớp vào cột lớp/mã số
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
# 4. COMPONENT ĐỒNG HỒ ĐẾM NGƯỢC JAVASCRIPT THỰC TẾ
# ==========================================
def render_live_timer(remaining_sec, section_key):
    timer_html = f"""
    <div id="timer-card-{section_key}" style="
        background-color: #FFF5F5;
        border: 2.5px solid #E53E3E;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        color: #C53030;
        text-align: center;
        font-family: 'Tahoma', sans-serif;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    ">
        ⏱️ Thời gian còn lại: <span id="time-display-{section_key}">--:--</span>
        <span id="warning-text-{section_key}" style="display:none; color:#C53030; margin-left:10px; font-size:16px;">⚠️ SẮP HẾT GIỜ!</span>
    </div>
    <script>
        (function() {{
            var totalSeconds = {remaining_sec};
            var timerCard = document.getElementById("timer-card-{section_key}");
            var timeDisplay = document.getElementById("time-display-{section_key}");
            var warningText = document.getElementById("warning-text-{section_key}");
            
            function updateTimer() {{
                if (totalSeconds <= 0) {{
                    timeDisplay.innerHTML = "00:00 - ĐÃ HẾT GIỜ!";
                    timerCard.style.backgroundColor = "#FED7D7";
                    timerCard.style.color = "#9B2C2C";
                    return;
                }}
                
                var mins = Math.floor(totalSeconds / 60);
                var secs = totalSeconds % 60;
                var minsStr = mins < 10 ? "0" + mins : mins;
                var secsStr = secs < 10 ? "0" + secs : secs;
                
                timeDisplay.innerHTML = minsStr + ":" + secsStr;
                
                if (totalSeconds <= 300) {{
                    warningText.style.display = "inline";
                    timerCard.style.backgroundColor = "#FED7D7";
                    timerCard.style.borderColor = "#E53E3E";
                }}
                
                totalSeconds--;
            }}
            
            updateTimer();
            setInterval(updateTimer, 1000);
        }})();
    </script>
    """
    components.html(timer_html, height=75)


# ==========================================
# 5. QUẢN LÝ SESSION STATE
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
# 6. TRANG 1: DANH SÁCH MÃ ĐỀ (LUYỆN ĐỀ HSK3)
# ==========================================
def render_landing_page():
    st.markdown("<h1 style='text-align: center; color: #1A365D; font-weight: bold;'>LUYỆN ĐỀ HSK3</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #4A5568;'>Vui lòng nhập thông tin học viên và chọn Mã Đề Thi để bắt đầu</p>", unsafe_allow_html=True)
    st.write("---")

    # Nhập thông tin thí sinh: Họ tên & Tên lớp (Bỏ mã học viên)
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.session_state.student_name = st.text_input("👤 Họ và tên học viên:", value=st.session_state.student_name, placeholder="Ví dụ: Nguyễn Văn A")
    with col_info2:
        st.session_state.class_name = st.text_input("🏫 Tên lớp:", value=st.session_state.class_name, placeholder="Ví dụ: Lớp HSK3-K24")

    st.write("")
    st.markdown("### 📋 Danh sách Mã Đề Thi HSK3:")

    exams = load_exam_data()
    exam_codes = list(exams.keys())

    # Hiển thị Grid 4 hình vuông pastel
    cols = st.columns(4)
    pastel_colors = ["#E8F0FE", "#E6F4EA", "#FCE8E6", "#FEF7E0"]
    border_colors = ["#1A365D", "#137333", "#C5221F", "#B06000"]

    for idx, code in enumerate(exam_codes):
        with cols[idx % 4]:
            p_bg = pastel_colors[idx % len(pastel_colors)]
            p_border = border_colors[idx % len(border_colors)]
            
            st.markdown(f"""
            <div style="background-color: {p_bg}; border: 2.5px solid {p_border}; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 12px;">
                <div style="font-size: 24px; font-weight: bold; color: {p_border}; font-family: 'Tahoma', sans-serif;">{code}</div>
                <div style="font-size: 13px; color: #555; margin-top: 5px;">Đề thi chuẩn HSK3</div>
                <div style="font-size: 12px; color: #777;">Listening • Reading • Writing</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"👉 Vào làm đề {code}", key=f"btn_{code}", use_container_width=True):
                if not st.session_state.student_name.strip():
                    st.error("⚠️ Vui lòng nhập Họ và Tên học viên trước khi bắt đầu!")
                else:
                    st.session_state.selected_exam = code
                    st.rerun()

    # Footer
    st.markdown("<div class='teacher-footer'>黄宝玉老师</div>", unsafe_allow_html=True)


# ==========================================
# 7. TRANG 2: TRANG LÀM BÀI CÁC PHẦN (3 TABS)
# ==========================================
def render_exam_page(exam_code):
    exams = load_exam_data()
    exam = exams[exam_code]

    # Header trang thi
    col_head1, col_head2 = st.columns([3, 1])
    with col_head1:
        st.markdown(f"# LUYỆN ĐỀ HSK3 - <span style='color:#1A365D;'>{exam_code}</span>", unsafe_allow_html=True)
        class_str = f" - Lớp: {st.session_state.class_name}" if st.session_state.class_name else ""
        st.markdown(f"**Học viên:** `{st.session_state.student_name}`{class_str}")
    with col_head2:
        if st.button("⬅️ Trở về chọn đề khác"):
            st.session_state.selected_exam = None
            st.rerun()

    st.write("---")

    # Quy định thời gian thi
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

    # 3 Tabs
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
            section_title="PHẦN VIẾT (书写) - Chấm nghiêm ngặt cả dấu câu",
            questions=exam["writing"],
            max_time_sec=SECTION_TIMES["writing"]
        )

    st.markdown("<div class='teacher-footer'>黄宝玉老师</div>", unsafe_allow_html=True)


# ==========================================
# 8. HÀM HIỂN THỊ CHI TIẾT TỪNG PHẦN THI
# ==========================================
def render_section_tab(exam_code, section_key, section_title, questions, max_time_sec, audio_file=None):
    st.subheader(f"📌 {section_title}")

    section_id = f"{exam_code}_{section_key}"
    is_submitted = st.session_state.submitted_sections.get(section_id, False)

    start_time = st.session_state.exam_start_times[exam_code][section_key]
    elapsed = time.time() - start_time
    remaining_sec = max(0, int(max_time_sec - elapsed))

    # Nếu chưa nộp, hiển thị Đồng hồ đếm ngược Javascript chạy thực tế
    if not is_submitted:
        render_live_timer(remaining_sec, section_key)

    if audio_file and section_key == "listening":
        st.info(f"📻 Audio đính kèm: `{audio_file}` (Tên file audio trùng mã đề)")
        st.audio(f"{audio_file}", format="audio/mp3")

    st.write("")

    answers_key_prefix = f"ans_{exam_code}_{section_key}"

    # Nếu đã nộp bài, hiển thị Dòng thông báo đúng yêu cầu
    if is_submitted:
        correct_count = sum([
            1 for q in questions if (
                (st.session_state.user_answers.get(f"{answers_key_prefix}_{q['id']}", "").strip() == q["correct"].strip())
                if q["type"] in ["reorder", "char_fill"]
                else (st.session_state.user_answers.get(f"{answers_key_prefix}_{q['id']}", "") == q["answer"])
            )
        ])
        total_q = len(questions)
        pct = round((correct_count / total_q) * 100, 1) if total_q > 0 else 0

        st.markdown(f"""
        <div class="completion-banner">
            <h2 style="color: #137333; margin: 0; font-size: 22px; font-weight: bold;">
                🎉 Chúc mừng "{st.session_state.student_name}" đã hoàn thành đề "{exam_code}" ({section_title})
            </h2>
            <p style="font-size: 19px; color: #2D3748; margin-top: 12px; font-weight: bold;">
                Điểm số của bạn là: <span style="color: #137333; font-size: 26px;">{correct_count}/{total_q}</span> ({pct}%)
            </p>
        </div>
        """, unsafe_allow_html=True)

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
                user_ans = st.text_input("Nhập câu hoàn chỉnh (Khớp 100% cả dấu câu tiếng Trung như 。, ？):", key=q_key)
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
                    • Đáp án bạn nhập/chọn: <code style='color:red;'>{user_ans if user_ans else '(Chưa trả lời)'}</code><br>
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


def main():
    if st.session_state.selected_exam is None:
        render_landing_page()
    else:
        render_exam_page(st.session_state.selected_exam)

if __name__ == "__main__":
    main()
