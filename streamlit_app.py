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

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tahoma&display=swap');
    
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    .stAppHeader {display: none !important;}

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
# 2. DỮ LIỆU ĐỀ THI HSK3 chuẩn xác (H31003 & H31008)
# ==========================================
@st.cache_data
def load_exam_data():
    # --- ĐỀ H31003 ---
    listening_31003 = [
        {'id': 11, 'type': 'listening_tf', 'prompt': '★ 冬天水果很便宜。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Sai (×)', 'script': '临近冬天，水果虽然比夏天贵。'},
        {'id': 12, 'type': 'listening_tf', 'prompt': '★ 他现在还不能打篮球。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Đúng (√)', 'script': '医生说他很快就能像以前一样打篮球了。'},
        {'id': 13, 'type': 'listening_tf', 'prompt': '★ 儿子比爸爸矮。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Sai (×)', 'script': '儿子十七岁了，现在他和爸爸一样高了。'},
        {'id': 14, 'type': 'listening_tf', 'prompt': '★ 八月十五的月亮大。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Đúng (√)', 'script': '八月十五的晚上，月亮就像一个白色的大盘子。'},
        {'id': 15, 'type': 'listening_tf', 'prompt': '★ 他现在住在公司附近。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Đúng (√)', 'script': '新的房子虽然小了点儿，但是离公司很近。'},
        {'id': 16, 'type': 'listening_tf', 'prompt': '★ 女儿喜欢小狗。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Sai (×)', 'script': '我家有一只小猫，女儿特别喜欢和它在一起玩儿。'},
        {'id': 17, 'type': 'listening_tf', 'prompt': '★ 老李第一次坐船。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Đúng (√)', 'script': '老李第一次坐船，觉得头晕。'},
        {'id': 18, 'type': 'listening_tf', 'prompt': '★ 他在黑板上画熊猫。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Sai (×)', 'script': '耳朵、鼻子都画完了，现在该画这只熊猫的脚了。'},
        {'id': 19, 'type': 'listening_tf', 'prompt': '★ 他的成绩不错。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Đúng (√)', 'script': '在电子信箱里看到了成绩单，我的成绩有了很大提高。'},
        {'id': 20, 'type': 'listening_tf', 'prompt': '★ 高兴的时候不会哭。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Sai (×)', 'script': '有的人在高兴的时候也会哭。'},
        {'id': 21, 'type': 'listening_mc', 'prompt': '男的想让小王做什么？', 'options': ['A 开门', 'B 拿东西', 'C 去超市买东西'], 'answer': 'A 开门', 'script': '男：小王，帮我开一下门，好吗？女：没问题。'},
        {'id': 22, 'type': 'listening_mc', 'prompt': '男的怎么去机场？', 'options': ['A 坐出租车', 'B 坐地铁', 'C 坐公共汽车'], 'answer': 'C 坐公共汽车', 'script': '男：公共汽车很方便，直接就能到。'},
        {'id': 23, 'type': 'listening_mc', 'prompt': '关于男的，可以知道什么？', 'options': ['A 生病了', 'B 喜欢喝茶', 'C 没戴眼镜'], 'answer': 'C 没戴眼镜', 'script': '男：我的眼镜呢？女：你戴在眼睛上呢。'},
        {'id': 24, 'type': 'listening_mc', 'prompt': '女的为什么不买那双鞋？', 'options': ['A 太贵了', 'B 太重了', 'C 太小了'], 'answer': 'C 太小了', 'script': '女：颜色是不错，但是太小了。'},
        {'id': 25, 'type': 'listening_mc', 'prompt': '他们是什么关系？', 'options': ['A 邻居', 'B 同学', 'C 老师和学生'], 'answer': 'A 邻居', 'script': '女：张先生，您出去啊？男：对，去倒垃圾。'},
        {'id': 26, 'type': 'listening_mc', 'prompt': '小李现在最可能在哪儿？', 'options': ['A 超市', 'B 机场', 'C 车站'], 'answer': 'A 超市', 'script': '女：他去超市买点儿东西。'},
        {'id': 27, 'type': 'listening_mc', 'prompt': '关于女的，可以知道什么？', 'options': ['A 准备买鞋', 'B 觉得感冒了', 'C 没上过大学'], 'answer': 'B 觉得感冒了', 'script': '女：我觉得有点儿冷， nervous 可能感冒了。'},
        {'id': 28, 'type': 'listening_mc', 'prompt': '蛋糕是谁做的？', 'options': ['A 姐姐', 'B 妈妈', 'C 弟弟'], 'answer': 'A 姐姐', 'script': '男：姐，您做的蛋糕真好吃！'},
        {'id': 29, 'type': 'listening_mc', 'prompt': '这件衬衫 pessimism 怎么样？', 'options': ['A 太贵了', 'B 太大了', 'C 太旧了'], 'answer': 'A 太贵了', 'script': '女：这件衬衫是很好，就是太贵了。'},
        {'id': 30, 'type': 'listening_mc', 'prompt': '女的主要是什么意思？', 'options': ['A 喜欢看足球', 'B 想踢足球', 'C 受男朋友影响'], 'answer': 'C 受男朋友影响', 'script': '女：我的男朋友喜欢看足球比赛，是他影响了我。'},
        {'id': 31, 'type': 'listening_mc', 'prompt': '关于这件衣服，可以知道什么？', 'options': ['A 颜色好看', 'B 太短了', 'C 适合夏天'], 'answer': 'A 颜色好看', 'script': '男：颜色真好看，特别适合你。'},
        {'id': 32, 'type': 'listening_mc', 'prompt': '男的准备怎么做？', 'options': ['A 去买书', 'B 问老师', 'C 查字典'], 'answer': 'C 查字典', 'script': '男：我也不是很清楚，我查查字典吧。'},
        {'id': 33, 'type': 'listening_mc', 'prompt': '他们最可能在什么地方？', 'options': ['A 饭馆儿', 'B 商店', 'C 车站'], 'answer': 'A 饭馆儿', 'script': '男：给我们拿一本菜单，谢谢。'},
        {'id': 34, 'type': 'listening_mc', 'prompt': '女的怎么了？', 'options': ['A 忘记拿钥匙', 'B 找不到护照', 'C 迷路了'], 'answer': 'B 找不到护照', 'script': '女：糟了，我的护照好像不见了！'},
        {'id': 35, 'type': 'listening_mc', 'prompt': '关于男的，可以知道什么？', 'options': ['A 会骑马', 'B 不会游泳', 'C 喜欢跑步'], 'answer': 'A 会骑马', 'script': '男：我从小在农村长大，几岁的时候就会骑马了。'}
    ]

    reading_31003 = [
        {'id': 41, 'type': 'reading_mc', 'prompt': '他女朋友比他大一岁，很可爱，而且很聪明。', 'options': ['A 已经都解决了', 'B 一起去踢足球', 'C 冰箱里还有不少香蕉', 'D 小王没来？', 'E 我们是经过同事介绍认识的'], 'answer': 'E 我们是经过同事介绍认识的', 'explanation': 'Nói về bạn gái / giới thiệu người quen.'},
        {'id': 42, 'type': 'reading_mc', 'prompt': '奶奶，家里是不是没水果了？', 'options': ['A 已经都解决了', 'B 一起去踢足球', 'C 冰箱里还有不少香蕉和葡萄呢', 'D 小王没来？', 'E 我们是经过同事介绍认识的'], 'answer': 'C 冰箱里还有不少香蕉和葡萄呢', 'explanation': 'Nói về trái cây / hoa quả.'},
        {'id': 43, 'type': 'reading_mc', 'prompt': '上次会上说到的那些问题怎么样了？', 'options': ['A 已经都解决了，校长，您放心吧', 'B 一起去踢足球', 'C 冰箱里还有不少香蕉', 'D 小王没来？', 'E 我们是经过同事介绍认识的'], 'answer': 'A 已经都解决了，校长，您放心吧', 'explanation': 'Nói về giải quyết vấn đề.'},
        {'id': 44, 'type': 'reading_mc', 'prompt': '你等我一下，我去换一双鞋就来。', 'options': ['A 已经都解决了', 'B 一起去踢足球，好不好？', 'C 冰箱里还有不少香蕉', 'D 小王没来？', 'E 我们是经过同事介绍认识的'], 'answer': 'B 一起去踢足球，好不好？', 'explanation': 'Rủ đi chơi thể thao / thay giày.'},
        {'id': 45, 'type': 'reading_mc', 'prompt': '他去火车站了，我刚才在电梯门口看见他了。', 'options': ['A 已经都解决了', 'B 一起去踢足球', 'C 冰箱里还有不少香蕉', 'D 小王没来？打他电话怎么一直没人接？', 'E 我们是经过同事介绍认识的'], 'answer': 'D 小王没来？打他电话怎么一直没人接？', 'explanation': 'Hỏi về tung tích của ai đó.'},
        {'id': 51, 'type': 'fill_gap', 'prompt': '有些事情看上去很（  ），但要做好，其实不容易。', 'options': ['A 简单', 'B 举行', 'C 像', 'D 复习'], 'answer': 'A 简单', 'explanation': 'Từ cần điền: 简单 (đơn giản).'},
        {'id': 52, 'type': 'fill_gap', 'prompt': '听张先生说，机场（  ）那个宾馆的环境不错。', 'options': ['A 简单', 'B 附近', 'C 像', 'D 复习'], 'answer': 'B 附近', 'explanation': 'Từ cần điền: 附近 (gần/lân cận).'},
        {'id': 53, 'type': 'fill_gap', 'prompt': '那个会议要在我们学校（  ），所以老师们最近特别忙。', 'options': ['A 简单', 'B 举行', 'C 像', 'D 复习'], 'answer': 'B 举行', 'explanation': 'Từ cần điền: 举行 (cử hành/tổ chức).'},
        {'id': 54, 'type': 'fill_gap', 'prompt': '她和她妈妈长得真（  ）啊！', 'options': ['A 简单', 'B 举行', 'C 像', 'D 复习'], 'answer': 'C 像', 'explanation': 'Từ cần điền: 像 (giống nhau).'},
        {'id': 55, 'type': 'fill_gap', 'prompt': '明天上午考数学，你（  ）得怎么样了？', 'options': ['A 简单', 'B 举行', 'C 像', 'D 复习'], 'answer': 'D 复习', 'explanation': 'Từ cần điền: 复习 (ôn tập).'},
        {'id': 56, 'type': 'fill_gap', 'prompt': 'A：怎么样，这房子您还（  ）吧？ B：很不错，但我还想看看其他的。', 'options': ['A 普通话', 'B 满意', 'C 终于', 'D 骑'], 'answer': 'B 满意', 'explanation': 'Từ cần điền: 满意 (hài lòng).'},
        {'id': 57, 'type': 'fill_gap', 'prompt': 'A：照片上（  ）马的这个人是你爸爸？ B：是的，那时他刚参加工作，很年轻。', 'options': ['A 普通话', 'B 满意', 'C 终于', 'D 骑'], 'answer': 'D 骑', 'explanation': 'Từ cần điền: 骑 (cưỡi ngựa).'},
        {'id': 58, 'type': 'fill_gap', 'prompt': 'A：儿子，快起床，外面天气非常好，我们出去跑跑步。 B：今天是周末，您让我再睡（  ）吧。', 'options': ['A 一会儿', 'B 满意', 'C 终于', 'D 骑'], 'answer': 'A 一会儿', 'explanation': 'Từ cần điền: 一会儿 (một lát).'},
        {'id': 59, 'type': 'fill_gap', 'prompt': 'A：他的（  ）说得真好。 B：当然了，你不知道？他是北京人。', 'options': ['A 普通话', 'B 满意', 'C 终于', 'D 骑'], 'answer': 'A 普通话', 'explanation': 'Từ cần điền: 普通话 (tiếng Phổ thông).'},
        {'id': 60, 'type': 'fill_gap', 'prompt': 'A：8 年了，她（  ）同意跟我结婚了。 B：真的吗？太好了！我真为你高兴！', 'options': ['A 普通话', 'B 满意', 'C 终于', 'D 骑'], 'answer': 'C 终于', 'explanation': 'Từ cần điền: 终于 (cuối cùng).'},
        {'id': 61, 'type': 'reading_mc', 'prompt': '到了机场，他发现护照不见了，在行李箱里找了半天，也没找到，很着急。\n★ 他为什么着急？', 'options': ['A 迟到了', 'B 忘记拿机票了', 'C 找不到护照了'], 'answer': 'C 找不到护照了', 'explanation': 'Chủ đề: 不见了护照.'},
        {'id': 62, 'type': 'reading_mc', 'prompt': '人们经常说：“面包会有的，牛奶也会有的。”是的，如果努力，什么都会有的。\n★ 这句话主要想告诉我们：', 'options': ['A 要相信别人', 'B 兴趣最重要', 'C 努力才有希望'], 'answer': 'C 努力才有希望', 'explanation': 'Chủ đề: 如果努力，什么都会有的.'},
        {'id': 63, 'type': 'reading_mc', 'prompt': '上个星期和朋友们去游泳，把我累坏了，到现在我的腿还在疼。看来我是应该多锻炼锻炼了。\n★ 他打算：', 'options': ['A 去医院', 'B 锻炼身体', 'C 下午去游泳'], 'answer': 'B 锻炼身体', 'explanation': 'Chủ đề: 应该多锻炼锻炼.'},
        {'id': 64, 'type': 'reading_mc', 'prompt': '越高的地方越冷，山路也越难走。但是不用担心，有我呢，我去年秋天爬过这个山，这儿我还是比较了解的。\n★ 根据这段话，可以知道什么？', 'options': ['A 他第一次爬这个山', 'B 他现在腿疼', 'C 他了解这个山'], 'answer': 'C 他了解这个山', 'explanation': 'Chủ đề: 我还是比较了解的.'},
        {'id': 65, 'type': 'reading_mc', 'prompt': '我在国外留学的时候，只要有时间，就会去当地人家里做客。在这期间，我认识了很多朋友，也更了解了那里的文化。\n★ 根据这段话，可以知道他：', 'options': ['A 没留过学', 'B 了解了当地文化', 'C 喜欢打篮球'], 'answer': 'B 了解了当地文化', 'explanation': 'Chủ đề: 了解了那里的文化.'}
    ]

    writing_31003 = [
        {'id': 71, 'type': 'reorder', 'prompt': '', 'words': ['把', '手机', '送给', '她', '决定', '弟弟', '。'], 'correct': '她决定把手机送给弟弟。'},
        {'id': 72, 'type': 'reorder', 'prompt': '', 'words': ['我和', '这个学生', '很久', '没见面了', '。'], 'correct': '我和这个学生很久没见面了。'},
        {'id': 73, 'type': 'reorder', 'prompt': '', 'words': ['这个城市的', '春天', '经常', '刮风', '。'], 'correct': '这个城市的春天经常刮风。'},
        {'id': 74, 'type': 'reorder', 'prompt': '', 'words': ['他的', '汉字', '写得', '很漂亮', '。'], 'correct': '他的汉字写得很漂亮。'},
        {'id': 75, 'type': 'reorder', 'prompt': '', 'words': ['叔叔的', '太阳镜', '花了', '900块钱', '。'], 'correct': '叔叔的太阳镜花了900块钱。'},
        {'id': 76, 'type': 'char_fill', 'prompt': '那轮（ yuè ）亮又大又圆。', 'correct': '月'},
        {'id': 77, 'type': 'char_fill', 'prompt': '太阳就像一个（ bái ）色的盘子。', 'correct': '白'},
        {'id': 78, 'type': 'char_fill', 'prompt': '一（ qiān ）万年前，动物们出现了吗？', 'correct': '千'},
        {'id': 79, 'type': 'char_fill', 'prompt': '外面下雪了，你让孩子路上小（ xīn ）点儿。', 'correct': '心'},
        {'id': 80, 'type': 'char_fill', 'prompt': '生病了要注意休息，（ yīn ）为健康最重要。', 'correct': '因'}
    ]

    # --- ĐỀ H31008 ---
    listening_31008 = [
        {'id': 11, 'type': 'listening_tf', 'prompt': '★ 空调的声音太大。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Sai (×)', 'script': '房间里的空调声音太大，吵得我一直没睡着。'},
        {'id': 12, 'type': 'listening_tf', 'prompt': '★ 今天天气很冷。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Sai (×)', 'script': '外面太阳很大，一点儿也不冷。'},
        {'id': 13, 'type': 'listening_tf', 'prompt': '★ 王经理是北方人。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Đúng (√)', 'script': '王经理是北方人，非常喜欢吃面条儿。'},
        {'id': 14, 'type': 'listening_tf', 'prompt': '★ 他们现在在电梯里。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Sai (×)', 'script': '我们在楼梯这儿呢，等会儿再坐电梯。'},
        {'id': 15, 'type': 'listening_tf', 'prompt': '★ 今天的月亮很大。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Đúng (√)', 'script': '你看，今晚的月亮又大又亮，真美啊。'},
        {'id': 16, 'type': 'listening_tf', 'prompt': '★ 小鸡会游泳。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Sai (×)', 'script': '小鸭子会游泳，但是小鸡可不会游泳。'},
        {'id': 17, 'type': 'listening_tf', 'prompt': '★ 小王的丈夫爱看篮球比赛。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Đúng (√)', 'script': '小王的丈夫是个体育迷，特别喜欢看篮球比赛。'},
        {'id': 18, 'type': 'listening_tf', 'prompt': '★ 努力的人机会多。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Đúng (√)', 'script': '只要你努力，机会总是有的。'},
        {'id': 19, 'type': 'listening_tf', 'prompt': '★ 葡萄不好吃。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Sai (×)', 'script': '今天的葡萄又甜又新鲜，非常美味。'},
        {'id': 20, 'type': 'listening_tf', 'prompt': '★ 老刘喝酒容易脸红。', 'options': ['Đúng (√)', 'Sai (×)'], 'answer': 'Đúng (√)', 'script': '老刘一喝酒脸就红，大家都很清楚。'},
        {'id': 21, 'type': 'listening_mc', 'prompt': '小张现在在哪儿？', 'options': ['A 办公室', 'B 图书馆', 'C 教室'], 'answer': 'B 图书馆', 'script': '男：小张，你在哪儿呢？\n女：我在图书馆看书呢，一杯茶就回去。'},
        {'id': 22, 'type': 'listening_mc', 'prompt': '男的想喝什么？', 'options': ['A 咖啡', 'B 牛奶', 'C 果汁'], 'answer': 'C 果汁', 'script': '女：你想喝点儿什么？有牛奶和咖啡。\n男：给我拿一杯果汁吧，谢谢。'},
        {'id': 23, 'type': 'listening_mc', 'prompt': '女的觉得那件衬衫怎么样？', 'options': ['A 太贵', 'B 很合适', 'C 颜色深'], 'answer': 'B 很合适', 'script': '男：这件衬衫你穿真不错。\n女：我也觉得挺合适的，大小刚好。'},
        {'id': 24, 'type': 'listening_mc', 'prompt': '男的要去哪里？', 'options': ['A 医院', 'B 车站', 'C 银行'], 'answer': 'A 医院', 'script': '女：你急急忙忙地要去哪儿？\n男：我爷爷身体不舒服，我去医院看看他。'},
        {'id': 25, 'type': 'listening_mc', 'prompt': '关于小王，可以知道什么？', 'options': ['A 还没结婚', 'B 已经下班了', 'C 在打扫房间'], 'answer': 'A 还没结婚', 'script': '男：小王今年多大了？结婚了吗？\n女：她今年二十五，还没结婚呢。'},
        {'id': 26, 'type': 'listening_mc', 'prompt': '比赛什么时候开始？', 'options': ['A 2点', 'B 3点', 'C 4点'], 'answer': 'B 3点', 'script': '女：足球比赛几点开始？\n男：下午三点，还有半个小时。'},
        {'id': 27, 'type': 'listening_mc', 'prompt': '关于男的，可以知道什么？', 'options': ['A 怕冷', 'B 不爱吃鱼', 'C 喜欢买东西'], 'answer': 'B 不爱吃鱼', 'script': '女：今天的鱼做得不错，你怎么不吃？\n男：我从小就不太爱吃鱼。'},
        {'id': 28, 'type': 'listening_mc', 'prompt': '天气怎么样？', 'options': ['A 刮风了', 'B 下雨了', 'C 阴天'], 'answer': 'C 阴天', 'script': '女：外面下雨了吗？\n男：还没下，不过天阴得很厉害。'},
        {'id': 29, 'type': 'listening_mc', 'prompt': '男的在做什么？', 'options': ['A 看报纸', 'B 听音乐', 'C 复习功课'], 'answer': 'A 看报纸', 'script': '女：别看报纸了，快准备吃饭吧。\n男：好的，看完这篇新闻就来。'},
        {'id': 30, 'type': 'listening_mc', 'prompt': '女的主要想表达什么？', 'options': ['A 感谢男的', 'B 表达不满', 'C 邀请男的'], 'answer': 'A 感谢男的', 'script': '女：这次多亏了你帮忙，真的太谢谢你了！\n男：不用客气，大家都是朋友。'},
        {'id': 31, 'type': 'listening_mc', 'prompt': '关于会议，可以知道什么？', 'options': ['A 已经结束了', 'B 迟到了', 'C 9点开始'], 'answer': 'C 9点开始', 'script': '女：会议几点开始？\n男：九点，还有十五分钟。'},
        {'id': 32, 'type': 'listening_mc', 'prompt': '男的认为那个饭馆儿怎么样？', 'options': ['A 菜太辣', 'B 服务差', 'C 菜很好吃'], 'answer': 'C 菜很好吃', 'script': '女：那家饭馆儿环境虽然一般，但菜做得真不错。\n男：对，我也觉得很好吃。'},
        {'id': 33, 'type': 'listening_mc', 'prompt': '女的要买什么？', 'options': ['A 水果', 'B 蔬菜', 'C 面包'], 'answer': 'B 蔬菜', 'script': '女：我去超市买点儿蔬菜，你想要什么吗？\n男：帮我买一瓶牛奶吧。'},
        {'id': 34, 'type': 'listening_mc', 'prompt': '关于小刘，可以知道什么？', 'options': ['A 换工作了', 'B 出国了', 'C 生病了'], 'answer': 'A 换工作了', 'script': '女：小刘还在以前那个公司吗？\n男：没有，他上个月换新工作了。'},
        {'id': 35, 'type': 'listening_mc', 'prompt': '他们准备什么时候去爬山？', 'options': ['A 周六', 'B 周日', 'C 下周'], 'answer': 'B 周日', 'script': '女：我们周六去爬山怎么样？\n男：周六我有事，周日去吧。'}
    ]

    reading_31008 = [
        {'id': 41, 'type': 'reading_mc', 'prompt': '没关系，我吃过药了。', 'options': ['A 特别胖', 'B 生日快乐', 'C 我来洗碗', 'D 需不需要去房间休息一下？', 'E 在外面照顾好自己'], 'answer': 'D 需不需要去房间休息一下？', 'explanation': 'Hỏi thăm sức khỏe/uống thuốc.'},
        {'id': 42, 'type': 'reading_mc', 'prompt': '他从去年秋天开始锻炼，现在不到 70 公斤。', 'options': ['A 我记得你弟弟以前特别胖。', 'B 生日快乐', 'C 我来洗碗', 'D 需不需要去房间休息', 'E 在外面照顾好自己'], 'answer': 'A 我记得你弟弟以前特别胖。', 'explanation': 'Nói về cân nặng/giảm cân.'},
        {'id': 43, 'type': 'reading_mc', 'prompt': '好，我会给你打电话或者写电子邮件的。', 'options': ['A 特别胖', 'B 生日快乐', 'C 我来洗碗', 'D 需不需要去房间休息', 'E 明天就要出国了？在外面注意身体，照顾好自己。'], 'answer': 'E 明天就要出国了？在外面注意身体，照顾好自己。', 'explanation': 'Dặn dò khi đi xa/giữ liên lạc.'},
        {'id': 44, 'type': 'reading_mc', 'prompt': '不用，你把筷子和杯子拿过来就可以了。', 'options': ['A 特别胖', 'B 生日快乐', 'C 今天我来洗碗，你累一天了，去看电视吧。', 'D 需不需要去房间休息', 'E 在外面照顾好自己'], 'answer': 'C 今天我来洗碗，你累一天了，去看电视吧。', 'explanation': 'Nói về việc nhà/rửa bát.'},
        {'id': 45, 'type': 'reading_mc', 'prompt': '大家来吃蛋糕吧，这块儿大的给你。', 'options': ['A 特别胖', 'B 祝您生日快乐！这是我送您的礼物。', 'C 我来洗碗', 'D 需不需要去房间休息', 'E 在外面照顾好自己'], 'answer': 'B 祝您生日快乐！这是我送您的礼物。', 'explanation': 'Ăn bánh sinh nhật.'},
        {'id': 51, 'type': 'fill_gap', 'prompt': '这个城市有几百年的（  ）了。', 'options': ['A 聪明', 'B 几乎', 'C 解决', 'D 历史'], 'answer': 'D 历史', 'explanation': 'Từ cần điền: 历史 (lịch sử).'},
        {'id': 52, 'type': 'fill_gap', 'prompt': '儿子长大了，都快一米八了，（  ）和他爸爸一样高了。', 'options': ['A 聪明', 'B 几乎', 'C 解决', 'D 历史'], 'answer': 'B 几乎', 'explanation': 'Từ cần điền: 几乎 (hầu như/gần như).'},
        {'id': 53, 'type': 'fill_gap', 'prompt': '小黄是我的好朋友，她和我的（  ）一直很好。', 'options': ['A 聪明', 'B 几乎', 'C 关系', 'D 历史'], 'answer': 'C 关系', 'explanation': 'Từ cần điền: 关系 (quan hệ/mối quan hệ).'},
        {'id': 54, 'type': 'fill_gap', 'prompt': '多吃鱼会使人变得更（  ）。', 'options': ['A 聪明', 'B 几乎', 'C 解决', 'D 历史'], 'answer': 'A 聪明', 'explanation': 'Từ cần điền: 聪明 (thông minh).'},
        {'id': 55, 'type': 'fill_gap', 'prompt': '我们已经找到（  ）问题的办法了。', 'options': ['A 聪明', 'B 几乎', 'C 解决', 'D 历史'], 'answer': 'C 解决', 'explanation': 'Từ cần điền: 解决 (giải quyết).'},
        {'id': 56, 'type': 'fill_gap', 'prompt': 'A：你（  ）的这是猫？\nB：大熊猫！它在爬树。这也看不懂？', 'options': ['A 画', 'B 选择', 'C 马上', 'D 结婚'], 'answer': 'A 画', 'explanation': 'Từ cần điền: 画 (vẽ).'},
        {'id': 57, 'type': 'fill_gap', 'prompt': 'A：你低着头想什么呢？\nB：是工作还是读书，我不知道应该怎么（  ）才好。', 'options': ['A 画', 'B 选择', 'C 马上', 'D 结婚'], 'answer': 'B 选择', 'explanation': 'Từ cần điền: 选择 (lựa chọn).'},
        {'id': 58, 'type': 'fill_gap', 'prompt': 'A：你渴不？我想去买点儿水。\nB：那你快一点儿，表演（  ）就要开始了。', 'options': ['A 画', 'B 选择', 'C 马上', 'D 结婚'], 'answer': 'C 马上', 'explanation': 'Từ cần điền: 马上 (ngay lập tức).'},
        {'id': 59, 'type': 'fill_gap', 'prompt': 'A：相信我，这件事对公司不会有影响的。\nB：夏经理，你把事情想得太（  ）了。', 'options': ['A 画', 'B 简单', 'C 马上', 'D 结婚'], 'answer': 'B 简单', 'explanation': 'Từ cần điền: 简单 (đơn giản).'},
        {'id': 60, 'type': 'fill_gap', 'prompt': 'A：好久没看见白老师了，他不在这儿住了？\nB：是，他（  ）以后就和妻子搬到学校去住了。', 'options': ['A 画', 'B 选择', 'C 马上', 'D 结婚'], 'answer': 'D 结婚', 'explanation': 'Từ cần điền: 结婚 (kết hôn).'},
        {'id': 61, 'type': 'reading_mc', 'prompt': '最近几年，这里的变化很大，车辆更多了，街道更干净了，天更蓝了，树更绿了。\n★ 这里最近几年怎么样？', 'options': ['A 环境变好了', 'B 和过去相同', 'C 变得更差了'], 'answer': 'A 环境变好了', 'explanation': 'Chủ đề: Môi trường tốt lên.'},
        {'id': 62, 'type': 'reading_mc', 'prompt': '人们根据季节的变化来决定喝什么茶。老人们经常说：“春天最好喝花茶，冬天最好喝红茶。”\n★ 这段话告诉我们：', 'options': ['A 茶有什么作用', 'B 老人爱喝红茶', 'C 不同季节喝不同的茶'], 'answer': 'C 不同季节喝不同的茶', 'explanation': 'Chủ đề: 根据季节喝茶.'},
        {'id': 63, 'type': 'reading_mc', 'prompt': '汉字有多少个？这个问题谁也回答不清楚，《汉语大字典》里有五六万字，普通的小字典，一本也有八九千字。但人们常用的也就两千多个，认识这两千多个字，读书看报就没什么问题了。\n★ 这段话的主要意思是：', 'options': ['A 汉字很难写', 'B 要学会查字典', 'C 常用汉字不多'], 'answer': 'C 常用汉字不多', 'explanation': 'Chủ đề: 人们常用的也就两千多个.'},
        {'id': 64, 'type': 'reading_mc', 'prompt': '为什么很多人愿意在网上买东西呢？因为非常方便，而且还便宜，如果对买到的东西有不满意的地方，也可以要求换新的。\n★ 在网上买东西：', 'options': ['A 比较贵', 'B 花钱少', 'C 花的时间多'], 'answer': 'B 花钱少', 'explanation': 'Chủ đề: 而且还便宜.'},
        {'id': 65, 'type': 'reading_mc', 'prompt': '每个人都有自己的脾气，遇到不高兴的事，发脾气是正常的。但是如果总是不高兴，甚至经常生气，那就需要特别注意了，这不仅会影响身体健康，也会影响与别人的关系。\n★ 这段话主要想告诉我们：', 'options': ['A 要少生气', 'B 脾气是可以改变的', 'C 不要总吃甜食'], 'answer': 'A 要少生气', 'explanation': 'Chủ đề: 不要经常生气.'}
    ]

    writing_31008 = [
        {'id': 71, 'type': 'reorder', 'prompt': '', 'words': ['那位', '邻居', '很热情', '。'], 'correct': '那位邻居很热情。'},
        {'id': 72, 'type': 'reorder', 'prompt': '', 'words': ['这个楼', '一共', '三层', '。'], 'correct': '这个楼一共三层。'},
        {'id': 73, 'type': 'reorder', 'prompt': '', 'words': ['菜单', '被', '服务员', '拿走了', '。'], 'correct': '菜单被服务员拿走了。'},
        {'id': 74, 'type': 'reorder', 'prompt': '', 'words': ['中国南方的雨水', '比', '北方', '多', '。'], 'correct': '中国南方的雨水比北方多。'},
        {'id': 75, 'type': 'reorder', 'prompt': '', 'words': ['把', '冰箱', '放', '厨房里吧', '。'], 'correct': '把冰箱放厨房里吧。'},
        {'id': 76, 'type': 'char_fill', 'prompt': '你姐姐的孩子上（ jǐ ）年级？', 'correct': '几'},
        {'id': 77, 'type': 'char_fill', 'prompt': '马小姐，谢谢关（ xīn ），我不发烧了，头也不疼了。', 'correct': '心'},
        {'id': 78, 'type': 'char_fill', 'prompt': '对不起，（ xià ）午有个重要的会议，我让司机去医院接你好不好？', 'correct': '下'},
        {'id': 79, 'type': 'char_fill', 'prompt': '经过4个星期的练习，叔叔的普通话水平有了很（ dà ）提高。', 'correct': '大'},
        {'id': 80, 'type': 'char_fill', 'prompt': '这个小太阳表示晴天，（ yún ）表示阴天。', 'correct': '云'}
    ]

    return {
        'H31003': {
            'title': 'H31003',
            'audio_file': 'H31003.mp3',
            'listening': listening_31003,
            'reading': reading_31003,
            'writing': writing_31003
        },
        'H31008': {
            'title': 'H31008',
            'audio_file': 'H31008.mp3',
            'listening': listening_31008,
            'reading': reading_31008,
            'writing': writing_31008
        }
    }


