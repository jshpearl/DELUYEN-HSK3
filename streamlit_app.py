import streamlit as st
import json
import random
import requests
import datetime
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="HSK 3 Master - Cô Bảo Ngọc",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- WEBHOOK CONFIG ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwwH0wE3X1zJ5kK5M3N7P8Q9R0S1T2U3V4W5X6Y7Z/exec"

def send_to_google_sheet(user_name, group_name, score, total, percentage):
    vn_tz = datetime.timezone(datetime.timedelta(hours=7))
    vn_now = datetime.datetime.now(vn_tz)
    payload = {
        "timestamp": vn_now.strftime("%Y-%m-%d %H:%M:%S"),
        "name": user_name,
        "group": group_name,
        "score": f"{score}/{total}",
        "percentage": f"{percentage:.1f}%"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=8)
        if response.status_code == 200:
            return True, "Thành công"
        else:
            return False, f"HTTP Status {response.status_code}"
    except Exception as e:
        return False, str(e)

# --- BẢNG MÀU 7 SẮC PASTEL (HỒNG, TÍM, XANH DƯƠNG, XANH LÁ, VÀNG, CAM, XÁM NÂU) ---
PASTEL_THEMES = [
    {
        "name": "Hồng Pastel", "emoji": "🌸",
        "bg_gradient": "linear-gradient(135deg, #FDF2F8 0%, #FCE7F3 100%)",
        "card_bg": "#FDF2F8", "border": "#EC4899", "title_color": "#831843",
        "fc_front_bg": "linear-gradient(135deg, #FFFFFF 0%, #FDF2F8 100%)", "fc_front_border": "#FBCFE8", "fc_front_text": "#9D174D",
        "fc_back_bg": "linear-gradient(135deg, #DB2777 0%, #F472B6 100%)", "fc_back_border": "#BE185D",
        "badge_bg": "#FCE7F3", "badge_text": "#9D174D"
    },
    {
        "name": "Tím Pastel", "emoji": "🟣",
        "bg_gradient": "linear-gradient(135deg, #FAF5FF 0%, #F3E8FF 100%)",
        "card_bg": "#FAF5FF", "border": "#A855F7", "title_color": "#581C87",
        "fc_front_bg": "linear-gradient(135deg, #FFFFFF 0%, #FAF5FF 100%)", "fc_front_border": "#DDD6FE", "fc_front_text": "#6B21A8",
        "fc_back_bg": "linear-gradient(135deg, #9333EA 0%, #C084FC 100%)", "fc_back_border": "#7E22CE",
        "badge_bg": "#F3E8FF", "badge_text": "#6B21A8"
    },
    {
        "name": "Xanh Dương Pastel", "emoji": "🔵",
        "bg_gradient": "linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%)",
        "card_bg": "#F0F9FF", "border": "#0EA5E9", "title_color": "#0C4A6E",
        "fc_front_bg": "linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%)", "fc_front_border": "#BAE6FD", "fc_front_text": "#0369A1",
        "fc_back_bg": "linear-gradient(135deg, #0284C7 0%, #38BDF8 100%)", "fc_back_border": "#0369A1",
        "badge_bg": "#E0F2FE", "badge_text": "#0369A1"
    },
    {
        "name": "Xanh Lá Pastel", "emoji": "🟢",
        "bg_gradient": "linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%)",
        "card_bg": "#F0FDF4", "border": "#22C55E", "title_color": "#14532D",
        "fc_front_bg": "linear-gradient(135deg, #FFFFFF 0%, #F0FDF4 100%)", "fc_front_border": "#BBF7D0", "fc_front_text": "#15803D",
        "fc_back_bg": "linear-gradient(135deg, #16A34A 0%, #4ADE80 100%)", "fc_back_border": "#15803D",
        "badge_bg": "#DCFCE7", "badge_text": "#15803D"
    },
    {
        "name": "Vàng Pastel", "emoji": "🟡",
        "bg_gradient": "linear-gradient(135deg, #FEFCE8 0%, #FEF9C3 100%)",
        "card_bg": "#FEFCE8", "border": "#EAB308", "title_color": "#713F12",
        "fc_front_bg": "linear-gradient(135deg, #FFFFFF 0%, #FEFCE8 100%)", "fc_front_border": "#FEF08A", "fc_front_text": "#A16207",
        "fc_back_bg": "linear-gradient(135deg, #CA8A04 0%, #FACC15 100%)", "fc_back_border": "#A16207",
        "badge_bg": "#FEF9C3", "badge_text": "#854D0E"
    },
    {
        "name": "Cam Pastel", "emoji": "🟠",
        "bg_gradient": "linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%)",
        "card_bg": "#FFF7ED", "border": "#F97316", "title_color": "#7C2D12",
        "fc_front_bg": "linear-gradient(135deg, #FFFFFF 0%, #FFF7ED 100%)", "fc_front_border": "#FED7AA", "fc_front_text": "#C2410C",
        "fc_back_bg": "linear-gradient(135deg, #EA580C 0%, #FB923C 100%)", "fc_back_border": "#C2410C",
        "badge_bg": "#FFEDD5", "badge_text": "#9A3412"
    },
    {
        "name": "Xám Nâu Pastel", "emoji": "🌰",
        "bg_gradient": "linear-gradient(135deg, #FAFAF9 0%, #F5F5F4 100%)",
        "card_bg": "#FAFAF9", "border": "#A8A29E", "title_color": "#44403C",
        "fc_front_bg": "linear-gradient(135deg, #FFFFFF 0%, #FAFAF9 100%)", "fc_front_border": "#E7E5E4", "fc_front_text": "#57534E",
        "fc_back_bg": "linear-gradient(135deg, #78350F 0%, #B45309 100%)", "fc_back_border": "#57534E",
        "badge_bg": "#F5F5F4", "badge_text": "#44403C"
    }
]

