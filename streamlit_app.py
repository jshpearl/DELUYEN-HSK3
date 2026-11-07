import streamlit as st
import time
import requests
import json
from datetime import datetime
import streamlit.components.v1 as components

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

    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    .stAppHeader {display: none !important;}

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

EXAM_DATA = {"H31003": {"title": "H31003", "audio_file": "H31003.mp3", "listening": [{"id": 1, "type": "listening_tf", "prompt": "1. ★ 下了飞机，就给我来电话。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：下了飞机，就给我来电话。\n男：好的。你到中国以后，自己照顾好自己。"}, {"id": 2, "type": "listening_tf", "prompt": "2. ★ 二零四房间在前面左边第二个。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：请问，二零四房间在哪儿？\n女：请这边走，前面左边第二个就是。"}, {"id": 3, "type": "listening_tf", "prompt": "3. ★ 现在眼睛已经不红了。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：眼药水用了吗？有作用没？\n男：有作用，现在眼睛已经不红了。"}, {"id": 4, "type": "listening_tf", "prompt": "4. ★ 这些书可以借两个月。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：这些书我可以借多长时间？\n女：一个月。如果看不完，可以再借一个月。"}, {"id": 5, "type": "listening_tf", "prompt": "5. ★ 这张花鸟画是他爷爷画的。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：这张画是你画的吗？\n男：是我爷爷画的，这是他的一张花鸟画。"}, {"id": 6, "type": "listening_tf", "prompt": "6. ★ 女的感冒发烧了。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：你不舒服吗？要不要我带你去医院检查检查？\n女：没关系，我应该是感冒了，有点儿发烧。"}, {"id": 7, "type": "listening_tf", "prompt": "7. ★ 今天的鸡蛋面很好吃。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：今天的鸡蛋面怎么样？\n男：很好吃，我吃饱了。我认为你做饭的水平越来越高了。"}, {"id": 8, "type": "listening_tf", "prompt": "8. ★ 欢迎他来公司工作。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：欢迎你来公司工作。\n女：谢谢您！谢谢您给我这个机会，我会努力的。"}, {"id": 9, "type": "listening_tf", "prompt": "9. ★ 一共三十五块钱。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：我马上就到，已经到楼下了。你好，一共多少钱？\n男：三十五块。"}, {"id": 10, "type": "listening_tf", "prompt": "10. ★ 女的想把头发剪得再短一些。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：小姐，这么长您看可以吗？\n女：再短一些吧。夏天到了，头发还是短一点儿好。"}, {"id": 11, "type": "listening_tf", "prompt": "11. ★ 冬天水果很便宜。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "在这里，冬天的水果虽然比夏天的贵，但是很新鲜。"}, {"id": 12, "type": "listening_tf", "prompt": "12. ★ 他现在还不能打篮球。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "太好了！他几乎不敢相信这是真的。医生说他很快就能像以前一样打篮球了。"}, {"id": 13, "type": "listening_tf", "prompt": "13. ★ 儿子比爸爸矮。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "儿子十七岁了，长得很快。去年买的裤子，现在已经不能穿了，现在他和他爸爸一样高了。"}, {"id": 14, "type": "listening_tf", "prompt": "14. ★ 八月十五的月亮大。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "八月十五的晚上，月亮就像一个白色的大盘子，非常漂亮。中国人喜欢在这一天和家里人一起吃饭，一起看月亮。"}, {"id": 15, "type": "listening_tf", "prompt": "15. ★ 他现在住在公司附近。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "我搬家了。新的房子虽然小了点儿，但是离公司很近。"}, {"id": 16, "type": "listening_tf", "prompt": "16. ★ 女儿喜欢小狗。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "我家有一只小猫，胖胖的，很可爱，女儿经常给它洗澡，特别喜欢和它在一起玩儿。"}, {"id": 17, "type": "listening_tf", "prompt": "17. ★ 老李第一次坐船。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "我看老李的脸色不太好，一问才知道他昨天晚上没睡好觉。他说，他第一次坐船，以为和坐车没什么不同，他现在明白了，差远了。"}, {"id": 18, "type": "listening_tf", "prompt": "18. ★ 他在黑板上画熊猫。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "把椅子上的铅笔给我，谢谢。耳朵、鼻子都画完了，现在该画这只熊猫的脚了。"}, {"id": 19, "type": "listening_tf", "prompt": "19. ★ 他的成绩不错。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "早上，我在电子信箱里看到了我的成绩单，我的成绩比过去有了很大提高。今天一天我都很快乐。"}, {"id": 20, "type": "listening_tf", "prompt": "20. ★ 高兴的时候不会哭。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "哭，不一定表示难过，有的人着急的时候会哭，有的人在高兴的时候也会哭。"}, {"id": 21, "type": "listening_mc", "prompt": "21. 男的送什么礼物了？", "options": ["A 包", "B 衣服", "C 蛋糕"], "answer": "A 包", "script": "女：谢谢你送我的生日礼物！这个包我非常喜欢。\n男：不客气，祝你生日快乐！"}, {"id": 22, "type": "listening_mc", "prompt": "22. 他们最可能是什么关系？", "options": ["A 邻居", "B 同事", "C 服务员和客人"], "answer": "C 服务员和客人", "script": "男：你好，我住六零七，房间里的空调坏了，你能来看看吗？\n女：好的，先生，对不起，我们马上找人来。"}, {"id": 23, "type": "listening_mc", "prompt": "23. 男的正在做什么？", "options": ["A 做作业", "B 睡觉", "C 玩儿游戏"], "answer": "C 玩儿游戏", "script": "女：你回来就一直玩儿游戏，作业写完了吗？\n男：我在学校就写完了。"}, {"id": 24, "type": "listening_mc", "prompt": "24. 女的是什么意思？", "options": ["A 想喝咖啡", "B 不累", "C 哪儿都行"], "answer": "C 哪儿都行", "script": "男：奇怪，我记得这条街上有一个咖啡馆儿的。\n女：没关系，我们找个地方坐坐就行。"}, {"id": 25, "type": "listening_mc", "prompt": "25. 女的为什么不能穿那条裙子？", "options": ["A 胖了", "B 裙子旧了", "C 裙子破了"], "answer": "A 胖了", "script": "女：这条裙子去年才买的，今年就不能穿了。\n男：你吃得太多，也不运动，可能又长十斤肉了吧？"}, {"id": 26, "type": "listening_mc", "prompt": "26. 他们现在在哪儿？", "options": ["A 一层", "B 二层", "C 三层"], "answer": "A 一层", "script": "男：帽子在几层呢？\n女：我看看，一层是家电，二层是衣帽，我们去二层。"}, {"id": 27, "type": "listening_mc", "prompt": "27. 关于女的，可以知道什么？", "options": ["A 要去开会", "B 是经理", "C 已经下班了"], "answer": "B 是经理", "script": "女：再见，一会儿你离开的时候记得关灯。\n男：好的，经理，明天见。"}, {"id": 28, "type": "listening_mc", "prompt": "28. 蛋糕是谁做的？", "options": ["A 姐姐", "B 弟弟", "C 妈妈"], "answer": "A 姐姐", "script": "男：姐，您做的蛋糕真好吃！\n女：洗手了吗？先去把手洗了，然后帮我拿碗筷，准备吃饭。"}, {"id": 29, "type": "listening_mc", "prompt": "29. 这件衬衫怎么样？", "options": ["A 太贵了", "B 很便宜", "C 颜色不好"], "answer": "A 太贵了", "script": "女：这件衬衫是很好，就是太贵了。\n男：那我再给您便宜五十块，怎么样？"}, {"id": 30, "type": "listening_mc", "prompt": "30. 女的主要是什么意思？", "options": ["A 喜欢足球", "B 不喜欢看球", "C 受男朋友影响"], "answer": "C 受男朋友影响", "script": "男：你怎么突然开始关心体育了？\n女：我的男朋友喜欢看足球比赛，是他影响了我。"}, {"id": 31, "type": "listening_mc", "prompt": "31. 小李现在最可能在哪儿？", "options": ["A 超市", "B 学校", "C 家里"], "answer": "A 超市", "script": "男：喂，请问小李在家吗？\n女：他出去了，请问您是哪位？\n男：我姓王，是他的同学。他什么时候回来？\n女：他去超市买点儿东西，可能十分钟就回来了。"}, {"id": 32, "type": "listening_mc", "prompt": "32. 现在几点了？", "options": ["A 10点", "B 9点45", "C 10点15"], "answer": "B 9点45", "script": "女：我们这儿有个西瓜文化节，您有兴趣去看看吗？\n男：当然有兴趣了。\n女：我们可以一边吃西瓜一边看表演。\n男：好，现在差一刻十点，我们现在去？"}, {"id": 33, "type": "listening_mc", "prompt": "33. 女的觉得那本书怎么样？", "options": ["A 没看懂", "B 很有意思", "C 很简单"], "answer": "A 没看懂", "script": "男：你把我的那本书放哪儿了？\n女：在桌子上吧。\n男：我要去还书，今天是最后一天，今天必须还。\n女：还了吧，那本书我也没看懂。"}, {"id": 34, "type": "listening_mc", "prompt": "34. 男的是做什么的？", "options": ["A 老师", "B 司机", "C 医生"], "answer": "B 司机", "script": "女：你好，我去世界公园。\n男：好的，没问题。\n女：从这儿到世界公园远吗？需要多长时间？\n男：不是很远，半个小时吧。"}, {"id": 35, "type": "listening_mc", "prompt": "35. 关于女的，可以知道什么？", "options": ["A 喜欢读书", "B 了解历史", "C 是老师"], "answer": "A 喜欢读书", "script": "男：你知道的怎么这么多，真聪明！\n女：那是因为我看的书多，读书使人聪明。\n男：那你对历史书也了解不少吧，给我介绍几本？\n女：明天吧？我给你写一个单子。"}], "reading": [{"id": 41, "type": "reading_mc", "prompt": "41. 你等我一下，我去换一双鞋就来。", "options": ["A 会做那些题", "B 还有10分钟", "C 一起去踢足球，好不好？", "D 在电梯门口看见他了", "E 冰箱里还有水果"], "answer": "C 一起去踢足球，好不好？", "explanation": "Đối đáp: Rủ đi đá bóng / Đi thay giày."}, {"id": 42, "type": "reading_mc", "prompt": "42. 奶奶，家里是不是没水果了？", "options": ["A 已经都解决了", "B 冰箱里还有不少香蕉和葡萄呢。", "C 我们是经同事介绍认识的", "D 马上就结束了", "E 会做那些题"], "answer": "B 冰箱里还有不少香蕉和葡萄呢。", "explanation": "Hỏi về hoa quả/trái cây trong nhà."}, {"id": 43, "type": "reading_mc", "prompt": "43. 上次会上说到的那些问题怎么样了？", "options": ["A 已经都解决了，校长，您放心吧。", "B 一起去踢足球", "C 冰箱里还有不少香蕉", "D 小王没来？", "E 我们是经过同事介绍认识的"], "answer": "A 已经都解决了，校长，您放心吧。", "explanation": "Báo cáo vấn đề trong cuộc họp trước."}, {"id": 44, "type": "reading_mc", "prompt": "44. 他女朋友比他大一岁，很可爱，而且很聪明。", "options": ["A 已经都解决了", "B 一起去踢足球", "C 冰箱里还有水果", "D 小王没来？", "E 我们是经过同事介绍认识的，已经认识两年了。"], "answer": "E 我们是经过同事介绍认识的，已经认识两年了。", "explanation": "Giới thiệu người yêu quen qua đồng nghiệp."}, {"id": 45, "type": "reading_mc", "prompt": "45. 小王没来？打他电话怎么一直没人接？", "options": ["A 已经都解决了", "B 他去火车站了，我刚才在电梯门口看见他了。", "C 冰箱里还有水果", "D 换一双鞋就来", "E 我们已经认识两年了"], "answer": "B 他去火车站了，我刚才在电梯门口看见他了。", "explanation": "Trả lời câu hỏi tìm người."}, {"id": 46, "type": "fill_gap", "prompt": "46. 有些事情看上去很（     ），但要做好，其实不容易。", "options": ["A 简单", "B 举行", "C 像", "D 复习", "E 附近"], "answer": "A 简单", "explanation": "Từ cần điền: 简单 (đơn giản)."}, {"id": 47, "type": "fill_gap", "prompt": "47. 听张先生说，机场（     ）那个宾馆的环境不错。", "options": ["A 简单", "B 举行", "C 像", "D 复习", "E 附近"], "answer": "E 附近", "explanation": "Từ cần điền: 附近 (gần/lân cận)."}, {"id": 48, "type": "fill_gap", "prompt": "48. 那个会议要在我们学校（     ），所以老师们最近特别忙。", "options": ["A 简单", "B 举行", "C 像", "D 复习", "E 附近"], "answer": "B 举行", "explanation": "Từ cần điền: 举行 (tổ chức/cử hành)."}, {"id": 49, "type": "fill_gap", "prompt": "49. 她和她妈妈长得真（     ）啊！", "options": ["A 简单", "B 举行", "C 像", "D 复习", "E 附近"], "answer": "C 像", "explanation": "Từ cần điền: 像 (giống)."}, {"id": 50, "type": "fill_gap", "prompt": "50. 明天上午考数学，你（     ）得怎么样了？", "options": ["A 简单", "B 举行", "C 像", "D 复习", "E 附近"], "answer": "D 复习", "explanation": "Từ cần điền: 复习 (ôn tập)."}, {"id": 51, "type": "fill_gap", "prompt": "51. A：怎么样，这房子您还（     ）吧？\nB：很不错，但我还想看看其他的。", "options": ["A 终于", "B 普通话", "C 满意", "D 骑", "E 一会儿"], "answer": "C 满意", "explanation": "Từ cần điền: 满意 (hài lòng)."}, {"id": 52, "type": "fill_gap", "prompt": "52. A：照片上（     ）马的这个人是你爸爸？\nB：是的，那时他刚参加工作，很年轻。", "options": ["A 终于", "B 普通话", "C 满意", "D 骑", "E 一会儿"], "answer": "D 骑", "explanation": "Từ cần điền: 骑 (cưỡi)."}, {"id": 53, "type": "fill_gap", "prompt": "53. A：儿子，快起床，外面天气非常好，我们出去跑跑步。\nB：今天是周末，您让我再睡（     ）吧。", "options": ["A 终于", "B 普通话", "C 满意", "D 骑", "E 一会儿"], "answer": "E 一会儿", "explanation": "Từ cần điền: 一会儿 (một lát)."}, {"id": 54, "type": "fill_gap", "prompt": "54. A：他的（     ）说得真好。\nB：当然了，你不知道？他是北京人。", "options": ["A 终于", "B 普通话", "C 满意", "D 骑", "E 一会儿"], "answer": "B 普通话", "explanation": "Từ cần điền: 普通话 (tiếng Phổ thông)."}, {"id": 55, "type": "fill_gap", "prompt": "55. A：8 年了，她（     ）同意跟我结婚了。\nB：真的吗？太好了！我真为你高兴！", "options": ["A 终于", "B 普通话", "C 满意", "D 骑", "E 一会儿"], "answer": "A 终于", "explanation": "Từ cần điền: 终于 (cuối cùng)."}, {"id": 56, "type": "reading_mc", "prompt": "56. 到了机场，他发现护照不见了，在行李箱里找了半天，也没找到，很着急。\n★ 他为什么着急？", "options": ["A 迟到了", "B 忘记拿机票了", "C 找不到护照了"], "answer": "C 找不到护照了", "explanation": "Mất hộ chiếu."}, {"id": 57, "type": "reading_mc", "prompt": "57. 人们经常说：“面包会有的，牛奶也会有的。”是的，如果努力，什么都会有的。\n★ 这句话主要想告诉我们：", "options": ["A 要相信别人", "B 兴趣最重要", "C 努力才有希望"], "answer": "C 努力才有希望", "explanation": "Chủ đề nỗ lực."}, {"id": 58, "type": "reading_mc", "prompt": "58. 上个星期和朋友们去游泳，把我累坏了，到现在我的腿还在疼。看来我是应该多锻炼锻炼了。\n★ 他打算：", "options": ["A 去医院", "B 锻炼身体", "C 下午去游泳"], "answer": "B 锻炼身体", "explanation": "Chủ đề rèn luyện sức khỏe."}, {"id": 59, "type": "reading_mc", "prompt": "59. 越高的地方越冷，山路也越难走。但是不用担心，有我呢，我去年秋天爬过这个山，这儿我还是比较了解的。我饿了，我们先坐下来吃点儿饭、喝点儿水，然后再爬。一会儿我们可以从中间这条路上去。\n★ 根据这段话，可以知道什么？", "options": ["A 他第一次爬这个山", "B 他现在腿疼", "C 他了解这个山"], "answer": "C 他了解这个山", "explanation": "Đoạn văn: 这儿我还是比较了解的."}, {"id": 60, "type": "reading_mc", "prompt": "60. 很多女孩子都希望自己能更瘦一些，所以常常不吃米饭和面条儿。这种做法很不健康。其实，只要多运动，少吃甜的东西，就不会发胖。\n★ 这段话主要想告诉我们：", "options": ["A 运动很危险", "B 怎么做才健康", "C 不吃米饭很好"], "answer": "B 怎么做才健康", "explanation": "Lời khuyên giảm cân khoa học."}, {"id": 61, "type": "reading_mc", "prompt": "61. 我在国外留学的时候，只要有时间，就会去当地人家里做客。在这期间，我认识了很多朋友，也更了解了那里的文化。\n★ 根据这段话，可以知道他：", "options": ["A 没留过学", "B 了解了当地文化", "C 喜欢打篮球"], "answer": "B 了解了当地文化", "explanation": "Hiểu biết văn hóa bản địa."}, {"id": 62, "type": "reading_mc", "prompt": "62. 昨天下了一天的大雪，今天天晴了。太阳出来了，照在白雪上，外面非常亮。虽然很冷，但是孩子们很高兴，在雪地上跑来跑去。\n★ 今天天气怎么样？", "options": ["A 在下雪", "B 阴天", "C 晴天"], "answer": "C 晴天", "explanation": "Hôm nay trời nắng: 今天天晴了."}, {"id": 63, "type": "reading_mc", "prompt": "63. 这家超市的东西不但便宜，而且质量非常好。每天都有很多人来这儿买东西，到了周末，人更多。\n★ 关于这家超市，可以知道什么？", "options": ["A 东西很贵", "B 周末人多", "C 地方很小"], "answer": "B 周末人多", "explanation": "Cuối tuần đông khách."}, {"id": 64, "type": "reading_mc", "prompt": "64. 我喜欢坐在窗户旁边，因为可以一边喝茶，一边看外面的风景。看着路上来来往往的人，我觉得很有趣。\n★ 他喜欢坐在哪儿？", "options": ["A 窗户旁边", "B 门旁边", "C 电视机前"], "answer": "A 窗户旁边", "explanation": "Thích ngồi bên cửa sổ."}, {"id": 65, "type": "reading_mc", "prompt": "65. 学汉语要多听、多说、多读、多写。每天坚持看半个小时的中文书，对提高汉语水平很有帮助。\n★ 怎样才能提高汉语水平？", "options": ["A 多睡觉", "B 坚持阅读", "C 少说话"], "answer": "B 坚持阅读", "explanation": "Kiên trì đọc sách mỗi ngày."}], "writing": [{"id": 71, "type": "reorder", "prompt": "71. ", "words": ["把", "手机", "送给", "她", "决定", "弟弟", "。"], "correct": "她决定把手机送给弟弟。"}, {"id": 72, "type": "reorder", "prompt": "72. ", "words": ["我和", "这个学生", "很久", "没见面了", "。"], "correct": "我和这个学生很久没见面了。"}, {"id": 73, "type": "reorder", "prompt": "73. ", "words": ["这个城市的", "春天", "经常", "刮风", "。"], "correct": "这个城市的春天经常刮风。"}, {"id": 74, "type": "reorder", "prompt": "74. ", "words": ["他的", "汉字", "写得", "很漂亮", "。"], "correct": "他的汉字写得很漂亮。"}, {"id": 75, "type": "reorder", "prompt": "75. ", "words": ["叔叔的", "太阳镜", "花了", "900块钱", "。"], "correct": "叔叔的太阳镜花了900块钱。"}, {"id": 76, "type": "char_fill", "prompt": "76. 那轮（ yuè ）亮又大又圆。", "correct": "月"}, {"id": 77, "type": "char_fill", "prompt": "77. 太阳就像一个（ bái ）色的盘子。", "correct": "白"}, {"id": 78, "type": "char_fill", "prompt": "78. 一（ qiān ）万年前，动物们出现了吗？", "correct": "千"}, {"id": 79, "type": "char_fill", "prompt": "79. 外面下雪了，你让孩子路上小（ xīn ）点儿。", "correct": "心"}, {"id": 80, "type": "char_fill", "prompt": "80. 生病了要注意休息，（ yīn ）为健康最重要。", "correct": "因"}]}, "H31008": {"title": "H31008", "audio_file": "H31008.mp3", "listening": [{"id": 1, "type": "listening_tf", "prompt": "1. ★ 他买了一瓶红酒。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：这瓶红酒多少钱？\n女：八十块。"}, {"id": 2, "type": "listening_tf", "prompt": "2. ★ 她在梳头发。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：帮我拿一下梳子，我的头发有点儿乱。\n男：好的，给你。"}, {"id": 3, "type": "listening_tf", "prompt": "3. ★ 桌子上有好多钱。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：手里拿了这么多硬币，去买什么呀？\n女：我去楼下买几份报纸。"}, {"id": 4, "type": "listening_tf", "prompt": "4. ★ 她去超市买新鲜蔬菜了。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：袋子里装的是什么？\n女：去超市买的一些新鲜蔬菜。"}, {"id": 5, "type": "listening_tf", "prompt": "5. ★ 房间里的灯坏了，需要换新的。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：洗手间的灯好像坏了，不亮了。\n男：我这儿有个新的灯泡，马上换上。"}, {"id": 6, "type": "listening_tf", "prompt": "6. ★ 蛋壳里长出了小草。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：你看这个蛋壳里长出的小草，多可爱啊！\n男：真有创意。"}, {"id": 7, "type": "listening_tf", "prompt": "7. ★ 他拿着行李箱准备去出差。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：票买好了吗？几点的飞机？\n女：下午两点，行李箱都收拾好了。"}, {"id": 8, "type": "listening_tf", "prompt": "8. ★ 这是一双小女孩儿穿的鞋。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：你看这双粉色的小鞋子，真漂亮。\n男：买下来送给姐姐的孩子吧。"}, {"id": 9, "type": "listening_tf", "prompt": "9. ★ 祝你生日快乐，这是送你的礼物。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：祝你生日快乐！打开看看喜不喜欢。\n女：谢谢你，我太开心了。"}, {"id": 10, "type": "listening_tf", "prompt": "10. ★ 他们在电脑前讨论工作。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：这个地方的数据你算得对吗？\n男：我再检查一遍电脑里的表格。"}, {"id": 11, "type": "listening_tf", "prompt": "11. ★ 果汁是刚买的。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "冰箱里的这瓶果汁已经放了一个星期了，不能喝了。"}, {"id": 12, "type": "listening_tf", "prompt": "12. ★ 老师多写了一个词语。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "请大家看黑板，这两个词语的意思是相同的。"}, {"id": 13, "type": "listening_tf", "prompt": "13. ★ 他孩子经常带糖去学校。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "我儿子特别爱吃糖，每天去学校口袋里都装几块糖。"}, {"id": 14, "type": "listening_tf", "prompt": "14. ★ 他们现在在电梯里。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "电梯坏了，我们还是走楼梯上去吧，一共才三层。"}, {"id": 15, "type": "listening_tf", "prompt": "15. ★ 今天的月亮很大。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "今天是农历八月十五，天上的月亮又圆又大。"}, {"id": 16, "type": "listening_tf", "prompt": "16. ★ 小鸡会游泳。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "河里有几只小鸭子在游泳，旁边的小鸡只能在岸上看。"}, {"id": 17, "type": "listening_tf", "prompt": "17. ★ 小王的丈夫爱看篮球比赛。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "小王的丈夫每天晚上都要看体育频道，特别爱看篮球。"}, {"id": 18, "type": "listening_tf", "prompt": "18. ★ 努力的人机会多。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "只要你努力工作，提高水平，机会总是会有的。"}, {"id": 19, "type": "listening_tf", "prompt": "19. ★ 葡萄不好吃。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "今天买的葡萄真甜，酸甜可口，大家都很喜欢。"}, {"id": 20, "type": "listening_tf", "prompt": "20. ★ 老刘喝酒容易脸红。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "老刘平时不怎么喝酒，只要喝一小杯脸就会红。"}, {"id": 21, "type": "listening_mc", "prompt": "21. 关于男的，可以知道什么？", "options": ["A 喜欢运动", "B 他不太饿", "C 想吃米饭"], "answer": "B 他不太饿", "script": "女：你再吃点儿米饭吧？\n男：不吃了，我今天不太饿。"}, {"id": 22, "type": "listening_mc", "prompt": "22. 女的提醒男的做什么？", "options": ["A 去看医生", "B 别去上班", "C 别忘关空调"], "answer": "C 别忘关空调", "script": "男：我出门了。\n女：走的时候别忘了关空调。"}, {"id": 23, "type": "listening_mc", "prompt": "23. 女的是什么意思？", "options": ["A 裤子短", "B 穿裤子好", "C 别穿旧裙子"], "answer": "B 穿裤子好", "script": "男：今天去爬山，我穿裙子好还是裤子好？\n女：山路不好走，穿裤子好。"}, {"id": 24, "type": "listening_mc", "prompt": "24. 图书馆在哪儿？", "options": ["A 楼后面", "B 教室旁边", "C 饭馆儿东边"], "answer": "A 楼后面", "script": "男：请问学校图书馆在哪儿？\n女：就在那栋教学楼的后面。"}, {"id": 25, "type": "listening_mc", "prompt": "25. 他们准备做什么？", "options": ["A 照相", "B 写信", "C 买手机"], "answer": "A 照相", "script": "女：这里风景真美，我们在这儿照张相吧。\n男：好啊，笑一笑。"}, {"id": 26, "type": "listening_mc", "prompt": "26. 他们最可能在什么地方？", "options": ["A 商店", "B 银行", "C 图书馆"], "answer": "B 银行", "script": "男：您好，我想把这些美元换成人民币。\n女：好的，请出示您的护照。"}, {"id": 27, "type": "listening_mc", "prompt": "27. 他们是什么关系？", "options": ["A 夫妻", "B 同事", "C 哥哥和妹妹"], "answer": "B 同事", "script": "女：下周经理出差，那份报告谁来做？\n男：经理让我和你一起完成。"}, {"id": 28, "type": "listening_mc", "prompt": "28. 发生什么事了？", "options": ["A 哭了", "B 生气了", "C 帽子被刮跑了"], "answer": "C 帽子被刮跑了", "script": "男：哎呀，外面风太大了！\n女：快看，你的帽子被风刮跑了！"}, {"id": 29, "type": "listening_mc", "prompt": "29. 他们要去哪儿散步？", "options": ["A 花园", "B 河边", "C 电影院"], "answer": "A 花园", "script": "女：晚饭后我们去哪儿走走？\n男：小区后面的小花园环境不错，去那儿吧。"}, {"id": 30, "type": "listening_mc", "prompt": "30. 男的打算做什么？", "options": ["A 还书", "B 打扫房间", "C 检查作业"], "answer": "A 还书", "script": "女：你拿着这些书要去哪儿？\n男：去图书馆还书，借期快到了。"}, {"id": 31, "type": "listening_mc", "prompt": "31. 男的怎么了？", "options": ["A 客人不满意", "B 护照不见了", "C 不认识路了"], "answer": "C 不认识路了", "script": "男：奇怪，我按照地图走，怎么找不到那家饭馆儿？\n女：你是不是走错方向了？我看看地图。\n男：对啊，我好像不认识路了。\n女：别急，问问路边的人吧。"}, {"id": 32, "type": "listening_mc", "prompt": "32. 他们现在在哪儿？", "options": ["A 超市", "B 地铁上", "C 出租车上"], "answer": "C 出租车上", "script": "女：师傅，请问到机场还要多久？\n男：路上有点儿堵车，大概还要半小时。\n女：好的，麻烦您尽量开快一点儿。\n男：放心吧。"}, {"id": 33, "type": "listening_mc", "prompt": "33. 弟弟怎么了？", "options": ["A 生病了", "B 跑得慢", "C 长得矮"], "answer": "B 跑得慢", "script": "女：你弟弟今天怎么没得第一名？\n男：他昨天脚扭了一下，今天跑得慢。\n女：原来是这样，没关系，健康第一。\n男：我也是这么跟他说的。"}, {"id": 34, "type": "listening_mc", "prompt": "34. 他们要在哪儿见面？", "options": ["A 公园", "B 机场", "C 办公室"], "answer": "A 公园", "script": "男：明天早上八点，我们在哪儿见？\n女：公园东门吧，那儿人少好找。\n男：行，那我骑自行车过去。\n女：明天见。"}, {"id": 35, "type": "listening_mc", "prompt": "35. 女的觉得那个蛋糕怎么样？", "options": ["A 很一般", "B 很好吃", "C 不太甜"], "answer": "B 很好吃", "script": "男：这个蛋糕是我妹妹自己做的，你尝尝。\n女：真不错！又香又甜，很好吃。\n男：喜欢就多吃一块儿。\n女：太好吃了，谢谢！"}], "reading": [{"id": 41, "type": "reading_mc", "prompt": "41. 上午的数学考试怎么样？", "options": ["A 真冷啊，把空调打开吧。", "B 先给我来一杯咖啡吧", "C 如果不下雪，我要去爬山", "D 还没看呢，洗完澡再看", "F 没问题，那些题都非常简单。"], "answer": "F 没问题，那些题都非常简单。", "explanation": "Hỏi về kỳ thi toán buổi sáng."}, {"id": 42, "type": "reading_mc", "prompt": "42. 先生，请问您喝点儿什么？", "options": ["A 真冷啊", "B 我等个朋友，先给我来一杯咖啡吧，谢谢。", "C 如果不下雪，我要去爬山", "D 还没看呢", "F 那些题非常简单"], "answer": "B 我等个朋友，先给我来一杯咖啡吧，谢谢。", "explanation": "Gọi đồ uống cà phê."}, {"id": 43, "type": "reading_mc", "prompt": "43. 这个周末你打算做什么？", "options": ["A 真冷啊", "B 来一杯咖啡", "C 如果不下雪，我要和同学们去爬山。", "D 还没看呢", "F 那些题非常简单"], "answer": "C 如果不下雪，我要和同学们去爬山。", "explanation": "Kế hoạch cuối tuần đi leo núi."}, {"id": 44, "type": "reading_mc", "prompt": "44. 报纸上有什么新闻吗？", "options": ["A 真冷啊", "B 来一杯咖啡", "C 去爬山", "D 还没看呢，我洗完澡再看。", "F 那些题非常简单"], "answer": "D 还没看呢，我洗完澡再看。", "explanation": "Hỏi về tin tức trên báo."}, {"id": 45, "type": "reading_mc", "prompt": "45. 你衣服穿得太少了，是不是感冒了？", "options": ["A 真冷啊，把空调打开吧。", "B 来一杯咖啡", "C 去爬山", "D 还没看呢", "F 那些题非常简单"], "answer": "A 真冷啊，把空调打开吧。", "explanation": "Nói về thời tiết lạnh/bật điều hòa."}, {"id": 46, "type": "reading_mc", "prompt": "46. 没关系，我吃过药了。", "options": ["A 我记得你弟弟以前特别胖。", "B 祝您生日快乐！", "C 今天我来洗碗", "D 你不舒服吗？需不需要去房间休息一下？", "E 在外面注意身体"], "answer": "D 你不舒服吗？需不需要去房间休息一下？", "explanation": "Hỏi thăm sức khỏe, người kia trả lời đã uống thuốc."}, {"id": 47, "type": "reading_mc", "prompt": "47. 他从去年秋天开始锻炼，现在不到 70 公斤。", "options": ["A 我记得你弟弟以前特别胖。", "B 祝您生日快乐！", "C 今天我来洗碗", "D 需不需要去房间休息", "E 在外面注意身体"], "answer": "A 我记得你弟弟以前特别胖。", "explanation": "Nói về tập luyện giảm cân so với lúc trước."}, {"id": 48, "type": "reading_mc", "prompt": "48. 好，我会给你打电话或者写电子邮件的。", "options": ["A 特别胖", "B 祝您生日快乐！", "C 今天我来洗碗", "D 需不需要去房间休息", "E 明天就要出国了？在外面注意身体，照顾好自己。"], "answer": "E 明天就要出国了？在外面注意身体，照顾好自己。", "explanation": "Lời dặn khi chuẩn bị xuất ngoại."}, {"id": 49, "type": "reading_mc", "prompt": "49. 不用，你把筷子和杯子拿过来就可以了。", "options": ["A 特别胖", "B 祝您生日快乐！", "C 今天我来洗碗，你累一天了，去看电视吧。", "D 需不需要去房间休息", "E 在外面注意身体"], "answer": "C 今天我来洗碗，你累一天了，去看电视吧。", "explanation": "Tranh rửa bát, làm việc nhà."}, {"id": 50, "type": "reading_mc", "prompt": "50. 大家来吃蛋糕吧，这块儿大的给你。", "options": ["A 特别胖", "B 祝您生日快乐！这是我送您的礼物。", "C 今天我来洗碗", "D 需不需要去房间休息", "E 在外面注意身体"], "answer": "B 祝您生日快乐！这是我送您的礼物。", "explanation": "Tặng quà chúc mừng sinh nhật và ăn bánh."}, {"id": 51, "type": "fill_gap", "prompt": "51. 这个城市有几百年的（     ）了。", "options": ["A 聪明", "B 几乎", "C 解决", "D 历史", "E 关系"], "answer": "D 历史", "explanation": "Từ cần điền: 历史 (lịch sử)."}, {"id": 52, "type": "fill_gap", "prompt": "52. 儿子长大了，都快一米八了，（     ）和他爸爸一样高了。", "options": ["A 聪明", "B 几乎", "C 解决", "D 历史", "E 关系"], "answer": "B 几乎", "explanation": "Từ cần điền: 几乎 (hầu như, gần như)."}, {"id": 53, "type": "fill_gap", "prompt": "53. 小黄是我的好朋友，她和我的（     ）一直很好。", "options": ["A 聪明", "B 几乎", "C 解决", "D 历史", "E 关系"], "answer": "E 关系", "explanation": "Từ cần điền: 关系 (mối quan hệ)."}, {"id": 54, "type": "fill_gap", "prompt": "54. 多吃鱼会使人变得更（     ）。", "options": ["A 聪明", "B 几乎", "C 解决", "D 历史", "E 关系"], "answer": "A 聪明", "explanation": "Từ cần điền: 聪明 (thông minh)."}, {"id": 55, "type": "fill_gap", "prompt": "55. 我们已经找到（     ）问题的办法了。", "options": ["A 聪明", "B 几乎", "C 解决", "D 历史", "E 关系"], "answer": "C 解决", "explanation": "Từ cần điền: 解决 (giải quyết)."}, {"id": 56, "type": "fill_gap", "prompt": "56. A：你（     ）的这是猫？\nB：大熊猫！它在爬树。这也看不懂？", "options": ["A 画", "B 简单", "C 选择", "D 结婚", "E 马上"], "answer": "A 画", "explanation": "Từ cần điền: 画 (vẽ tranh)."}, {"id": 57, "type": "fill_gap", "prompt": "57. A：你低着头想什么呢？\nB：是工作还是读书，我不知道应该怎么（     ）才好。", "options": ["A 画", "B 简单", "C 选择", "D 结婚", "E 马上"], "answer": "C 选择", "explanation": "Từ cần điền: 选择 (lựa chọn)."}, {"id": 58, "type": "fill_gap", "prompt": "58. A：你渴不？我想去买点儿水。\nB：那你快一点儿，表演（     ）就要开始了。", "options": ["A 画", "B 简单", "C 选择", "D 结婚", "E 马上"], "answer": "E 马上", "explanation": "Từ cần điền: 马上 (ngay lập tức)."}, {"id": 59, "type": "fill_gap", "prompt": "59. A：相信我，这件事对公司不会有影响的。\nB：夏经理，你把事情想得太（     ）了。", "options": ["A 画", "B 简单", "C 选择", "D 结婚", "E 马上"], "answer": "B 简单", "explanation": "Từ cần điền: 简单 (đơn giản)."}, {"id": 60, "type": "fill_gap", "prompt": "60. A：好久没看见白老师了，他不在这儿住了？\nB：是，他（     ）以后就和妻子搬到学校去住了。", "options": ["A 画", "B 简单", "C 选择", "D 结婚", "E 马上"], "answer": "D 结婚", "explanation": "Từ cần điền: 结婚 (kết hôn)."}, {"id": 61, "type": "reading_mc", "prompt": "61. 最近几年，这里的变化很大，车辆更多了，街道更干净了，天更蓝了，树更绿了。\n★ 这里最近几年怎么样？", "options": ["A 环境变好了", "B 和过去相同", "C 变得更差了"], "answer": "A 环境变好了", "explanation": "Đoạn văn: 街道更干净了，天更蓝了."}, {"id": 62, "type": "reading_mc", "prompt": "62. 人们根据季节的变化来决定喝什么茶。老人们经常说：“春天最好喝花茶，冬天最好喝红茶。”\n★ 这段话告诉我们：", "options": ["A 茶有什么作用", "B 老人爱喝红茶", "C 不同季节喝不同的茶"], "answer": "C 不同季节喝不同的茶", "explanation": "Đoạn văn: 根据季节的变化来决定喝什么茶."}, {"id": 63, "type": "reading_mc", "prompt": "63. 汉字有多少个？这个问题谁也回答不清楚，《汉语大字典》里有五六万字，普通的小字典，一本也有八九千字。但人们常用的也就两千多个，认识这两千多个字，读书看报就没什么问题了。\n★ 这段话的主要意思是：", "options": ["A 汉字很难写", "B 要学会查字典", "C 常用汉字不多"], "answer": "C 常用汉字不多", "explanation": "Đoạn văn: 但人们常用的也就两千多个."}, {"id": 64, "type": "reading_mc", "prompt": "64. 为什么很多人愿意在网上买东西呢？因为非常方便，而且还便宜，如果对买到的东西有不满意的地方，也可以要求换新的。\n★ 在网上买东西：", "options": ["A 比较贵", "B 花钱少", "C 花的时间多"], "answer": "B 花钱少", "explanation": "Đoạn văn: 而且还便宜 (chi tiêu ít tiền hơn)."}, {"id": 65, "type": "reading_mc", "prompt": "65. 儿子的作业总是做错，但昨天的一个也没错。老师问：“有人帮你写作业了？”“没有，我爸爸昨天没时间，我想我应该自己完成了。”\n★ 儿子昨天的作业为什么没错？", "options": ["A 自己做的", "B 爸爸帮忙了", "C 认真复习了"], "answer": "A 自己做的", "explanation": "Đoạn văn: 我想我应该自己完成了."}], "writing": [{"id": 71, "type": "reorder", "prompt": "71. ", "words": ["那", "邻居", "很热情", "位", "。"], "correct": "那位邻居很热情。"}, {"id": 72, "type": "reorder", "prompt": "72. ", "words": ["这个", "三层", "一共", "楼", "。"], "correct": "这个楼一共三层。"}, {"id": 73, "type": "reorder", "prompt": "73. ", "words": ["菜单", "服务员", "拿走了", "被", "。"], "correct": "菜单被服务员拿走了。"}, {"id": 74, "type": "reorder", "prompt": "74. ", "words": ["比", "北方", "中国南方的雨水", "多", "。"], "correct": "中国南方的雨水比北方多。"}, {"id": 75, "type": "reorder", "prompt": "75. ", "words": ["把", "厨房里", "吧", "冰箱", "放", "。"], "correct": "把冰箱放厨房里吧。"}, {"id": 76, "type": "char_fill", "prompt": "76. 你姐姐的孩子上（ jǐ ）年级？", "correct": "几"}, {"id": 77, "type": "char_fill", "prompt": "77. 马小姐，谢谢关（ xīn ），我不发烧了，头也不疼了。", "correct": "心"}, {"id": 78, "type": "char_fill", "prompt": "78. 对不起，（ xià ）午有个重要的会议，我让司机去医院接你好不好？", "correct": "下"}, {"id": 79, "type": "char_fill", "prompt": "79. 经过4个星期的练习，叔叔的普通话水平有了很（ dà ）提高。", "correct": "大"}, {"id": 80, "type": "char_fill", "prompt": "80. 这个小太阳表示晴天，（ yún ）表示阴天。", "correct": "云"}]}, "H31111": {"title": "H31111", "audio_file": "H31111.mp3", "listening": [{"id": 1, "type": "listening_tf", "prompt": "1. ★ 下雨了，出门记得带伞。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：外面阴天了，好像要下雨。\n男：那你出门的时候记得带把雨伞。"}, {"id": 2, "type": "listening_tf", "prompt": "2. ★ 这只熊猫特别喜欢吃竹子。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：你看这只大熊猫，吃竹子吃得多香啊！\n女：是啊，真可爱。"}, {"id": 3, "type": "listening_tf", "prompt": "3. ★ 天气太热，太阳很大。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：今天太阳真大，外面热极了。\n男：我们快进屋吹空调吧。"}, {"id": 4, "type": "listening_tf", "prompt": "4. ★ 他们正在搬家呢。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：箱子太重了，我来帮你抬椅子。\n女：谢谢你，搬家可真累。"}, {"id": 5, "type": "listening_tf", "prompt": "5. ★ 医生正在看病历呢。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：医生，请问我的检查结果出来了吗？\n男：请稍等，我看一下病历。"}, {"id": 6, "type": "listening_tf", "prompt": "6. ★ 他们在饭馆儿点菜呢。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：服务员，请给我们拿一下菜单。\n女：好的，请问几位喝点儿什么？"}, {"id": 7, "type": "listening_tf", "prompt": "7. ★ 孩子发烧了，要量体温。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：孩子额头有点儿烫，量体温了吗？\n男：量过了，三十八度五，发烧了。"}, {"id": 8, "type": "listening_tf", "prompt": "8. ★ 他在收拾行李准备出发。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：衣服都装进行李箱了吗？\n女：都收拾好了，准备出发吧。"}, {"id": 9, "type": "listening_tf", "prompt": "9. ★ 两人在车站握手告别。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "女：很高兴能和您合作，祝您一路平安！\n男：谢谢您，下次北京见。"}, {"id": 10, "type": "listening_tf", "prompt": "10. ★ 姐姐在镜子前试新衣服。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "男：这件黑色的裙子你穿真好看！\n女：我也觉得挺合适的，很漂亮。"}, {"id": 11, "type": "listening_tf", "prompt": "11. ★ 校长还认识他。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "没想到过了这么多年，校长依然能一眼认出他，叫出他的名字。"}, {"id": 12, "type": "listening_tf", "prompt": "12. ★ 现在的书比以前的贵。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "去书店买了几本新书，现在的书确实比以前贵了不少。"}, {"id": 13, "type": "listening_tf", "prompt": "13. ★ 他对这个运动没有兴趣。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "足球是他最喜欢的体育运动，只要有比赛他都会看。"}, {"id": 14, "type": "listening_tf", "prompt": "14. ★ 他们在想办法。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "这件事情已经顺利解决了，大家都不用再操心了。"}, {"id": 15, "type": "listening_tf", "prompt": "15. ★ 那个学生想参加比赛。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "王老师，这次汉语演讲比赛我也想报名参加，可以吗？"}, {"id": 16, "type": "listening_tf", "prompt": "16. ★ 他忘了同学的生日。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "明天是小李的生日，我早在一个星期前就给他挑好了生日礼物。"}, {"id": 17, "type": "listening_tf", "prompt": "17. ★ 黄经理很着急。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "黄经理在办公室走来走去，会议马上就要开始了，材料还没送来。"}, {"id": 18, "type": "listening_tf", "prompt": "18. ★ 那位司机没什么爱好。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "那位出租车司机不仅车开得好，平时还特别喜欢唱歌和听京剧。"}, {"id": 19, "type": "listening_tf", "prompt": "19. ★ 小晴正在画画儿。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Đúng (√)", "script": "别去打扰小晴，她正拿着画笔认真地画大熊猫呢。"}, {"id": 20, "type": "listening_tf", "prompt": "20. ★ 那条狗走在他前面。", "options": ["Đúng (√)", "Sai (×)"], "answer": "Sai (×)", "script": "散步的时候，小狗总是乖乖地跟在主人的后面。"}, {"id": 21, "type": "listening_mc", "prompt": "21. 男的想喝什么？", "options": ["A 茶", "B 啤酒", "C 西瓜汁"], "answer": "C 西瓜汁", "script": "女：天气这么热，你想喝点儿什么？有茶和啤酒。\n男：给我来一杯新鲜的西瓜汁吧，解解渴。"}, {"id": 22, "type": "listening_mc", "prompt": "22. 他们在哪儿见面？", "options": ["A 西门", "B 机场", "C 办公室"], "answer": "A 西门", "script": "男：到了学校我们在哪儿碰头？\n女：就在学校西门门口吧，那儿标志明显。"}, {"id": 23, "type": "listening_mc", "prompt": "23. 关于男的，可以知道什么？", "options": ["A 正在上班", "B 有女朋友了", "C 同意现在去"], "answer": "B 有女朋友了", "script": "女：你弟弟结婚了吗？有对象了吗？\n男：刚谈了一个女朋友，人很不错。"}, {"id": 24, "type": "listening_mc", "prompt": "24. 他们在看什么？", "options": ["A 照片", "B 电视", "C 报纸"], "answer": "A 照片", "script": "男：这张照得多好看啊，笑得多甜！\n女：是啊，这是去年旅游时照的照片。"}, {"id": 25, "type": "listening_mc", "prompt": "25. 他们最可能在什么地方？", "options": ["A 教室", "B 超市", "C 图书馆"], "answer": "B 超市", "script": "女：你看这个推车里装的面包和水果够不够？\n男：再去买两袋牛奶，然后去结账吧。"}, {"id": 26, "type": "listening_mc", "prompt": "26. 关于女的，可以知道什么？", "options": ["A 马上就到", "B 是服务员", "C 在公共汽车上"], "answer": "A 马上就到", "script": "男：你到哪儿了？大家都在等你呢。\n女：别急，我已经到楼下了，马上就到！"}, {"id": 27, "type": "listening_mc", "prompt": "27. 女的怎么了？", "options": ["A 口渴了", "B 生病了", "C 害怕吃药"], "answer": "B 生病了", "script": "男：看你脸色不太好，怎么了？\n女：头疼发烧，好像生病了。"}, {"id": 28, "type": "listening_mc", "prompt": "28. 妹妹叫什么名字？", "options": ["A 甜甜", "B 双双", "C 笑笑"], "answer": "A 甜甜", "script": "男：你家两个女儿，小的那个叫什么来着？\n女：大女儿叫双双，小女儿叫甜甜。"}, {"id": 29, "type": "listening_mc", "prompt": "29. 关于同事，可以知道什么？", "options": ["A 都很年轻", "B 工作认真", "C 很关心他"], "answer": "C 很关心他", "script": "女：新公司的人怎么样？\n男：同事们都非常热情，平时都很关心我。"}, {"id": 30, "type": "listening_mc", "prompt": "30. 关于汉语考试，可以知道什么？", "options": ["A 已经考完了", "B 昨天考汉语", "C 比别人考得好"], "answer": "A 已经考完了", "script": "女：汉语三级考试准备得怎么样了？\n男：今天上午刚考完，感觉还不错。"}, {"id": 31, "type": "listening_mc", "prompt": "31. 那个表演怎么样？", "options": ["A 不好", "B 一般", "C 非常好"], "answer": "C 非常好", "script": "男：昨晚学校举行的文艺表演你看了吗？\n女：看了，特别是那个音乐节目，演得非常好！\n男：我也觉得水平很高。\n女：大家都鼓掌了。"}, {"id": 32, "type": "listening_mc", "prompt": "32. 女的买了什么水果？", "options": ["A 香蕉", "B 葡萄", "C 苹果"], "answer": "A 香蕉", "script": "男：你买水果回来了？买了什么？\n女：超市里的香蕉很新鲜，我买了一大把。\n男：苹果没买吗？\n女：苹果不太新鲜，就只买了香蕉。"}, {"id": 33, "type": "listening_mc", "prompt": "33. 他们在谈论什么？", "options": ["A 节日", "B 汉字", "C 菜单"], "answer": "B 汉字", "script": "女：这个词语你写得真漂亮，是哪个字？\n男：这是春天的“春”，我练了很久。\n女：中国汉字真有意思。\n男：是啊，结构很特别。"}, {"id": 34, "type": "listening_mc", "prompt": "34. 他们现在在哪儿？", "options": ["A 饿了", "B 在河边", "C 走不动了"], "answer": "B 在河边", "script": "男：外面的风景真不错，微风吹着真舒服。\n女：是啊，沿着河边散散步，心情好多了。\n男：看，河里还有小鱼游来游去呢。\n女：真漂亮。"}, {"id": 35, "type": "listening_mc", "prompt": "35. 女的现在在哪儿？", "options": ["A 快到家了", "B 在洗手间", "C 在跳舞呢"], "answer": "A 快到家了", "script": "男：喂，你下班了吗？什么时候回来做饭？\n女：我已经下地铁了，现在在走回小区的路上，快到家了。\n男：好，那我先把米饭煮上。\n女：好的，五分钟后见。"}], "reading": [{"id": 41, "type": "reading_mc", "prompt": "41. 这个城市每条街道都很干净。", "options": ["A 那儿的环境很好，天总是蓝的。", "B 你这次去中国打算玩儿多久？", "C 很简单，一定是你拿错了。", "D 奇怪，会议室的灯怎么没关？", "F 做蛋糕的时候，除了放鸡蛋外，还可以再放些牛奶。"], "answer": "A 那儿的环境很好，天总是蓝的。", "explanation": "Khen ngợi môi trường thành phố sạch đẹp, không khí trong lành."}, {"id": 42, "type": "reading_mc", "prompt": "42. 回到家，才发现行李箱里有一件白衬衫不是我的。", "options": ["A 那儿的环境很好", "B 打算玩儿多久", "C 很简单，一定是你拿错了。", "D 奇怪，灯怎么没关", "F 做蛋糕的时候"], "answer": "C 很简单，一定是你拿错了。", "explanation": "Đáp lại việc cầm nhầm áo sơ mi trong hành lý."}, {"id": 43, "type": "reading_mc", "prompt": "43. 对不起，我以为你们一会儿还要回去。", "options": ["A 那儿的环境很好", "B 打算玩儿多久", "C 一定是你拿错了", "D 奇怪，会议室的灯怎么没关？", "F 做蛋糕的时候"], "answer": "D 奇怪，会议室的灯怎么没关？", "explanation": "Giải thích lý do chưa tắt đèn phòng họp."}, {"id": 44, "type": "reading_mc", "prompt": "44. 我 16 号去，29 号回来。", "options": ["A 那儿的环境很好", "B 你这次去中国打算玩儿多久？", "C 一定是你拿错了", "D 奇怪，灯怎么没关", "F 做蛋糕的时候"], "answer": "B 你这次去中国打算玩儿多久？", "explanation": "Trả lời câu hỏi về thời gian đi du lịch Trung Quốc."}, {"id": 45, "type": "reading_mc", "prompt": "45. 我知道，奶奶以前教过我。", "options": ["A 那儿的环境很好", "B 打算玩儿多久", "C 一定是你拿错了", "D 奇怪，灯怎么没关", "F 做蛋糕的时候，除了放鸡蛋外，还可以再放些牛奶。"], "answer": "F 做蛋糕的时候，除了放鸡蛋外，还可以再放些牛奶。", "explanation": "Đáp lại kinh nghiệm làm bánh ngọt."}, {"id": 46, "type": "reading_mc", "prompt": "46. 你们去旅游，那小狗谁来照顾？", "options": ["A 我希望早点儿离开", "B 告诉外面天阴了", "C 这是个坏习惯", "D 放心吧，我们跟邻居说了，他们很愿意帮忙。", "E 主要是他最近身体不好"], "answer": "D 放心吧，我们跟邻居说了，他们很愿意帮忙。", "explanation": "Nhờ hàng xóm chăm sóc chó cưng khi đi du lịch."}, {"id": 47, "type": "reading_mc", "prompt": "47. 如果没什么变化，他应该已经上飞机了。", "options": ["A 我希望早点儿离开这个国家。", "B 外面天阴了", "C 这是个坏习惯", "D 邻居很愿意帮忙", "E 影响了学习"], "answer": "A 我希望早点儿离开这个国家。", "explanation": "Liên quan đến việc lên máy bay rời đi."}, {"id": 48, "type": "reading_mc", "prompt": "48. 晚上不要吃得太多，太饱，那样睡觉会不舒服。", "options": ["A 希望早点儿离开", "B 外面天阴了", "C 我明白，这是个坏习惯。", "D 邻居很愿意帮忙", "E 影响了学习"], "answer": "C 我明白，这是个坏习惯。", "explanation": "Thừa nhận thói quen ăn quá no buổi tối là không tốt."}, {"id": 49, "type": "reading_mc", "prompt": "49. 历史考试没考好，是题太难吗？", "options": ["A 希望早点儿离开", "B 外面天阴了", "C 这是个坏习惯", "D 邻居很愿意帮忙", "E 主要是他最近身体不好，影响了学习。"], "answer": "E 主要是他最近身体不好，影响了学习。", "explanation": "Giải thích nguyên nhân thi không tốt do sức khỏe kém."}, {"id": 50, "type": "reading_mc", "prompt": "50. 我刚才洗澡去了，有事吗？", "options": ["A 希望早点儿离开", "B 没什么，就是告诉你外面天阴了，可能要下雪。", "C 这是个坏习惯", "D 邻居很愿意帮忙", "E 影响了学习"], "answer": "B 没什么，就是告诉你外面天阴了，可能要下雪。", "explanation": "Báo tin thời tiết râm mát, sắp có tuyết rơi."}, {"id": 51, "type": "fill_gap", "prompt": "51. 北方人爱吃（     ），南方人喜欢吃米饭。", "options": ["A 终于", "B 水平", "C 面条儿", "D 结婚", "E 了解"], "answer": "C 面条儿", "explanation": "Từ cần điền: 面条儿 (mì sợi)."}, {"id": 52, "type": "fill_gap", "prompt": "52. 坐了 7 个小时的火车，我们（     ）到北京了。", "options": ["A 终于", "B 水平", "C 面条儿", "D 结婚", "E 了解"], "answer": "A 终于", "explanation": "Từ cần điền: 终于 (cuối cùng)."}, {"id": 53, "type": "fill_gap", "prompt": "53. 他们准备 8 月（     ）。", "options": ["A 终于", "B 水平", "C 面条儿", "D 结婚", "E 了解"], "answer": "D 结婚", "explanation": "Từ cần điền: 结婚 (kết hôn)."}, {"id": 54, "type": "fill_gap", "prompt": "54. 看了好几个节目，我觉得三年级二班的（     ）最高。", "options": ["A 终于", "B 水平", "C 面条儿", "D 结婚", "E 了解"], "answer": "B 水平", "explanation": "Từ cần điền: 水平 (trình độ)."}, {"id": 55, "type": "fill_gap", "prompt": "55. 你应该先（     ）事情的经过，然后再想怎么解决问题。", "options": ["A 终于", "B 水平", "C 面条儿", "D 结婚", "E 了解"], "answer": "E 了解", "explanation": "Từ cần điền: 了解 (tìm hiểu, hiểu rõ)."}, {"id": 56, "type": "fill_gap", "prompt": "56. A：我到你们公司楼下了，你在几（     ）？\nB：你等一下，我下来接你。", "options": ["A 结束", "B 方便", "C 层", "D 当然", "E 一直"], "answer": "C 层", "explanation": "Từ cần điền: 层 (tầng nhà)."}, {"id": 57, "type": "fill_gap", "prompt": "57. A：船票我买到了，记得来送我。\nB：等表演一（     ）我就去找你。", "options": ["A 结束", "B 方便", "C 层", "D 当然", "E 一直"], "answer": "A 结束", "explanation": "Từ cần điền: 结束 (kết thúc)."}, {"id": 58, "type": "fill_gap", "prompt": "58. A：我周末想去动物园，你知道怎么去吗？\nB：坐 405 路就能到。骑自行车去可能更（     ）。", "options": ["A 结束", "B 方便", "C 层", "D 当然", "E 一直"], "answer": "B 方便", "explanation": "Từ cần điền: 方便 (tiện lợi)."}, {"id": 59, "type": "fill_gap", "prompt": "59. A：火车站附近有宾馆吗？\nB：（     ）有，我第一次来的时候就住前面那个宾馆。", "options": ["A 结束", "B 方便", "C 层", "D 当然", "E 一直"], "answer": "D 当然", "explanation": "Từ cần điền: 当然 (đương nhiên)."}, {"id": 60, "type": "fill_gap", "prompt": "60. A：小马，你好久没来打篮球了。\nB：最近（     ）忙着找工作，没时间玩儿。", "options": ["A 结束", "B 方便", "C 层", "D 当然", "E 一直"], "answer": "E 一直", "explanation": "Từ cần điền: 一直 (luôn/suốt)."}, {"id": 61, "type": "reading_mc", "prompt": "61. 昨天，我送给妻子一个礼物，是一辆红色的汽车，她高兴极了。妻子的那辆旧车开了六七年了，早就应该换了。\n★ 妻子为什么很高兴？", "options": ["A 搬新家了", "B 换了辆新车", "C 把旧车卖了"], "answer": "B 换了辆新车", "explanation": "Được tặng xe ô tô mới thay cho xe cũ."}, {"id": 62, "type": "reading_mc", "prompt": "62. 那个饭馆儿虽然不大，但是菜做得很好吃，而且不贵。很多新客人变成了老客人，老客人又带来更多新客人。\n★ 根据这段话，那家饭馆儿：", "options": ["A 菜便宜", "B 很安静", "C 客人少"], "answer": "A 菜便宜", "explanation": "Đoạn văn nêu rõ: 菜做得很好吃，而且不贵 (giá rẻ)."}, {"id": 63, "type": "reading_mc", "prompt": "63. 为了变得瘦一些，妹妹决定每天早上去跑步。开始的几天，她每天能跑三千米，很努力。但是慢慢地，跑得越来越短，现在每天能跑 500 米就不错了。\n★ 根据这段话，妹妹现在：", "options": ["A 变黑了", "B 不胖了", "C 天天跑步"], "answer": "C 天天跑步", "explanation": "Vẫn duy trì chạy mỗi ngày dù cự ly ngắn hơn."}, {"id": 64, "type": "reading_mc", "prompt": "64. 她看那个电影的时候哭了，因为电影里的故事让她想起了很多年以前的一些事情，想起了很多以前的朋友。\n★ 关于这个电影，可以知道什么？", "options": ["A 很有名", "B 让她很难过", "C 没什么意思"], "answer": "B 让她很难过", "explanation": "Phim làm cô ấy xúc động rơi nước mắt."}, {"id": 65, "type": "reading_mc", "prompt": "65. 小云，我给你介绍个男朋友吧？是我先生的弟弟，人很聪明，在银行工作，找机会你们见个面怎么样？\n★ 她想为小云：", "options": ["A 办护照", "B 介绍工作", "C 介绍男朋友"], "answer": "C 介绍男朋友", "explanation": "Đoạn văn: 我给你介绍个男朋友吧."}], "writing": [{"id": 71, "type": "reorder", "prompt": "71. ", "words": ["左阿姨", "讲", "普通话", "不会", "。"], "correct": "左阿姨不会讲普通话。"}, {"id": 72, "type": "reorder", "prompt": "72. ", "words": ["面包", "18 块", "这些", "一共", "。"], "correct": "这些面包一共 18 块。"}, {"id": 73, "type": "reorder", "prompt": "73. ", "words": ["完成", "了", "你的作业", "吗", "？"], "correct": "你的作业完成了吗？"}, {"id": 74, "type": "reorder", "prompt": "74. ", "words": ["成绩", "我女儿的", "非常好", "数学", "。"], "correct": "我女儿的数学成绩非常好。"}, {"id": 75, "type": "reorder", "prompt": "75. ", "words": ["她", "放进了", "叔叔的包里", "把", "信", "。"], "correct": "她把信放进了叔叔的包里。"}, {"id": 76, "type": "char_fill", "prompt": "76. 再见，欢迎您（ xià ）次再来。", "correct": "下"}, {"id": 77, "type": "char_fill", "prompt": "77. 男朋友的（ huí ）答，让她特别高兴。", "correct": "回"}, {"id": 78, "type": "char_fill", "prompt": "78. 对猫来说，小鱼（ bǐ ）羊肉更好吃。", "correct": "比"}, {"id": 79, "type": "char_fill", "prompt": "79. 你把空调打开吧，房间里（ tài ）热了。", "correct": "太"}, {"id": 80, "type": "char_fill", "prompt": "80. 爷爷，您今（ tiān ）买的葡萄真新鲜，非常好吃。", "correct": "天"}]}}

