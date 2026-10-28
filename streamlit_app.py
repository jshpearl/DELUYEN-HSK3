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

    /* Header & Đồng hồ */
    .timer-box {
        background-color: #FFF5F5;
        border: 2px solid #E53E3E;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: bold;
        color: #C53030;
        text-align: center;
        margin-bottom: 15px;
    }

    .timer-warning {
        animation: blinker 1s linear infinite;
        background-color: #FED7D7 !important;
    }

    @keyframes blinker {
        50% { opacity: 0.5; }
    }

    /* CSS cho Bảng điểm & Câu hỏi */
    .question-box {
        background-color: #FFFFFF;
        border-left: 5px solid #4A5568;
        border-right: 1px solid #E2E8F0;
        border-top: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 18px;
    }

    .correct-answer {
        background-color: #F0FFF4;
        border-left: 5px solid #38A169;
        padding: 10px;
        border-radius: 4px;
        margin-top: 8px;
    }

    .wrong-answer {
        background-color: #FFF5F5;
        border-left: 5px solid #E53E3E;
        padding: 10px;
        border-radius: 4px;
        margin-top: 8px;
    }

    /* Banner hoàn thành */
    .completion-banner {
        background-color: #EBF8FF;
        border: 2px solid #3182CE;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        text-align: center;
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
# 2. DỮ LIỆU ĐỀ THI HSK3 ĐẦY ĐỦ 4 ĐỀ
# ==========================================
@st.cache_data
def load_exam_data():
    return {
        "H31003": {
            "title": "Mã đề H31003",
            "audio_file": "H31003.mp3",
            "listening": [
                {"id": 1, "type": "listening_mc", "prompt": "1. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "E", "script": "女：下了飞机，就给我来电话。\n男：好的。你到中国以后，自己照顾好自己。"},
                {"id": 2, "type": "listening_mc", "prompt": "2. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "B", "script": "男：请问，二零四房间在哪儿？\n女：请这边走，前面左边第二个就是。"},
                {"id": 3, "type": "listening_mc", "prompt": "3. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "C", "script": "女：眼药水用了吗？有作用没？\n男：有作用，现在眼睛已经不红了。"},
                {"id": 4, "type": "listening_mc", "prompt": "4. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "F", "script": "男：这些书我可以借多长时间？\n女：一个月。如果看不完，可以再借一个月。"},
                {"id": 5, "type": "listening_mc", "prompt": "5. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "A", "script": "女：这张画是你画的吗？\n男：是我爷爷画的，这是他的一张花鸟画。"},
                {"id": 11, "type": "listening_tf", "prompt": "11. ★ 冬天水果很便宜。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "在这里，冬天的水果虽然比夏天的贵，但是新鲜。"},
                {"id": 12, "type": "listening_tf", "prompt": "12. ★ 他现在还不能打篮球。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "太好了！他几乎不敢相信这是真的。医生说他很快就能像以前一样打篮球了。"},
                {"id": 13, "type": "listening_tf", "prompt": "13. ★ 儿子比爸爸矮。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "儿子十七岁了，长得很快。去年买的裤子，现在已经不能穿了，现在他和他爸爸一样高了。"},
                {"id": 14, "type": "listening_tf", "prompt": "14. ★ 八月十五的月亮大。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "八月十五的晚上，月亮就像一个白色的大盘子，非常漂亮。中国人喜欢在这一天和家里人一起吃饭，一起看月亮。"},
                {"id": 15, "type": "listening_tf", "prompt": "15. ★ 他现在住在公司附近。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "我搬家了。新的房子虽然小了点儿，但是离公司很近。"},
                {"id": 16, "type": "listening_tf", "prompt": "16. ★ 女儿喜欢小狗。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "我家有一只小猫，胖胖的，很可爱，女儿经常给它洗澡，特别喜欢和它在一起玩儿。"},
                {"id": 17, "type": "listening_tf", "prompt": "17. ★ 老李第一次坐船。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "我看老李的脸色不太好，一问才知道他昨天晚上没睡好觉。他说，他第一次坐船，以为和坐车没什么不同，他现在明白了，差远了。"},
                {"id": 18, "type": "listening_tf", "prompt": "18. ★ 他在黑板上画熊猫。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "把椅子上的铅笔给我，谢谢。耳朵、鼻子都画完了，现在该画这只熊猫的脚了。"},
                {"id": 19, "type": "listening_tf", "prompt": "19. ★ 他的成绩不错。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "早上，我在电子信箱里看到了我的成绩单，我的成绩比过去有了很大提高。今天一天我都很快乐。"},
                {"id": 20, "type": "listening_tf", "prompt": "20. ★ 高兴的时候不会哭。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "哭，不一定表示难过，有的人着急的时候会哭，有的人在高兴的时候也会哭。"},
                {"id": 21, "type": "listening_mc", "prompt": "21. 男的想让小王做什么？", "options": ["A 开门", "B 拿东西", "C 去超市买东西"], "answer": "A 开门", "script": "男：小王，帮我开一下门，好吗？谢谢！\n女：没问题。您去超市了？ bought 这么多东西。"},
                {"id": 22, "type": "listening_mc", "prompt": "22. 他们在谈论什么？", "options": ["A 体育", "B 历史", "C 中国文化"], "answer": "C 中国文化", "script": "女：这几本书都是关于中国文化的，很有趣。\n男：是吗？那我也借两本看看。"},
                {"id": 23, "type": "listening_mc", "prompt": "23. 女的想喝什么？", "options": ["A 茶", "B 啤酒", "C 西瓜汁"], "answer": "C 西瓜汁", "script": "男：先生，您喝点儿什么？\n女：给我一杯西瓜汁，谢谢。"},
                {"id": 24, "type": "listening_mc", "prompt": "24. 他们怎么去火车站？", "options": ["A 坐公共汽车", "B 坐地铁", "C 坐出租车"], "answer": "C 坐出租车", "script": "女：从这儿到火车站多远？\n男：有点儿远，我们坐出租车吧。"},
                {"id": 25, "type": "listening_mc", "prompt": "25. 男的在找什么？", "options": ["A 眼镜", "B 铅笔", "C 地图"], "answer": "A 眼镜", "script": "男：你看见我的眼镜了吗？\n女：在桌子上呢。"},
                {"id": 31, "type": "listening_mc", "prompt": "31. 小李现在最可能在哪儿？", "options": ["A 超市", "B 机场", "C 车站"], "answer": "A 超市", "script": "男：喂，请问小李在家吗？\n女：他出去了。他去超市买点儿东西，可能十分钟就回来了。"},
                {"id": 32, "type": "listening_mc", "prompt": "32. 现在几点了？", "options": ["A 10点", "B 差一刻10点", "C 10点一刻"], "answer": "B 差一刻10点", "script": "男：好，现在差一刻十点，我们现在去？"},
                {"id": 33, "type": "listening_mc", "prompt": "33. 女的觉得那本书怎么样？", "options": ["A 没看懂", "B 很有趣", "C 太难了"], "answer": "A 没看懂", "script": "女：还了吧，那本书我也没看懂。"},
                {"id": 34, "type": "listening_mc", "prompt": "34. 男的是做什么的？", "options": ["A 医生", "B 出租车司机", "C 老师"], "answer": "B 出租车司机", "script": "女：你好，我去世界公园。\n男：好的，没问题。"},
                {"id": 35, "type": "listening_mc", "prompt": "35. 关于女的，可以知道什么？", "options": ["A 喜欢看书", "B 是老师", "C 喜欢历史"], "answer": "A 喜欢看书", "script": "女：那是因为我看的书多，读书使人聪明。"}
            ],
            "reading": [
                {"id": 41, "type": "reading_mc", "prompt": "41. 您知道怎么去那儿吗？", "options": ["A 已经都解决了", "B 一起去踢足球", "C 冰箱里还有不少", "D 我们先坐公共汽车，然后换地铁", "E 我们是经过同事介绍认识的"], "answer": "D 我们先坐公共汽车，然后换地铁", "explanation": "H31003 第一部分 41-45 配对题"},
                {"id": 51, "type": "fill_gap", "prompt": "51. 有些事情看上去很（  ），但要做好，其实不容易。", "options": ["A 简单", "B 举行", "C 像", "D 复习", "E 声音", "F 附近"], "answer": "A 简单", "explanation": "Từ cần điền: 简单 (đơn giản)."},
                {"id": 52, "type": "fill_gap", "prompt": "52. 听张先生说，机场（  ）那个宾馆的环境不错。", "options": ["A 简单", "B 举行", "C 像", "D 复习", "E 声音", "F 附近"], "answer": "F 附近", "explanation": "Từ cần điền: 附近 (gần)."},
                {"id": 53, "type": "fill_gap", "prompt": "53. 那个会议要在我们学校（  ），所以老师们最近特别忙。", "options": ["A 简单", "B 举行", "C 像", "D 复习", "E 声音", "F 附近"], "answer": "B 举行", "explanation": "Từ cần điền: 举行 (cử hành, tổ chức)."},
                {"id": 54, "type": "fill_gap", "prompt": "54. 她和她妈妈长得真（  ）啊！", "options": ["A 简单", "B 举行", "C 像", "D 复习", "E 声音", "F 附近"], "answer": "C 像", "explanation": "Từ cần điền: 像 (giống)."},
                {"id": 55, "type": "fill_gap", "prompt": "55. 明天上午考数学，你（  ）得怎么样了？", "options": ["A 简单", "B 举行", "C 像", "D 复习", "E 声音", "F 附近"], "answer": "D 复习", "explanation": "Từ cần điền: 复习 (ôn tập)."},
                {"id": 56, "type": "fill_gap", "prompt": "56. A: 怎么样，这房子您还（  ）吧？\nB: 很不错，但我还想看看其他的。", "options": ["A 终于", "B 普通话", "C 满意", "D 爱好", "E 骑", "F 一会儿"], "answer": "C 满意", "explanation": "Từ cần điền: 满意 (hài lòng)."},
                {"id": 57, "type": "fill_gap", "prompt": "57. A: 照片上（  ）马的这个人是你爸爸？\nB: 是的，那时他刚参加工作，很年轻。", "options": ["A 终于", "B 普通话", "C 满意", "D 爱好", "E 骑", "F 一会儿"], "answer": "E 骑", "explanation": "Từ cần điền: 骑 (cưỡi, cưỡi ngựa)."},
                {"id": 58, "type": "fill_gap", "prompt": "58. A: 儿子，快起床，外面天气非常好，我们出去跑跑步。\nB: 今天是周末，您让我再睡（  ）吧。", "options": ["A 终于", "B 普通话", "C 满意", "D 爱好", "E 骑", "F 一会儿"], "answer": "F 一会儿", "explanation": "Từ cần điền: 一会儿 (một lát)."},
                {"id": 59, "type": "fill_gap", "prompt": "59. A: 他的（  ）说得真好。\nB: 当然了，你不知道？他是北京人。", "options": ["A 终于", "B 普通话", "C 满意", "D 爱好", "E 骑", "F 一会儿"], "answer": "B 普通话", "explanation": "Từ cần điền: 普通话 (tiếng Phổ thông)."},
                {"id": 60, "type": "fill_gap", "prompt": "60. A: 8 年了，她（  ）同意跟我结婚了。\nB: 真的吗？太好了！我真为你高兴！", "options": ["A 终于", "B 普通话", "C 满意", "D 爱好", "E 骑", "F 一会儿"], "answer": "A 终于", "explanation": "Từ cần điền: 终于 (cuối cùng)."},
                {"id": 61, "type": "reading_mc", "prompt": "61. 到了机场，他发现护照不见了，在行李箱里找了半天，也没找到，很着急。\n★ 他为什么着急？", "options": ["A 迟到了", "B 忘记拿机票了", "C 找不到护照了"], "answer": "C 找不到护照了", "explanation": "Bất an vì không tìm thấy hộ chiếu."},
                {"id": 62, "type": "reading_mc", "prompt": "62. 人们经常说：“面包会有的，牛奶也会有的。”是的，如果努力，什么都会有的。\n★ 这句话主要想告诉我们：", "options": ["A 要相信别人", "B 兴趣最重要", "C 努力才有希望"], "answer": "C 努力才有希望", "explanation": "Ý chính: Nỗ lực mới có hy vọng."},
                {"id": 63, "type": "reading_mc", "prompt": "63. 上个星期和朋友们去游泳，把我累坏了，到现在我的腿还在疼。看来我是应该多锻炼锻炼了。\n★ 他打算：", "options": ["A 去医院", "B 锻炼身体", "C 下午去游泳"], "answer": "B 锻炼身体", "explanation": "打算多锻炼锻炼."},
                {"id": 64, "type": "reading_mc", "prompt": "64. 越高的地方越冷，山路也越难走。但是不用担心，有我呢，我去年秋天爬过这个山...\n★ 根据这段话，可以知道什么？", "options": ["A 他害怕爬山", "B 应该夏天去爬山", "C 他爬过这个山"], "answer": "C 他爬过这个山", "explanation": "Nêu rõ: 我去年秋天爬过这个山."},
                {"id": 65, "type": "reading_mc", "prompt": "65. 小黄，明天上午我有个会，你帮我去机场接李先生吧...\n★ 小黄明天最可能：", "options": ["A 去旅游", "B 去机场接人", "C 要照顾病人"], "answer": "B 去机场接人", "explanation": "Nhờ đi airport đón khách."}
            ],
            "writing": [
                {"id": 71, "type": "reorder", "prompt": "71. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc khớp 100% cả dấu câu):", "words": ["把", "手机", "送给", "她", "决定", "弟弟", "。"], "correct": "她决定把手机送给弟弟。", "hint": "Chủ ngữ 她 + 决定 + 把..."},
                {"id": 72, "type": "reorder", "prompt": "72. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc khớp 100% cả dấu câu):", "words": ["这个学生", "我和", "很久", "没见面了", "。"], "correct": "我和这个学生很久没见面了。", "hint": "我和这个学生 + 很久 + 没见面了。"},
                {"id": 73, "type": "reorder", "prompt": "73. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc khớp 100% cả dấu câu):", "words": ["经常", "刮风", "这个城市的", "春天", "。"], "correct": "这个城市的春天经常刮风。", "hint": "Chủ ngữ 这个城市的春天 + 经常刮风。"},
                {"id": 74, "type": "reorder", "prompt": "74. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc khớp 100% cả dấu câu):", "words": ["他的", "写得", "汉字", "很漂亮", "。"], "correct": "他的汉字写得很漂亮。", "hint": "他的汉字 + 写得很漂亮。"},
                {"id": 75, "type": "reorder", "prompt": "75. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc khớp 100% cả dấu câu):", "words": ["叔叔的", "太阳镜", "花了", "900块钱", "。"], "correct": "叔叔的太阳镜花了900块钱。", "hint": "叔叔的太阳镜 + 花了900块钱。"},
                {"id": 76, "type": "char_fill", "prompt": "76. Điền chữ Hán chính xác cho phiên âm (yuè): 八（ yuè ）十五的月亮真圆。", "correct": "月", "hint": "月 (yuè) - 月亮"},
                {"id": 77, "type": "char_fill", "prompt": "77. Điền chữ Hán chính xác cho phiên âm (bái): 那只小猫是（ bái ）色的。", "correct": "白", "hint": "白 (bái) - 白色"},
                {"id": 78, "type": "char_fill", "prompt": "78. Điền chữ Hán chính xác cho phiên âm (qiān): 一（ qiān ）万年前，动物们出现了吗？", "correct": "千", "hint": "千 (qiān) - 一千万"},
                {"id": 79, "type": "char_fill", "prompt": "79. Điền chữ Hán chính xác cho phiên âm (xīn): 外面下雪了，路上小（ xīn ）点儿。", "correct": "心", "hint": "心 (xīn) - 小心"},
                {"id": 80, "type": "char_fill", "prompt": "80. Điền chữ Hán chính xác cho phiên âm (yīn): 生病了要注意休息，（ yīn ）为健康最重要。", "correct": "因", "hint": "因 (yīn) - 因为"}
            ]
        },
        "H31006": {
            "title": "Mã đề H31006",
            "audio_file": "H31006.mp3",
            "listening": [
                {"id": 1, "type": "listening_mc", "prompt": "1. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "A", "script": "1．A"},
                {"id": 2, "type": "listening_mc", "prompt": "2. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "E", "script": "2．E"},
                {"id": 3, "type": "listening_mc", "prompt": "3. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "C", "script": "3．C"},
                {"id": 4, "type": "listening_mc", "prompt": "4. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "F", "script": "4．F"},
                {"id": 5, "type": "listening_mc", "prompt": "5. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "B", "script": "5．B"},
                {"id": 11, "type": "listening_tf", "prompt": "11. ★ 运动会还没举行。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "11．×"},
                {"id": 12, "type": "listening_tf", "prompt": "12. ★ 爸爸去上班了。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "12．√"},
                {"id": 13, "type": "listening_tf", "prompt": "13. ★ 他在眼镜店里。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "13．×"},
                {"id": 14, "type": "listening_tf", "prompt": "14. ★ 关心朋友的办法很多。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "14．×"},
                {"id": 15, "type": "listening_tf", "prompt": "15. ★ 她越来越漂亮了。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "15．×"},
                {"id": 16, "type": "listening_tf", "prompt": "16. ★ 他在眼镜店里。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "这家眼镜店的服务很好，我的眼镜就是在他们家买的。"},
                {"id": 17, "type": "listening_tf", "prompt": "17. ★ 校长的猫喜欢在椅子上睡觉。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "17．√"},
                {"id": 18, "type": "listening_tf", "prompt": "18. ★ 他是老师。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "18．×"},
                {"id": 19, "type": "listening_tf", "prompt": "19. ★ 她在洗手间呢。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "19．√"},
                {"id": 20, "type": "listening_tf", "prompt": "20. ★ 他们要去拿照片。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "20．√"}
            ],
            "reading": [
                {"id": 51, "type": "fill_gap", "prompt": "51. 这个城市已经有 900 多年的历史了，非常（  ）。", "options": ["A 有名", "B 变化", "C 季节", "D 只", "E 声音", "F 瘦"], "answer": "A 有名", "explanation": "Có lịch sử hơn 900 năm nên rất 有名."},
                {"id": 52, "type": "fill_gap", "prompt": "52. 因为工作比较忙，小李最近（  ）了很多。", "options": ["A 有名", "B 变化", "C 季节", "D 只", "E 声音", "F 瘦"], "answer": "F 瘦", "explanation": "最近 瘦 了很多 (gầy đi nhiều)."},
                {"id": 53, "type": "fill_gap", "prompt": "53. 春、夏、秋、冬，你最喜欢哪个（  ）？", "options": ["A 有名", "B 变化", "C 季节", "D 只", "E 声音", "F 瘦"], "answer": "C 季节", "explanation": "Mùa (季节)."},
                {"id": 54, "type": "fill_gap", "prompt": "54. 你阿姨的（  ）真大，我几乎没认出她来。", "options": ["A 有名", "B 变化", "C 季节", "D 只", "E 声音", "F 瘦"], "answer": "B 变化", "explanation": "Sự thay đổi (变化) rất lớn."},
                {"id": 55, "type": "fill_gap", "prompt": "55. 从我们学校坐公共汽车去火车站，（  ）需要 10 分钟。", "options": ["A 有名", "B 变化", "C 季节", "D 只", "E 声音", "F 瘦"], "answer": "D 只", "explanation": "Chỉ cần (只需要)."},
                {"id": 56, "type": "fill_gap", "prompt": "56. A: 音乐会的门票我放在桌子上了，（  ）4 张。\nB: 我看见了，谢谢你。", "options": ["A 刷牙", "B 太阳", "C 一共", "D 爱好", "E 借", "F 新鲜"], "answer": "C 一共", "explanation": "Tổng cộng (一共) 4 tấm."},
                {"id": 57, "type": "fill_gap", "prompt": "57. A:（  ）以后不能再吃东西了。\nB: 妈，您说第 1001 次了。", "options": ["A 刷牙", "B 太阳", "C 一共", "D 爱好", "E 借", "F 新鲜"], "answer": "A 刷牙", "explanation": "Đánh răng (刷牙) xong."},
                {"id": 58, "type": "fill_gap", "prompt": "58. A: 小姐，葡萄多少钱一斤？\nB: 3 块。今天的葡萄很（  ），也很甜。", "options": ["A 刷牙", "B 太阳", "C 一共", "D 爱好", "E 借", "F 新鲜"], "answer": "F 新鲜", "explanation": "Tươi ngon (新鲜)."},
                {"id": 59, "type": "fill_gap", "prompt": "59. A: 喂，上次（  ）的那本书，晚几天还你可以吗？\nB: 没问题，我现在在外地，回去再说。", "options": ["A 刷牙", "B 太阳", "C 一共", "D 爱好", "E 借", "F 新鲜"], "answer": "E 借", "explanation": "Mượn (借) cuốn sách."},
                {"id": 60, "type": "fill_gap", "prompt": "60. A: 天终于晴了，好久没看见（  ）了。\nB: 天气这么好，我们去河边走走？", "options": ["A 刷牙", "B 太阳", "C 一共", "D 爱好", "E 借", "F 新鲜"], "answer": "B 太阳", "explanation": "Mặt trời (太阳)."},
                {"id": 61, "type": "reading_mc", "prompt": "61. 站得高，才能看得远。所以，人们对自己的要求高一些，了解的事情就会更多一些。\n★ 想要了解更多，我们需要：", "options": ["A 换新的环境", "B 多帮助别人", "C 提高对自己的要求"], "answer": "C 提高对自己的要求", "explanation": "Nâng cao yêu cầu bản thân."},
                {"id": 62, "type": "reading_mc", "prompt": "62. 熊猫的耳朵、眼睛、鼻子是黑色的...\n★ 根据这段话，熊猫：", "options": ["A 爱照相", "B 很聪明", "C 有个黑鼻子"], "answer": "C 有个黑鼻子", "explanation": "Có cái mũi màu đen."},
                {"id": 63, "type": "reading_mc", "prompt": "63. 老师问小明：“北京和月亮，哪个离你更近？”...\n★ 小明为什么认为月亮离他近？", "options": ["A 月亮很大", "B 容易看到月亮", "C 他没去过北京"], "answer": "B 容易看到月亮", "explanation": "Dễ dàng nhìn thấy mặt trăng."},
                {"id": 64, "type": "reading_mc", "prompt": "64. 他刚才给我打电话，说那本书里还有一个问题...\n★ 那本书：", "options": ["A 作用不大", "B 有不少错字", "C 被发现还有问题"], "answer": "C 被发现还有问题", "explanation": "Phát hiện có vấn đề."},
                {"id": 65, "type": "reading_mc", "prompt": "65. 小黄，明天上午我有个会，你帮我去机场接李先生吧...\n★ 小黄明天最可能：", "options": ["A 去旅游", "B 去机场接人", "C 要照顾病人"], "answer": "B 去机场接人", "explanation": "Đi sân bay đón người."}
            ],
            "writing": [
                {"id": 71, "type": "reorder", "prompt": "71. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc khớp 100% cả dấu câu):", "words": ["咖啡里", "放糖", "不要", "。"], "correct": "咖啡里不要放糖。", "hint": "咖啡里 + 不要放糖。"},
                {"id": 72, "type": "reorder", "prompt": "72. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc khớp 100% cả dấu câu):", "words": ["干净了", "把", "碗和筷子", "洗", "吗", "？"], "correct": "把碗和筷子洗干净了吗？", "hint": "把碗和筷子 + 洗干净了吗？"},
                {"id": 73, "type": "reorder", "prompt": "73. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc khớp 100% cả dấu câu):", "words": ["孩子", "了", "突然", "发烧", "。"], "correct": "孩子突然发烧了。", "hint": "孩子 + 突然 + 发烧了。"},
                {"id": 74, "type": "reorder", "prompt": "74. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc khớp 100% cả dấu câu):", "words": ["这个句子", "游戏结束", "表示", "看到", "。"], "correct": "看到这个句子表示游戏结束。", "hint": "看到这个句子 + 表示 + 游戏结束。"},
                {"id": 75, "type": "reorder", "prompt": "75. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc khớp 100% cả dấu câu):", "words": ["她", "很", "这条绿裤子", "对", "满意", "。"], "correct": "她对这条绿裤子很满意。", "hint": "她 + 对这条绿裤子 + 很满意。"},
                {"id": 76, "type": "char_fill", "prompt": "76. Điền chữ Hán chính xác cho phiên âm (yě): 相信我，面包会有的，牛奶（ yě ）会有的。", "correct": "也", "hint": "也 (yě)"},
                {"id": 77, "type": "char_fill", "prompt": "77. Điền chữ Hán chính xác cho phiên âm (rì): 每个国家都有自己的节（ rì ）、自己的文化。", "correct": "日", "hint": "日 (rì) - 节日"},
                {"id": 78, "type": "char_fill", "prompt": "78. Điền chữ Hán chính xác cho phiên âm (zài): 请用铅笔把姓名写（ zài ）照片后面。", "correct": "在", "hint": "在 (zài) - 写在"},
                {"id": 79, "type": "char_fill", "prompt": "79. Điền chữ Hán chính xác cho phiên âm (duō): 第二，必须（ duō ）练习。", "correct": "多", "hint": "多 (duō) - 多练习"},
                {"id": 80, "type": "char_fill", "prompt": "80. Điền chữ Hán chính xác cho phiên âm (wèi): 我想请您（ wèi ）我写介绍信。", "correct": "为", "hint": "为 (wèi) - 为我写"}
            ]
        },
        "H31008": {
            "title": "Mã đề H31008",
            "audio_file": "H31008.mp3",
            "listening": [
                {"id": 1, "type": "listening_mc", "prompt": "1. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "A", "script": "1．A"},
                {"id": 2, "type": "listening_mc", "prompt": "2. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "B", "script": "2．B"},
                {"id": 3, "type": "listening_mc", "prompt": "3. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "F", "script": "3．F"},
                {"id": 4, "type": "listening_mc", "prompt": "4. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "C", "script": "4．C"},
                {"id": 5, "type": "listening_mc", "prompt": "5. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "E", "script": "5．E"},
                {"id": 11, "type": "listening_tf", "prompt": "11. ★ 他们现在在电梯里。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "11．×"},
                {"id": 12, "type": "listening_tf", "prompt": "12. ★ 今天的月亮很大。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "12．×"},
                {"id": 13, "type": "listening_tf", "prompt": "13. ★ 小鸡会游泳。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "13．√"},
                {"id": 14, "type": "listening_tf", "prompt": "14. ★ 小王的丈夫爱看篮球比赛。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "14．×"},
                {"id": 15, "type": "listening_tf", "prompt": "15. ★ 努力的人机会多。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "只要你努力，机会总是有的。"},
                {"id": 16, "type": "listening_tf", "prompt": "16. ★ 葡萄不好吃。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "16．×"},
                {"id": 17, "type": "listening_tf", "prompt": "17. ★ 老刘喝酒容易脸红。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "17．√"},
                {"id": 18, "type": "listening_tf", "prompt": "18. ★ 他病了。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "18．√"},
                {"id": 19, "type": "listening_tf", "prompt": "19. ★ 她去超市了。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "19．×"},
                {"id": 20, "type": "listening_tf", "prompt": "20. ★ 他们买到了火车票。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "20．√"}
            ],
            "reading": [
                {"id": 51, "type": "fill_gap", "prompt": "51. 这个城市有几百年的（  ）了。", "options": ["A 聪明", "B 几乎", "C 解决", "D 历史", "E 声音", "F 关系"], "answer": "D 历史", "explanation": "Lịch sử (历史) vài trăm năm."},
                {"id": 52, "type": "fill_gap", "prompt": "52. 儿子长大了，都快一米八了，（  ）和他爸爸一样高了。", "options": ["A 聪明", "B 几乎", "C 解决", "D 历史", "E 声音", "F 关系"], "answer": "B 几乎", "explanation": "Hầu như (几乎) cao bằng bố."},
                {"id": 53, "type": "fill_gap", "prompt": "53. 小黄是我的好朋友，她和我的（  ）一直很好。", "options": ["A 聪明", "B 几乎", "C 解决", "D 历史", "E 声音", "F 关系"], "answer": "F 关系", "explanation": "Mối quan hệ (关系) rất tốt."},
                {"id": 54, "type": "fill_gap", "prompt": "54. 多吃鱼会使人变得更（  ）。", "options": ["A 聪明", "B 几乎", "C 解决", "D 历史", "E 声音", "F 关系"], "answer": "A 聪明", "explanation": "Thông minh (聪明)."},
                {"id": 55, "type": "fill_gap", "prompt": "55. 我们已经找到（  ）问题的办法了。", "options": ["A 聪明", "B 几乎", "C 解决", "D 历史", "E 声音", "F 关系"], "answer": "C 解决", "explanation": "Giải quyết (解决) vấn đề."},
                {"id": 56, "type": "fill_gap", "prompt": "56. A: 你（  ）的这是猫？\nB: 大熊猫！它在爬树。这也看不懂？", "options": ["A 画", "B 简单", "C 选择", "D 爱好", "E 结婚", "F 马上"], "answer": "A 画", "explanation": "Vẽ (画)."},
                {"id": 57, "type": "fill_gap", "prompt": "57. A: 你低着头想什么呢？\nB: 是工作还是读书，我不知道应该怎么（  ）才好。", "options": ["A 画", "B 简单", "C 选择", "D 爱好", "E 结婚", "F 马上"], "answer": "C 选择", "explanation": "Lựa chọn (选择)."},
                {"id": 58, "type": "fill_gap", "prompt": "58. A: 你渴不？我想去买点儿水。\nB: 那你快一点儿，表演（  ）就要开始了。", "options": ["A 画", "B 简单", "C 选择", "D 爱好", "E 结婚", "F 马上"], "answer": "F 马上", "explanation": "Lập tức, ngay (马上)."},
                {"id": 59, "type": "fill_gap", "prompt": "59. A: 相信我，这件事对公司不会有影响的。\nB: 夏经理，你把事情想得太（  ）了。", "options": ["A 画", "B 简单", "C 选择", "D 爱好", "E 结婚", "F 马上"], "answer": "B 简单", "explanation": "Đơn giản (简单)."},
                {"id": 60, "type": "fill_gap", "prompt": "60. A: 好久没看见白老师了，他不在这儿住了？\nB: 是，他（  ）以后就和妻子搬到学校去住了。", "options": ["A 画", "B 简单", "C 选择", "D 爱好", "E 结婚", "F 马上"], "answer": "E 结婚", "explanation": "Kết hôn (结婚)."},
                {"id": 61, "type": "reading_mc", "prompt": "61. 最近几年，这里的变化很大，车辆更多了，街道更干净了，天更蓝了...\n★ 这里最近几年怎么样？", "options": ["A 环境变好了", "B 和过去相同", "C 变得更差了"], "answer": "A 环境变好了", "explanation": "Môi trường biến tốt hơn."},
                {"id": 62, "type": "reading_mc", "prompt": "62. 人们根据季节的变化来决定喝什么茶...\n★ 这段话告诉我们：", "options": ["A 茶有什么作用", "B 老人爱喝红茶", "C 不同季节喝不同的茶"], "answer": "C 不同季节喝不同的茶", "explanation": "Mỗi mùa uống trà khác nhau."},
                {"id": 63, "type": "reading_mc", "prompt": "63. 汉字有多少个？...但人们常用的也就两千多个...\n★ 这段话的主要意思是：", "options": ["A 汉字很难写", "B 要学会查字典", "C 常用汉字不多"], "answer": "C 常用汉字不多", "explanation": "Chữ Hán thông dụng không nhiều."},
                {"id": 64, "type": "reading_mc", "prompt": "64. 为什么很多人愿意在网上买东西呢？...\n★ 在网上买东西：", "options": ["A 比较贵", "B 花钱少", "C 花的时间多"], "answer": "B 花钱少", "explanation": "Mua hàng online tiết kiệm tiền hơn."},
                {"id": 65, "type": "reading_mc", "prompt": "65. 儿子的作业总是做错，但昨天的一个也没错...\n★ 儿子昨天的作业 festival 无错的原因：", "options": ["A 自己做的", "B 爸爸帮忙了", "C 认真复习了"], "answer": "A 自己做的", "explanation": "Tự làm (自己做的)."}
            ],
            "writing": [
                {"id": 71, "type": "reorder", "prompt": "71. Sắp xếp câu chính xác (Khớp 100% cả dấu câu):", "words": ["那位", "邻居", "很热情", "。"], "correct": "那位邻居很热情。", "hint": "那位邻居 + 很热情。"},
                {"id": 72, "type": "reorder", "prompt": "72. Sắp xếp câu chính xác (Khớp 100% cả dấu câu):", "words": ["这个楼", "一共", "三层", "。"], "correct": "这个楼一共三层。", "hint": "这个楼 + 一共三层。"},
                {"id": 73, "type": "reorder", "prompt": "73. Sắp xếp câu chính xác (Khớp 100% cả dấu câu):", "words": ["菜单", "被", "服务员", "拿走了", "。"], "correct": "菜单被服务员拿走了。", "hint": "菜单 + 被服务员 + 拿走了。"},
                {"id": 74, "type": "reorder", "prompt": "74. Sắp xếp câu chính xác (Khớp 100% cả dấu câu):", "words": ["中国南方的雨水", "比", "北方", "多", "。"], "correct": "中国南方的雨水比北方多。", "hint": "中国南方的雨水 + 比北方多。"},
                {"id": 75, "type": "reorder", "prompt": "75. Sắp xếp câu chính xác (Khớp 100% cả dấu câu):", "words": ["把", "冰箱", "放", "厨房里", "吧", "。"], "correct": "把冰箱放厨房里吧。", "hint": "把冰箱 + 放厨房里吧。"},
                {"id": 76, "type": "char_fill", "prompt": "76. Điền chữ Hán chính xác cho phiên âm (jǐ): 你姐姐的孩子上（ jǐ ）年级？", "correct": "几", "hint": "几 (jǐ)"},
                {"id": 77, "type": "char_fill", "prompt": "77. Điền chữ Hán chính xác cho phiên âm (xīn): 马小姐，谢谢关（ xīn ），我不发烧了。", "correct": "心", "hint": "心 (xīn) - 关心"},
                {"id": 78, "type": "char_fill", "prompt": "78. Điền chữ Hán chính xác cho phiên âm (xià): 对不起，（ xià ）午有个重要的会议。", "correct": "下", "hint": "下 (xià) - 下午"},
                {"id": 79, "type": "char_fill", "prompt": "79. Điền chữ Hán chính xác cho phiên âm (dà): 叔叔的普通话水平有了很（ dà ）提高。", "correct": "大", "hint": "大 (dà) - 很大"},
                {"id": 80, "type": "char_fill", "prompt": "80. Điền chữ Hán chính xác cho phiên âm (yún): 这个小太阳表示晴天，（ yún ）表示阴天。", "correct": "云", "hint": "云 (yún) - 云彩"}
            ]
        },
        "H31111": {
            "title": "Mã đề H31111",
            "audio_file": "H31111.mp3",
            "listening": [
                {"id": 1, "type": "listening_mc", "prompt": "1. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "F", "script": "1．F"},
                {"id": 2, "type": "listening_mc", "prompt": "2. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "B", "script": "2．B"},
                {"id": 3, "type": "listening_mc", "prompt": "3. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "A", "script": "3．A"},
                {"id": 4, "type": "listening_mc", "prompt": "4. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "E", "script": "4．E"},
                {"id": 5, "type": "listening_mc", "prompt": "5. 听力第一部分（1-5题）", "options": ["A", "B", "C", "D", "E", "F"], "answer": "C", "script": "5．C"},
                {"id": 11, "type": "listening_tf", "prompt": "11. ★ 校长还认识他。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "没想到过了这么多年，校长依然能叫出他的名字。"},
                {"id": 12, "type": "listening_tf", "prompt": "12. ★ 现在的书比以前的贵。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "12．√"},
                {"id": 13, "type": "listening_tf", "prompt": "13. ★ 他对这个运动没有兴趣。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "13．×"},
                {"id": 14, "type": "listening_tf", "prompt": "14. ★ 他们在想办法。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "14．×"},
                {"id": 15, "type": "listening_tf", "prompt": "15. ★ 那个学生想参加比赛。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "15．√"},
                {"id": 16, "type": "listening_tf", "prompt": "16. ★ 他忘了同学的生日。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "16．×"},
                {"id": 17, "type": "listening_tf", "prompt": "17. ★ 黄经理很着急。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "17．√"},
                {"id": 18, "type": "listening_tf", "prompt": "18. ★ 那位司机没什么爱好。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "18．×"},
                {"id": 19, "type": "listening_tf", "prompt": "19. ★ 小晴正在画画儿。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "19．√"},
                {"id": 20, "type": "listening_tf", "prompt": "20. ★ 那条狗走在他前面。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "20．×"}
            ],
            "reading": [
                {"id": 51, "type": "fill_gap", "prompt": "51. 北方人爱吃（  ），南方人喜欢吃米饭。", "options": ["A 终于", "B 水平", "C 面条儿", "D 结婚", "E 声音", "F 了解"], "answer": "C 面条儿", "explanation": "Mì (面条儿)."},
                {"id": 52, "type": "fill_gap", "prompt": "52. 坐了 7 个小时的火车，我们（  ）到北京了。", "options": ["A 终于", "B 水平", "C 面条儿", "D 结婚", "E 声音", "F 了解"], "answer": "A 终于", "explanation": "Rốt cuộc, cuối cùng (终于)."},
                {"id": 53, "type": "fill_gap", "prompt": "53. 他们准备 8 月（  ）。", "options": ["A 终于", "B 水平", "C 面条儿", "D 结婚", "E 声音", "F 了解"], "answer": "D 结婚", "explanation": "Kết hôn (结婚)."},
                {"id": 54, "type": "fill_gap", "prompt": "54. 看了好几个节目，我觉得三年级二班的（  ）最高。", "options": ["A 终于", "B 水平", "C 面条儿", "D 结婚", "E 声音", "F 了解"], "answer": "B 水平", "explanation": "Trình độ (水平)."},
                {"id": 55, "type": "fill_gap", "prompt": "55. 你应该先（  ）事情的经过，然后再想怎么解决问题。", "options": ["A 终于", "B 水平", "C 面条儿", "D 结婚", "E 声音", "F 了解"], "answer": "F 了解", "explanation": "Tìm hiểu, hiểu rõ (了解)."},
                {"id": 56, "type": "fill_gap", "prompt": "56. A: 我到你们公司楼下了，你在几（  ）？\nB: 你等一下，我下来接你。", "options": ["A 结束", "B 方便", "C 层", "D 爱好", "E 当然", "F 一直"], "answer": "C 层", "explanation": "Tầng (层)."},
                {"id": 57, "type": "fill_gap", "prompt": "57. A: 船票我买到了，记得来送我。\nB: 等表演一（  ）我就去找你。", "options": ["A 结束", "B 方便", "C 层", "D 爱好", "E 当然", "F 一直"], "answer": "A 结束", "explanation": "Kết thúc (结束)."},
                {"id": 58, "type": "fill_gap", "prompt": "58. A: 我周末想去动物园，你知道怎么去吗？\nB: 坐 405 路就能到。骑自行车去可能更（  ）。", "options": ["A 结束", "B 方便", "C 层", "D 爱好", "E 当然", "F 一直"], "answer": "B 方便", "explanation": "Thuận tiện (方便)."},
                {"id": 59, "type": "fill_gap", "prompt": "59. A: 火车站附近有宾馆吗？\nB:（  ）有，我第一次来的时候就住前面那个宾馆。", "options": ["A 结束", "B 方便", "C 层", "D 爱好", "E 当然", "F 一直"], "answer": "E 当然", "explanation": "Dĩ nhiên (当然)."},
                {"id": 60, "type": "fill_gap", "prompt": "60. A: 小马，你好久没来打篮球了。\nB: 最近（  ）忙着找工作，没时间玩儿。", "options": ["A 结束", "B 方便", "C 层", "D 爱好", "E 当然", "F 一直"], "answer": "F 一直", "explanation": "Liên tục, luôn (一直)."},
                {"id": 61, "type": "reading_mc", "prompt": "61. 昨天，我送给妻子一个礼物，是一辆红色的汽车，她高兴极了。\n★ 妻子为什么很高兴？", "options": ["A 搬新家了", "B 换了辆新车", "C 把旧车卖了"], "answer": "B 换了辆新车", "explanation": "Được đổi xe ô tô mới."},
                {"id": 62, "type": "reading_mc", "prompt": "62. 那个饭馆儿虽然不大， लेकिन 菜做得很好吃，而且不贵...\n★ 根据这段话，那家饭馆儿：", "options": ["A 菜便宜", "B 很安静", "C 客人少"], "answer": "A 菜便宜", "explanation": "Món ăn rẻ."},
                {"id": 63, "type": "reading_mc", "prompt": "63. 为了变得瘦一些，妹妹决定每天早上去跑步...\n★ 根据这段话，妹妹 breath：", "options": ["A 变黑了", "B 不胖了", "C 天天跑步"], "answer": "C 天天跑步", "explanation": "Hàng ngày chạy bộ."},
                {"id": 64, "type": "reading_mc", "prompt": "64. 她看那个电影的时候哭了，因为电影里的故事...\n★ 关于这个电影，可以知道什么？", "options": ["A 很有名", "B 让她很难过", "C 没什么意思"], "answer": "B 让她很难过", "explanation": "Khiến cô ấy rất cảm động/buồn."},
                {"id": 65, "type": "reading_mc", "prompt": "65. 小云，我给你介绍个男朋友吧？...\n★ 她想为小云：", "options": ["A 办护照", "B 介绍工作", "C 介绍男朋友"], "answer": "C 介绍男朋友", "explanation": "Giới thiệu bạn trai."}
            ],
            "writing": [
                {"id": 71, "type": "reorder", "prompt": "71. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc đúng dấu câu):", "words": ["左阿姨", "讲", "普通话", "不会", "。"], "correct": "左阿姨不会讲普通话。", "hint": "左阿姨 + 不会讲 + 普通话。"},
                {"id": 72, "type": "reorder", "prompt": "72. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc đúng dấu câu):", "words": ["面包", "18块", " these ", "一共", "。"], "correct": "这些面包一共18块。", "hint": "这些面包 + 一共18块。"},
                {"id": 73, "type": "reorder", "prompt": "73. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc đúng dấu câu):", "words": ["完成", "了", "你的作业", "吗", "？"], "correct": "完成了你的作业吗？", "hint": "Cuối câu dùng dấu hỏi ？"},
                {"id": 74, "type": "reorder", "prompt": "74. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc đúng dấu câu):", "words": ["成绩", "我女儿的", "非常好", "数学", "。"], "correct": "我女儿的数学成绩非常好。", "hint": "我女儿的数学成绩 + 非常好。"},
                {"id": 75, "type": "reorder", "prompt": "75. Sắp xếp từ thành câu hoàn chỉnh (Bắt buộc đúng dấu câu):", "words": ["她", "放进了", "叔叔的包里", "把", "信", "。"], "correct": "她把信放进了叔叔的包里。", "hint": "她 + 把信 + 放进了叔叔的包里。"},
                {"id": 76, "type": "char_fill", "prompt": "76. Điền chữ Hán chính xác cho phiên âm (xià): 再见，欢迎您（ xià ）次再来。", "correct": "下", "hint": "下 (xià) - 下次"},
                {"id": 77, "type": "char_fill", "prompt": "77. Điền chữ Hán chính xác cho phiên âm (huí): 男朋友的（ huí ）答，让她特别高兴。", "correct": "回", "hint": "回 (huí) - 回答"},
                {"id": 78, "type": "char_fill", "prompt": "78. Điền chữ Hán chính xác cho phiên âm (bǐ): 对猫来说，小鱼（ bǐ ）羊肉更好吃。", "correct": "比", "hint": "比 (bǐ)"},
                {"id": 79, "type": "char_fill", "prompt": "79. Điền chữ Hán chính xác cho phiên âm (tài): 你把空调打开吧，房间里（ tài ）热了。", "correct": "太", "hint": "太 (tài) - 太热了"},
                {"id": 80, "type": "char_fill", "prompt": "80. Điền chữ Hán chính xác cho phiên âm (tiān): 今天是晴（ tiān ）。", "correct": "天", "hint": "天 (tiān) - 晴天"}
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
    st.markdown("<h1 style='text-align: center; color: #1A365D;'>🎓 LUYỆN ĐỀ HSK3</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #4A5568;'>Vui lòng nhập thông tin và chọn Mã Đề Thi để bắt đầu</p>", unsafe_allow_html=True)
    st.write("---")

    # Nhập thông tin thí sinh
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.session_state.student_name = st.text_input("👤 Họ và tên học viên:", value=st.session_state.student_name, placeholder="Ví dụ: Nguyễn Văn A")
    with col_info2:
        st.session_state.class_name = st.text_input("🏫 Tên lớp:", value=st.session_state.class_name, placeholder="Ví dụ: Lớp HSK3-K24")

    st.write("")
    st.markdown("### 📋 Chọn Mã Đề Thi:")

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
            <div style="background-color: {p_bg}; border: 2.5px solid {p_border}; border-radius: 12px; padding: 25px 15px; text-align: center; margin-bottom: 12px;">
                <div style="font-size: 26px; font-weight: bold; color: {p_border}; font-family: 'Tahoma', sans-serif;">{code}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"👉 Vào làm đề {code}", key=f"btn_{code}", use_container_width=True):
                if not st.session_state.student_name.strip():
                    st.error("⚠️ Vui lòng nhập Họ và Tên trước khi vào thi!")
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

    # Header trang thi
    col_head1, col_head2 = st.columns([3, 1])
    with col_head1:
        st.markdown(f"## 📝 LUYỆN ĐỀ HSK3: <span style='color:#1A365D;'>{exam_code}</span>", unsafe_allow_html=True)
        st.markdown(f"**Học viên:** `{st.session_state.student_name}` | **Lớp:** `{st.session_state.class_name}`")
    with col_head2:
        if st.button("⬅️ Trở về chọn đề khác"):
            st.session_state.selected_exam = None
            st.rerun()

    st.write("---")

    # Quy định thời gian thi (giây)
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
# 7. HÀM HIỂN THỊ CHI TIẾT TỪNG PHẦN THI
# ==========================================
def render_section_tab(exam_code, section_key, section_title, questions, max_time_sec, audio_file=None):
    st.subheader(f"📌 {section_title}")

    section_id = f"{exam_code}_{section_key}"
    is_submitted = st.session_state.submitted_sections.get(section_id, False)

    start_time = st.session_state.exam_start_times[exam_code][section_key]
    elapsed = time.time() - start_time
    remaining_sec = max(0, int(max_time_sec - elapsed))

    # ĐỒNG HỒ ĐẾM NGƯỢC ĐỘNG BẰNG JAVASCRIPT
    if not is_submitted:
        st.components.v1.html(f"""
        <div id="timer_{section_key}" style="
            background-color: #FFF5F5;
            border: 2px solid #E53E3E;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 20px;
            font-weight: bold;
            color: #C53030;
            text-align: center;
            font-family: 'Tahoma', sans-serif;
            margin-bottom: 10px;
        ">⏱️ Thời gian còn lại: <span id="time_str_{section_key}">--:--</span></div>

        <script>
            var seconds = {remaining_sec};
            function updateTimer() {{
                var mins = Math.floor(seconds / 60);
                var secs = seconds % 60;
                var displayMins = mins < 10 ? "0" + mins : mins;
                var displaySecs = secs < 10 ? "0" + secs : secs;
                var timerElem = document.getElementById("timer_{section_key}");
                var strElem = document.getElementById("time_str_{section_key}");
                
                if (strElem) {{
                    strElem.innerHTML = displayMins + ":" + displaySecs;
                }}
                
                if (seconds <= 300 && seconds > 0) {{
                    timerElem.style.backgroundColor = "#FED7D7";
                    timerElem.style.borderColor = "#E53E3E";
                    timerElem.innerHTML = "⚠️ SẮP HẾT GIỜ! ⏱️ Thời gian còn lại: " + displayMins + ":" + displaySecs;
                }}
                
                if (seconds <= 0) {{
                    timerElem.innerHTML = "🚨 ĐÃ HẾT GIỜ LÀM BÀI!";
                }} else {{
                    seconds--;
                }}
            }}
            updateTimer();
            setInterval(updateTimer, 1000);
        </script>
        """, height=65)

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
    else:
        correct_count = sum([
            1 for q in questions if (
                (st.session_state.user_answers.get(f"{answers_key_prefix}_{q['id']}", "").strip() == q['correct'].strip())
                if q["type"] in ["reorder", "char_fill"]
                else (st.session_state.user_answers.get(f"{answers_key_prefix}_{q['id']}", "") == q['answer'])
            )
        ])
        
        # BANNER HIỂN THỊ DÒNG THÔNG BÁO HOÀN THÀNH
        sec_name_vn = "Nghe" if section_key == "listening" else ("Đọc" if section_key == "reading" else "Viết")
        st.markdown(f"""
        <div class="completion-banner">
            <h3 style="color: #2B6CB0; margin-bottom: 8px;">🎉 Chúc mừng "{st.session_state.student_name}" đã hoàn thành đề "{exam_code}" (Phần {sec_name_vn})</h3>
            <p style="font-size: 20px; font-weight: bold; color: #2D3748; margin: 0;">
                Điểm số của bạn là: <span style="color: #38A169;">{correct_count}/{len(questions)}</span> câu đúng ({int(correct_count/len(questions)*100)}%)
            </p>
        </div>
        """, unsafe_allow_html=True)


def main():
    if st.session_state.selected_exam is None:
        render_landing_page()
    else:
        render_exam_page(st.session_state.selected_exam)

if __name__ == "__main__":
    main()