# ==========================================
# 3. HÀM GỬI ĐIỂM VỀ GOOGLE SHEET CÔ BẢO NGỌC
# ==========================================
def send_score_to_google_sheet(student_name, class_name, exam_code, section, score, total_questions):
    DEFAULT_WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycby7XFJf1fV5aL5UiRY0h-kAxHVszQvUnAgSt5brar-K7Fe7-BV9_ifRTZ7suCPEC1BoHg/exec'
    webhook_url = st.secrets.get('SHEET_WEBHOOK_URL', DEFAULT_WEBHOOK_URL)
    
    payload = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'student_name': student_name,
        'class_name': class_name,
        'exam_code': exam_code,
        'section': section,
        'score': score,
        'total': total_questions,
        'percentage': round((score / total_questions) * 100, 1) if total_questions > 0 else 0
    }
    
    if webhook_url:
        try:
            requests.post(webhook_url, json=payload, timeout=5)
            return True
        except Exception:
            pass
            
    if 'sheet_history' not in st.session_state:
        st.session_state.sheet_history = []
    st.session_state.sheet_history.append(payload)
    return True


# ==========================================
# 4. QUẢN LÝ SESSION STATE
# ==========================================
if 'selected_exam' not in st.session_state:
    st.session_state.selected_exam = None