# --- GLOBAL STYLING WITH 7-PASTEL RAINBOW AURORA ---
st.markdown("""
<style>
    /* 1. Ẩn Sidebar & Header mặc định */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }

    /* 2. Áp dụng Font Tahoma & Nền Pastel 7 màu hòa quyện */
    html, body, [class*="css"], .stApp {
        font-family: 'Tahoma', Geneva, Verdana, sans-serif !important;
    }
    .stApp {
        background: linear-gradient(135deg, #FFF5F7 0%, #FEF9C3 20%, #FFEDD5 40%, #DCFCE7 60%, #E0F2FE 80%, #F3E8FF 100%) !important;
    }

    /* 3. Header Box Với Cầu Vồng 7 Sắc Pastel */
    .header-box {
        text-align: center;
        padding: 26px 20px;
        background: linear-gradient(135deg, #EC4899 0%, #A855F7 20%, #0EA5E9 40%, #22C55E 60%, #EAB308 80%, #F97316 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(168, 85, 247, 0.25);
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: 0.5px;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
    }
    .sub-title {
        font-size: 1.05rem;
        opacity: 0.95;
        margin-top: 8px;
    }

    /* 4. Thẻ Nhập Họ tên */
    .user-info-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 2px solid #E0E7FF;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        margin-bottom: 25px;
    }

    /* 5. Flashcard 3D Structure */
    .flip-card {
        background-color: transparent;
        width: 100%;
        height: 240px;
        perspective: 1000px;
        margin-bottom: 15px;
    }
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s;
        transform-style: preserve-3d;
        cursor: pointer;
    }
    .flip-card:hover .flip-card-inner {
        transform: rotateY(180deg);
    }
    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.06);
    }

    /* 6. Footer Chữ ký */
    .teacher-footer {
        text-align: center;
        color: #6B21A8;
        font-size: 1.35rem;
        font-weight: 900;
        margin-top: 40px;
        margin-bottom: 25px;
        padding-top: 15px;
        border-top: 2px dashed #CBD5E1;
    }

    .congrats-card {
        background-color: #DCFCE7;
        border: 2px solid #16A34A;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: #000000 !important;
        font-size: 1.3rem;
        font-weight: 900;
        margin-top: 10px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA TỪ FILE DATA.JSON ---
@st.cache_data
def load_all_data():
    json_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

ORDERED_GROUPS = load_all_data()

# --- HEADER MAIN ---
st.markdown('<div class="header-box"><div class="main-title">✨ CHINH PHỤC TỪ VỰNG HSK 3 ✨</div><div class="sub-title">Cùng học và ôn trọn bộ 300 từ vựng HSK3 nhé</div></div>', unsafe_allow_html=True)

# --- USER NAME INPUT ---
st.markdown('<div class="user-info-card">', unsafe_allow_html=True)
user_name = st.text_input("👤 Họ và tên người học (Bắt buộc nhập tên để nộp bài):", value="", placeholder="Vui lòng nhập họ và tên của bạn tại đây...", key="user_name_input")
st.markdown('</div>', unsafe_allow_html=True)

# --- GROUP SELECTOR ---
group_titles = [g["title"] for g in ORDERED_GROUPS]
selected_group_title = st.selectbox("📌 Chọn Nhóm từ vựng để học và làm bài tập:", options=group_titles, index=0)

group_idx = next(i for i, g in enumerate(ORDERED_GROUPS) if g["title"] == selected_group_title)
group_info = ORDERED_GROUPS[group_idx]

# Assign 1 of the 7 Pastel Color Themes based on group_idx
theme = PASTEL_THEMES[group_idx % 7]



st.markdown(f"### 📌 {group_info['title']} (20 từ vựng & Bài tập)")

# PHẦN 1: FLASHCARD & BẢNG TỪ VỰNG
fc_key = f"fc_index_{group_info['id']}"
show_table_key = f"show_table_{group_info['id']}"

if fc_key not in st.session_state:
    st.session_state[fc_key] = 0
if show_table_key not in st.session_state:
    st.session_state[show_table_key] = False

vocab_list = group_info["vocab"]
curr_idx = st.session_state[fc_key]
curr_item = vocab_list[curr_idx]

flip_card_html = f"""
<div class="flip-card">
  <div class="flip-card-inner">
    <div class="flip-card-front" style="background:{theme['fc_front_bg']}; border:3px solid {theme['fc_front_border']}; color:{theme['fc_front_text']};">
      <div style="font-size:0.95rem; font-weight:800; margin-bottom:8px; opacity:0.8;">✦ CLICK / DI CHUỘT ĐỂ XEM NGHĨA ✦</div>
      <div style="font-size:3.2rem; font-weight:900;">{curr_item['hanzi']}</div>
    </div>
    <div class="flip-card-back" style="background:{theme['fc_back_bg']}; border:3px solid {theme['fc_back_border']}; color:white;">
      <div style="font-size:2.2rem; font-weight:900; margin-bottom:4px;">{curr_item['hanzi']}</div>
      <div style="font-size:1.3rem; font-weight:700; color:#FEF08A; margin-bottom:6px;">[{curr_item['pinyin']}] • {curr_item['type']}</div>
      <div style="font-size:1.4rem; font-weight:900; margin-bottom:10px;">👉 {curr_item['meaning']}</div>
      <div style="font-size:1.05rem; background:rgba(255,255,255,0.2); padding:8px 12px; border-radius:10px;">💡 {curr_item['example']}</div>
    </div>
  </div>
</div>
"""
st.markdown(flip_card_html, unsafe_allow_html=True)

col_prev, col_num, col_next = st.columns([1, 2, 1])
with col_prev:
    if st.button("⬅️ Từ trước", key=f"prev_{group_info['id']}", use_container_width=True):
        st.session_state[fc_key] = (curr_idx - 1) % len(vocab_list)
        st.rerun()
with col_num:
    st.markdown(f"<div style='text-align:center; font-weight:800; font-size:1.1rem; padding-top:6px; color:{theme['title_color']};'>Thẻ {curr_idx + 1} / {len(vocab_list)}</div>", unsafe_allow_html=True)
with col_next:
    if st.button("Từ tiếp ➡️", key=f"next_{group_info['id']}", use_container_width=True):
        st.session_state[fc_key] = (curr_idx + 1) % len(vocab_list)
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
btn_table_label = "🙈 Thu gọn Bảng từ vựng" if st.session_state[show_table_key] else "📖 Mở rộng Bảng 20 từ vựng Nhóm này"
if st.button(btn_table_label, key=f"btn_tb_{group_info['id']}", use_container_width=True):
    st.session_state[show_table_key] = not st.session_state[show_table_key]
    st.rerun()

if st.session_state[show_table_key]:
    table_md = "| STT | Chữ Hán | Phiên âm | Từ loại | Ý nghĩa | Ví dụ minh họa |\n| :---: | :---: | :---: | :---: | :--- | :--- |\n"
    for v_i, v_data in enumerate(vocab_list, 1):
        table_md += f"| {v_i} | **{v_data['hanzi']}** | {v_data['pinyin']} | *{v_data['type']}* | {v_data['meaning']} | {v_data['example']} |\n"
    st.markdown(table_md)

st.markdown(f"<hr style='border:1px dashed {theme['border']}; margin:25px 0;'>", unsafe_allow_html=True)

# PHẦN 2: BÀI TẬP 4 TABS
def render_quiz_section(sub_quiz_data, sub_key):
    submitted_flag = f"sub_submitted_{group_info['id']}_{sub_key}"
    res_data_flag = f"sub_res_data_{group_info['id']}_{sub_key}"

    if submitted_flag not in st.session_state:
        st.session_state[submitted_flag] = False

    if st.session_state[submitted_flag] and res_data_flag in st.session_state:
        res = st.session_state[res_data_flag]
        st.markdown('''<div class="congrats-card">🎉 Chúc mừng bạn đã làm xong! Chăm chỉ quá!</div>''', unsafe_allow_html=True)

        st.metric("Kết quả làm bài", f"{res['score']} / {res['total']} câu đúng", f"{res['pct']:.1f}%")

        if res['score'] < res['total']:
            st.markdown('''<div style="background-color: #FEF3C7; border: 2px solid #F59E0B; border-radius: 12px; padding: 12px 16px; margin-top: 10px; margin-bottom: 15px; color: #92400E; font-weight: 800; text-align: center; font-size: 1.05rem;">💡 Bạn hãy kiểm tra lại danh sách câu hỏi bên dưới để xem đáp án đúng và lời giải thích chi tiết cho các câu làm chưa chính xác nhé!</div>''', unsafe_allow_html=True)

        if res['ok']:
            st.success(f"✅ Đã gửi điểm về Sheet cho cô Bảo Ngọc ({user_name.strip()}: {res['score']}/{res['total']})")
        else:
            st.info(f"ℹ️ Đã ghi nhận điểm trên ứng dụng: {res['score']}/{res['total']} câu đúng. ({res['msg']})")

    user_ans = {}
    for q_i, q_data in enumerate(sub_quiz_data):
        # Khung câu hỏi thiết kế theo chủ đề Pastel của nhóm
        q_card_html = f"""
        <div style="background-color:{theme['card_bg']}; border-left:5px solid {theme['border']}; border-radius:12px; padding:14px 18px; margin-top:15px; margin-bottom:12px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="color:{theme['title_color']}; font-size:1.12rem; font-weight:800; line-height:1.5;">Câu {q_i + 1}: {q_data['q']}</div>
        </div>
        """
        st.markdown(q_card_html, unsafe_allow_html=True)

        shuffled_key = f"shuffled_opts_{group_info['id']}_{sub_key}_{q_i}"
        if shuffled_key not in st.session_state:
            opts = list(q_data["options"])
            random.shuffle(opts)
            st.session_state[shuffled_key] = opts
        else:
            opts = st.session_state[shuffled_key]

        radio_key = f"q_{group_info['id']}_{sub_key}_{q_i}"
        ans = st.radio(
            f"Chọn đáp án câu {q_i + 1}:",
            opts,
            key=radio_key,
            index=None,
            label_visibility="collapsed"
        )
        user_ans[q_i] = ans

        if st.session_state[submitted_flag]:
            if ans == q_data["ans"]:
                st.success(f"✅ Đúng! ({q_data['ans']}) — {q_data['exp']}")
            elif ans is not None:
                st.error(f"❌ Chưa đúng! Đáp án đúng là: **{q_data['ans']}** — 💡 {q_data['exp']}")
            else:
                st.warning(f"⚠️ Chưa trả lời. Đáp án đúng là: **{q_data['ans']}** — 💡 {q_data['exp']}")

        st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        sub_btn = st.button(f"🚀 Nộp bài - {sub_key}", key=f"btn_sub_{group_info['id']}_{sub_key}", type="primary", use_container_width=True)
    with col_btn2:
        redo_btn = st.button(f"🔄 Làm lại phần này", key=f"btn_redo_{group_info['id']}_{sub_key}", use_container_width=True)

    if redo_btn:
        st.session_state[submitted_flag] = False
        if res_data_flag in st.session_state:
            del st.session_state[res_data_flag]
        for q_i in range(len(sub_quiz_data)):
            r_k = f"q_{group_info['id']}_{sub_key}_{q_i}"
            if r_k in st.session_state:
                del st.session_state[r_k]
        st.rerun()

    if sub_btn:
        if not user_name or not user_name.strip() or user_name.strip().lower() in ["", "học viên hsk3"]:
            st.warning("⚠️ Vui lòng nhập Họ và tên ở ô thông tin phía trên trước khi nộp bài!")
        else:
            st.session_state[submitted_flag] = True
            score = 0
            unans = 0
            for q_i, q_data in enumerate(sub_quiz_data):
                ans = user_ans.get(q_i)
                if ans is None:
                    unans += 1
                elif ans == q_data["ans"]:
                    score += 1

            total = len(sub_quiz_data)
            pct = (score / total) * 100

            with st.spinner("Đang gửi điểm về Google Sheet cho cô Bảo Ngọc..."):
                ok, msg = send_to_google_sheet(
                    user_name=user_name.strip(),
                    group_name=f"{group_info['title']} - {sub_key}",
                    score=score,
                    total=total,
                    percentage=pct
                )

            st.session_state[res_data_flag] = {
                "score": score,
                "total": total,
                "pct": pct,
                "unans": unans,
                "ok": ok,
                "msg": msg
            }

            st.rerun()

sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs(["📝 1. Kiểm tra từ vựng", "✏️ 2. Điền vào chỗ trống", "🧩 3. Sắp xếp câu", "💬 4. Chọn câu trả lời"])

with sub_tab1:
    render_quiz_section(group_info["tab1"], "Kiểm tra từ vựng")
with sub_tab2:
    render_quiz_section(group_info["tab2"], "Điền vào chỗ trống")
with sub_tab3:
    render_quiz_section(group_info["tab3"], "Sắp xếp câu")
with sub_tab4:
    render_quiz_section(group_info["tab4"], "Chọn câu trả lời")

st.markdown('<div class="teacher-footer">黄宝玉老师</div>', unsafe_allow_html=True)