@st.cache_data
def load_exam_data():
    return EXAM_DATA

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

    cols = st.columns(3)
    pastel_colors = ["#E8F0FE", "#E6F4EA", "#FCE8E6"]
    border_colors = ["#1A365D", "#137333", "#C5221F"]

    for idx, code in enumerate(exam_codes):
        with cols[idx % 3]:
            p_bg = pastel_colors[idx % len(pastel_colors)]
            p_border = border_colors[idx % len(border_colors)]
            
            st.markdown(f'''
            <div style="background-color: {p_bg}; border: 3px solid {p_border}; border-radius: 14px; padding: 25px 15px; text-align: center; margin-bottom: 15px;">
                <div style="font-size: 32px; font-weight: bold; color: {p_border}; font-family: 'Tahoma', sans-serif;">{code}</div>
            </div>
            ''', unsafe_allow_html=True)

            if st.button(f"👉 Vào làm đề {code}", key=f"btn_{code}", use_container_width=True):
                if not st.session_state.student_name.strip():
                    st.error("⚠️ Vui lòng nhập Họ và tên trước khi vào thi!")
                elif not st.session_state.class_name.strip():
                    st.error("⚠️ Vui lòng nhập Tên lớp trước khi vào thi!")
                else:
                    st.session_state.selected_exam = code
                    st.rerun()

    st.markdown("<div class='teacher-footer'>黄宝玉老师</div>", unsafe_allow_html=True)

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

def render_section_tab(exam_code, section_key, section_title, questions, max_time_sec, audio_file=None):
    st.subheader(f"📌 {section_title}")

    section_id = f"{exam_code}_{section_key}"
    is_submitted = st.session_state.submitted_sections.get(section_id, False)

    start_time = st.session_state.exam_start_times[exam_code][section_key]
    elapsed = time.time() - start_time
    remaining_sec = max(0, int(max_time_sec - elapsed))

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
        
        if q["prompt"]:
            st.markdown(f"<span class='chinese-text' style='font-size:19px; font-weight:bold;'>{q['prompt']}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"**Câu {q_id}:**", unsafe_allow_html=True)

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

        student_name_val = st.session_state.student_name
        st.markdown(f"""
        <div class="congrats-banner">
            <h3 style="color: #2B6CB0; margin-bottom: 10px;">🎉 Chúc mừng <b>"{student_name_val}"</b> đã hoàn thành đề <b>"{exam_code}"</b> ({section_title})</h3>
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