if 'student_name' not in st.session_state:
    st.session_state.student_name = ''

if 'class_name' not in st.session_state:
    st.session_state.class_name = ''

if 'submitted_sections' not in st.session_state:
    st.session_state.submitted_sections = {}

if 'exam_start_times' not in st.session_state:
    st.session_state.exam_start_times = {}

if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}


# ==========================================
# 5. TRANG 1: DANH SÁCH MÃ ĐỀ (GRID PASTEL)
# ==========================================
def render_landing_page():
    st.markdown("<h1 style='text-align: center; color: #1A365D; font-size: 36px; font-weight: bold;'>🎓 LUYỆN ĐỀ HSK3</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #4A5568;'>Vui lòng điền thông tin và chọn Mã Đề Thi để bắt đầu</p>", unsafe_allow_html=True)
    st.write('---')

    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.session_state.student_name = st.text_input('👤 Họ và tên học viên:', value=st.session_state.student_name, placeholder='Ví dụ: Nguyễn Văn A')
    with col_info2:
        st.session_state.class_name = st.text_input('🏫 Tên lớp:', value=st.session_state.class_name, placeholder='Ví dụ: HSK3-K24')

    st.write('')
    st.markdown('### 📋 Danh sách Mã Đề Thi:')

    exams = load_exam_data()
    exam_codes = list(exams.keys())

    cols = st.columns(2)
    pastel_colors = ['#E8F0FE', '#E6F4EA']
    border_colors = ['#1A365D', '#137333']

    for idx, code in enumerate(exam_codes):
        with cols[idx % 2]:
            p_bg = pastel_colors[idx % len(pastel_colors)]
            p_border = border_colors[idx % len(border_colors)]
            
            st.markdown(f"""
            <div style="background-color: {p_bg}; border: 3px solid {p_border}; border-radius: 14px; padding: 25px 15px; text-align: center; margin-bottom: 15px;">
                <div style="font-size: 32px; font-weight: bold; color: {p_border}; font-family: 'Tahoma', sans-serif;">{code}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f'👉 Vào làm đề {code}', key=f'btn_{code}', use_container_width=True):
                if not st.session_state.student_name.strip():
                    st.error('⚠️ Vui lòng nhập Họ và tên trước khi vào thi!')
                elif not st.session_state.class_name.strip():
                    st.error('⚠️ Vui lòng nhập Tên lớp trước khi vào thi!')
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
        if st.button('⬅️ Trở về chọn đề khác'):
            st.session_state.selected_exam = None
            st.rerun()

    st.write('---')

    SECTION_TIMES = {
        'listening': 35 * 60,
        'reading': 30 * 60,
        'writing': 15 * 60
    }

    if exam_code not in st.session_state.exam_start_times:
        st.session_state.exam_start_times[exam_code] = {
            'listening': time.time(),
            'reading': time.time(),
            'writing': time.time()
        }

    tab_listen, tab_read, tab_write = st.tabs(['🎧 PHẦN NGHE (Listening)', '📖 PHẦN ĐỌC (Reading)', '✍️ PHẦN VIẾT (Writing)'])

    with tab_listen:
        render_section_tab(
            exam_code=exam_code,
            section_key='listening',
            section_title='PHẦN NGHE (听力)',
            questions=exam['listening'],
            max_time_sec=SECTION_TIMES['listening'],
            audio_file=exam['audio_file']
        )

    with tab_read:
        render_section_tab(
            exam_code=exam_code,
            section_key='reading',
            section_title='PHẦN ĐỌC (阅读)',
            questions=exam['reading'],
            max_time_sec=SECTION_TIMES['reading']
        )

    with tab_write:
        render_section_tab(
            exam_code=exam_code,
            section_key='writing',
            section_title='PHẦN VIẾT (书写)',
            questions=exam['writing'],
            max_time_sec=SECTION_TIMES['writing']
        )

    st.markdown("<div class='teacher-footer'>黄宝玉老师</div>", unsafe_allow_html=True)


# ==========================================
# 7. HÀM HIỂN THỊ CHI TIẾT TỪNG PHẦN THI
# ==========================================
def render_section_tab(exam_code, section_key, section_title, questions, max_time_sec, audio_file=None):
    st.subheader(f'📌 {section_title}')

    section_id = f'{exam_code}_{section_key}'
    is_submitted = st.session_state.submitted_sections.get(section_id, False)

    start_time = st.session_state.exam_start_times[exam_code][section_key]
    elapsed = time.time() - start_time
    remaining_sec = max(0, int(max_time_sec - elapsed))

    # JavaScript Đồng hồ đếm ngược chạy thực tế trong IFrame
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
            st.error('🚨 ĐÃ HẾT GIỜ LÀM BÀI! Tự động nộp phần này...')
            st.session_state.submitted_sections[section_id] = True
            is_submitted = True
            st.rerun()

    if audio_file and section_key == 'listening':
        st.audio(f'{audio_file}', format='audio/mp3')

    st.write('')

    answers_key_prefix = f'ans_{exam_code}_{section_key}'

    for idx, q in enumerate(questions):
        q_id = q['id']
        q_key = f'{answers_key_prefix}_{q_id}'

        st.markdown("<div class='question-box'>", unsafe_allow_html=True)
        
        # Hiển thị STT câu
        if q['prompt']:
            st.markdown(f"**Câu {q_id}:** <span class='chinese-text' style='font-size:19px;'>{q['prompt']}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"**Câu {q_id}:**", unsafe_allow_html=True)

        # Chữ Hán phần sắp xếp to (28px)
        if q['type'] == 'reorder':
            words_html = ''.join([f"<span class='word-token'>{w}</span>" for w in q.get('words', [])])
            st.markdown(f"<div style='margin: 12px 0 18px 0; line-height: 2.2;'>{words_html}</div>", unsafe_allow_html=True)

        if not is_submitted:
            if q['type'] in ['listening_tf', 'listening_mc', 'fill_gap', 'reading_mc']:
                user_ans = st.radio('Chọn đáp án:', q['options'], key=q_key, index=None)
                st.session_state.user_answers[q_key] = user_ans
            elif q['type'] in ['reorder', 'char_fill']:
                user_ans = st.text_input('Nhập câu trả lời:', key=q_key)
                st.session_state.user_answers[q_key] = user_ans
        else:
            user_ans = st.session_state.user_answers.get(q_key, '')
            
            if q['type'] in ['reorder', 'char_fill']:
                is_correct = (user_ans.strip() == q['correct'].strip())
                expected = q['correct']
            else:
                is_correct = (user_ans == q['answer'])
                expected = q['answer']

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

            if 'script' in q:
                with st.expander('📝 Xem Script bài nghe'):
                    st.write(q['script'])
            if 'explanation' in q:
                with st.expander('💡 Giải thích đáp án'):
                    st.write(q['explanation'])

        st.markdown('</div>', unsafe_allow_html=True)

    st.write('')
    if not is_submitted:
        if st.button(f'🚀 NỘP BÀI {section_title.upper()}', key=f'sub_btn_{section_id}', type='primary'):
            st.session_state.submitted_sections[section_id] = True

            correct_count = 0
            for q in questions:
                q_key = f'{answers_key_prefix}_{q["id"]}'
                u_a = st.session_state.user_answers.get(q_key, '')
                if q['type'] in ['reorder', 'char_fill']:
                    if u_a.strip() == q['correct'].strip():
                        correct_count += 1
                else:
                    if u_a == q['answer']:
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
                (st.session_state.user_answers.get(f'{answers_key_prefix}_{q["id"]}', '').strip() == q['correct'].strip())
                if q['type'] in ['reorder', 'char_fill']
                else (st.session_state.user_answers.get(f'{answers_key_prefix}_{q["id"]}', '') == q['answer'])
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

if __name__ == '__main__':
    main()
