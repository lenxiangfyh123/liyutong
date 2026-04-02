import streamlit as st
import random
import re

# 页面配置
st.set_page_config(
    page_title="🐢 海龟汤 - 问答互动版",
    page_icon="🐢",
    layout="centered"
)

# 自定义样式
st.markdown("""
<style>
.stTitle {
    color: #2E86C1;
    text-align: center;
}
.game-box {
    background-color: #F8F9F9;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #2E86C1;
    margin: 20px 0;
}
.clue-box {
    background-color: #FEF9E7;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #F39C12;
    margin: 10px 0;
}
.answer-box {
    background-color: #D5F5E3;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #27AE60;
    margin: 10px 0;
}
.question-box {
    background-color: #EBF5FB;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #3498DB;
    margin: 10px 0;
}
.answer-yes {
    background-color: #D5F5E3;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #27AE60;
    margin: 10px 0;
}
.answer-no {
    background-color: #FADBD8;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #E74C3C;
    margin: 10px 0;
}
.answer-related {
    background-color: #FEF9E7;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #F39C12;
    margin: 10px 0;
}
.answer-unrelated {
    background-color: #F4ECF7;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #8E44AD;
    margin: 10px 0;
}
.chat-history {
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid #ddd;
    padding: 10px;
    border-radius: 8px;
    background-color: #FAFAFA;
}
</style>
""", unsafe_allow_html=True)

# 海龟汤题目数据库（包含关键词和答案逻辑）
stories = [
    {
        "title": "经典的海龟汤",
        "difficulty": "⭐⭐",
        "story": "一个男人走进一家餐厅，点了一碗海龟汤。他喝了一口后，突然脸色大变，立刻冲出餐厅，回到家后就自杀了。为什么？",
        "answer": "这个男人曾经和妻子一起遭遇海难，漂流到一个荒岛上。妻子不幸去世，其他幸存者告诉他说，他们找到了食物（海龟汤）才救了他。他一直以为是海龟汤救了自己。直到今天在餐厅喝了真正的海龟汤，才发现味道完全不同。他瞬间明白，当年在荒岛上吃的'海龟汤'其实是...他妻子的肉。无法承受这个真相的他选择了自杀。",
        "keywords": {
            "海难": True,
            "荒岛": True,
            "妻子": True,
            "幸存者": True,
            "人肉": True,
            "味道": True,
            "回忆": True,
            "过去": True,
            "灾难": True,
            "死亡": True,
            "自杀": True,
            "餐厅": False,
            "厨师": False,
            "价格": False,
            "服务": False
        },
        "key_facts": [
            "男人以前经历过灾难",
            "他和妻子一起遇难",
            "妻子在荒岛上去世了",
            "他在荒岛上吃了东西",
            "他以为吃的是海龟",
            "实际上吃的不是海龟",
            "他吃的是人肉",
            "他吃的是妻子的肉",
            "今天的海龟汤味道不对",
            "他意识到了真相",
            "他无法接受真相"
        ],
        "yes_questions": [
            "男人以前经历过什么特殊的事情吗？",
            "他的妻子还活着吗？",
            "他在荒岛上待过吗？",
            "他在荒岛上吃了东西吗？",
            "他吃的真的是海龟吗？",
            "那是人肉吗？",
            "是他妻子的肉吗？",
            "今天的海龟汤和他记忆中的一样吗？",
            "他意识到真相了吗？",
            "因为这个真相他选择自杀吗？"
        ],
        "hints": [
            "💡 提示 1：这个故事发生在很久以前",
            "💡 提示 2：男人曾经经历过一场灾难",
            "💡 提示 3：他以为自己在荒岛上吃的是海龟",
            "💡 提示 4：实际上他在荒岛上吃的不是海龟"
        ]
    },
    {
        "title": "半夜的敲门声",
        "difficulty": "⭐⭐⭐",
        "story": "一个独居的女人，每天晚上 12 点都会听到敲门声。她每次打开门都没人。就这样持续了一个月，最后她疯了。为什么？",
        "answer": "这个女人其实已经失明了。她听到的敲门声是真的，但开门后因为看不见，所以以为没人。实际上，敲门的是她的邻居，一个好心人每天来确认她是否安全。但她不知道，以为是自己精神出了问题，最终崩溃了。",
        "keywords": {
            "失明": True,
            "看不见": True,
            "残疾": True,
            "邻居": True,
            "关心": True,
            "安全": True,
            "好心": True,
            "精神": True,
            "崩溃": True,
            "疯狂": True,
            "门": False,
            "鬼": False,
            "恶作剧": False,
            "报复": False
        },
        "key_facts": [
            "女人身体有残疾",
            "她失明了",
            "她看不见",
            "敲门的是人",
            "敲门的是邻居",
            "邻居是好心",
            "邻居来确认她安全",
            "女人不知道是邻居",
            "女人以为没人",
            "女人以为自己疯了",
            "女人精神崩溃了"
        ],
        "yes_questions": [
            "女人身体有残疾吗？",
            "她失明吗？",
            "她看得见吗？",
            "敲门的是人吗？",
            "敲门的是认识的人吗？",
            "是邻居吗？",
            "邻居是好意吗？",
            "女人知道是邻居吗？",
            "女人以为门外没人吗？",
            "女人最后精神崩溃了吗？"
        ],
        "hints": [
            "💡 提示 1：女人的身体有什么特殊情况",
            "💡 提示 2：敲门的人是真实存在的",
            "💡 提示 3：开门后真的'没人'吗？",
            "💡 提示 4：敲门的目的是什么？"
        ]
    },
    {
        "title": "红色的房间",
        "difficulty": "⭐⭐",
        "story": "小明住进了一家便宜的旅馆。他发现隔壁房间的门缝下总是渗出红色的液体。他好奇地舔了一下，发现是甜的。第二天，小明死了。为什么？",
        "answer": "小明舔到的是血。隔壁房间发生了谋杀案，凶手发现小明在偷看，为了灭口就杀了他。红色液体是血，甜味是因为血中含有糖分（或者混合了其他甜的物质）。",
        "keywords": {
            "血": True,
            "谋杀": True,
            "凶手": True,
            "灭口": True,
            "杀人": True,
            "偷看": True,
            "发现": True,
            "旅馆": False,
            "老板": False,
            "价格": False,
            "毒药": False,
            "自杀": False
        },
        "key_facts": [
            "红色液体是血",
            "隔壁发生了谋杀",
            "有人被杀了",
            "凶手在隔壁房间",
            "凶手发现小明了",
            "小明在偷看",
            "凶手为了灭口",
            "凶手杀了小明",
            "血是甜的",
            "小明是被杀的"
        ],
        "yes_questions": [
            "红色液体是血吗？",
            "隔壁发生了犯罪吗？",
            "是谋杀吗？",
            "有人被杀了吗？",
            "凶手在房间里吗？",
            "凶手发现小明了吗？",
            "小明被杀了吗？",
            "是为了灭口吗？",
            "血是甜的吗？",
            "小明是被他杀吗？"
        ],
        "hints": [
            "💡 提示 1：红色液体是什么？",
            "💡 提示 2：小明的死和隔壁房间有关吗？",
            "💡 提示 3：有人知道小明发现了秘密吗？",
            "💡 提示 4：凶手会怎么做？"
        ]
    },
    {
        "title": "消失的乘客",
        "difficulty": "⭐⭐⭐⭐",
        "story": "一辆公交车在深夜行驶，司机在每个站都停车，但没有任何人上车或下车。可是车上的人数却一直在减少。为什么？",
        "answer": "这是一辆运送尸体的殡仪馆专用车。司机每到一个站点就卸下一具尸体（送到不同的火葬场或墓地），所以车上的人数（尸体数量）在减少，但没有活人上下车。",
        "keywords": {
            "尸体": True,
            "殡仪馆": True,
            "火葬场": True,
            "墓地": True,
            "运送": True,
            "卸下": True,
            "死亡": True,
            "公交车": False,
            "乘客": False,
            "售票员": False
        },
        "key_facts": [
            "这不是普通公交车",
            "是殡仪馆的车",
            "车上装的是尸体",
            "司机在运送尸体",
            "每个站点卸下尸体",
            "送到火葬场或墓地",
            "人数指的是尸体数量",
            "没有活人上下车"
        ],
        "yes_questions": [
            "这是普通的公交车吗？",
            "车上的是活人吗？",
            "那是尸体吗？",
            "司机是殡仪馆工作人员吗？",
            "他在运送尸体吗？",
            "每个站点卸下尸体吗？",
            "送到火葬场吗？",
            "人数在减少是因为卸下尸体吗？"
        ],
        "hints": [
            "💡 提示 1：这不是普通的公交车",
            "💡 提示 2：'人数'指的是活人吗？",
            "💡 提示 3：车上装的是什么？",
            "💡 提示 4：司机的职业可能是什么？"
        ]
    },
    {
        "title": "时间循环的杀手",
        "difficulty": "⭐⭐⭐⭐⭐",
        "story": "一个男人每天早上醒来，都会发现床头放着一张报纸，日期是明天。他按照报纸上的内容生活，一切都准确无误。直到有一天，报纸上刊登了他的死讯，死亡时间是今晚 12 点。他整晚不敢睡觉，死死盯着时钟。12 点到了，他安然无恙。但第二天，他还是死了。为什么？",
        "answer": "男人确实活过了 12 点，但他看到的报纸其实是后天（而不是明天）的。第一天他看到的是周二的报纸（显示周一的新闻），所以他以为今天是周二，实际上是周三。当他看到自己的死讯说'今晚 12 点'时，他以为是周二晚上，其实是周三晚上。他活过了周二 12 点，但在周三晚上 12 点准时死亡。报纸是时间旅行者故意放在那里引导他的。",
        "keywords": {
            "时间": True,
            "报纸": True,
            "日期": True,
            "明天": True,
            "后天": True,
            "今天": True,
            "星期": True,
            "误导": True,
            "时间旅行": True,
            "循环": True,
            "闹钟": False,
            "梦境": False,
            "幻觉": False
        },
        "key_facts": [
            "报纸的日期有误导性",
            "男人搞错了今天的日期",
            "他以为看到的是明天的报纸",
            "实际上看到的是后天的报纸",
            "他以为自己活过了死亡时间",
            "其实还没到真正的死亡时间",
            "第二天晚上 12 点他才死",
            "有人故意误导他"
        ],
        "yes_questions": [
            "报纸的日期是正确的吗？",
            "男人知道的日期对吗？",
            "他搞错日期了吗？",
            "报纸是明天的吗？",
            "是后天的吗？",
            "有人故意误导他吗？",
            "他活过了第一个 12 点吗？",
            "他在第二个 12 点死的吗？"
        ],
        "hints": [
            "💡 提示 1：关键不在于时间，而在于日期",
            "💡 提示 2：男人真的知道今天是星期几吗？",
            "💡 提示 3：报纸真的是'明天'的吗？",
            "💡 提示 4：他活过了 12 点，但真的是你以为的那个 12 点吗？"
        ]
    },
    {
        "title": "双胞胎的谎言",
        "difficulty": "⭐⭐⭐⭐⭐",
        "story": "警察抓到一名嫌疑人，他有完美的不在场证明：案发时他在千里之外的城市，有多人作证。但侦探只问了一个问题就确定他是真凶。侦探问的是：'你认识死者吗？'嫌疑人回答：'不认识，我从未见过她。'为什么这个回答暴露了他？",
        "answer": "死者是一名女性，但警方从未向外界透露过死者的性别。嫌疑人说不认识'她'，说明他知道死者是女性，这暴露了他就是凶手。这是一个经典的'知识泄漏'案例——只有凶手才知道的细节。",
        "keywords": {
            "性别": True,
            "女性": True,
            "死者": True,
            "知道": True,
            "泄漏": True,
            "细节": True,
            "暴露": True,
            "警察": False,
            "证据": False,
            "证人": False
        },
        "key_facts": [
            "警方未公开死者性别",
            "死者是女性",
            "嫌疑人知道死者是女性",
            "他用'她'称呼死者",
            "只有凶手才知道这个信息",
            "他不应该知道死者性别",
            "一句话暴露了他"
        ],
        "yes_questions": [
            "警方公开了所有信息吗？",
            "死者是女性吗？",
            "嫌疑人知道死者性别吗？",
            "他不应该知道吗？",
            "只有凶手才知道吗？",
            "他的话有问题吗？",
            "是措辞暴露了他吗？"
        ],
        "hints": [
            "💡 提示 1：问题出在他的回答上",
            "💡 提示 2：有些信息警方没有公开",
            "💡 提示 3：他知道了一些不该知道的事情",
            "💡 提示 4：注意他如何称呼死者"
        ]
    },
    {
        "title": "倒着走的凶手",
        "difficulty": "⭐⭐⭐⭐⭐",
        "story": "雪夜里，一个人在家中被杀。警察赶到时，发现雪地上只有受害者的脚印，从门口延伸到屋内，然后就没有了。门窗都锁着，是密室。但侦探却说：'凶手从未离开过这里。'为什么？",
        "answer": "凶手就是第一个'发现'尸体的人。他作案后，倒着走出屋子（踩着原来的脚印），然后假装成发现者报警。警察看到的'从门口到屋内'的脚印，其实是受害者进来时的脚印，而凶手的脚印被巧妙地隐藏了——因为他一直是倒着走的。",
        "keywords": {
            "脚印": True,
            "倒着走": True,
            "雪地": True,
            "密室": True,
            "发现者": True,
            "报警": True,
            "隐藏": True,
            "离开": False,
            "窗户": False,
            "钥匙": False
        },
        "key_facts": [
            "雪地上的脚印是受害者的",
            "凶手倒着走",
            "凶手踩着原来的脚印出去",
            "凶手是发现尸体的人",
            "凶手报的警",
            "制造了密室的假象",
            "凶手从未真正'离开'"
        ],
        "yes_questions": [
            "脚印是受害者的吗？",
            "凶手倒着走吗？",
            "凶手踩着原路回去吗？",
            "凶手是发现者吗？",
            "凶手报的警吗？",
            "密室是假的吗？",
            "凶手其实还在现场吗？"
        ],
        "hints": [
            "💡 提示 1：关键在于脚印的方向",
            "💡 提示 2：谁第一个发现尸体？",
            "💡 提示 3：凶手怎么离开的？也许他根本没离开",
            "💡 提示 4：如果倒着走会怎样？"
        ]
    },
    {
        "title": "看不见的凶手",
        "difficulty": "⭐⭐⭐⭐",
        "story": "一个盲人在家里被杀了。警察询问他的导盲犬，训犬师说：'我的狗绝对不会伤害人类。'但侦探听完就说：'我知道凶手是谁了。'为什么？",
        "answer": "导盲犬经过严格训练，不会攻击人类，但它们会对主人的遇袭做出反应。如果主人被陌生人攻击，导盲犬会保护主人或者至少表现出异常。但导盲犬没有反应，说明凶手是它熟悉且不设防的人——很可能是主人的家人、朋友或经常来往的人。",
        "keywords": {
            "导盲犬": True,
            "训练": True,
            "熟悉": True,
            "反应": True,
            "信任": True,
            "熟人": True,
            "盲人": True,
            "攻击": False,
            "武器": False,
            "时间": False
        },
        "key_facts": [
            "导盲犬不会攻击人类",
            "导盲犬会保护主人",
            "狗对凶手没有反应",
            "凶手是狗熟悉的人",
            "可能是家人或朋友",
            "不是陌生人作案"
        ],
        "yes_questions": [
            "导盲犬会攻击人吗？",
            "狗会保护主人吗？",
            "狗对凶手有反应吗？",
            "凶手是陌生人吗？",
            "是熟人作案吗？",
            "狗认识凶手吗？"
        ],
        "hints": [
            "💡 提示 1：导盲犬的特性是什么？",
            "💡 提示 2：狗会对什么情况做出反应？",
            "💡 提示 3：凶手和狗的关系如何？",
            "💡 提示 4：为什么狗没有阻止？"
        ]
    },
    {
        "title": "第十三层楼",
        "difficulty": "⭐⭐⭐⭐⭐",
        "story": "一个人住在 30 层楼的高级公寓里。每天早上他乘电梯下到 1 楼去上班。但每天晚上回来时，如果电梯里只有他一个人，他只坐到 15 楼就走楼梯上去；如果有人一起，他就直接坐到 30 楼。某天下雨，他独自坐电梯直接到了 30 楼。为什么？",
        "answer": "这个人是个侏儒（身材矮小的人）。他够不到电梯按钮面板上高于 15 楼的按钮。平时只能按到 15 楼，然后走楼梯。如果有人同行，别人会帮他按 30 楼。下雨天他带着雨伞，可以用雨伞按到 30 楼的按钮，所以直接上去了。",
        "keywords": {
            "身高": True,
            "侏儒": True,
            "矮小": True,
            "按钮": True,
            "雨伞": True,
            "够不到": True,
            "帮助": True,
            "电梯": False,
            "楼层": False,
            "天气": False
        },
        "key_facts": [
            "主人公身材矮小",
            "他够不到高层按钮",
            "最高只能按到 15 楼",
            "需要别人帮助",
            "用雨伞可以按到",
            "下雨天带了伞"
        ],
        "yes_questions": [
            "主人公身体有特殊吗？",
            "他很矮吗？",
            "是侏儒吗？",
            "他够不到按钮吗？",
            "能按到 30 楼吗？",
            "需要帮助吗？",
            "雨伞有用吗？"
        ],
        "hints": [
            "💡 提示 1：问题出在电梯按钮上",
            "💡 提示 2：主人公的身体有什么特点？",
            "💡 提示 3：为什么有人时就能到 30 楼？",
            "💡 提示 4：雨伞在这里有什么用？"
        ]
    },
    {
        "title": "录音带里的秘密",
        "difficulty": "⭐⭐⭐⭐",
        "story": "警察在一个死者手中发现了一盘录音带。播放后，里面传来死者的声音：'我受不了了，我要自杀。'然后是枪声。警察听完后立即判定：这是他杀，不是自杀。为什么？",
        "answer": "如果是自杀，死者说完话后开枪，录音会继续录下枪声以及之后的声音（倒地、挣扎等）。但这盘录音带在枪声后就结束了，说明有人开枪后立即关掉了录音机并拿走了后半段录音带。这是凶手伪造自杀现场的破绽。",
        "keywords": {
            "录音": True,
            "枪声": True,
            "之后": True,
            "关掉": True,
            "伪造": True,
            "现场": True,
            "破绽": True,
            "磁带": False,
            "时间": False,
            "地点": False
        },
        "key_facts": [
            "录音应该在枪声后继续",
            "会有倒地的声音",
            "但录音突然结束",
            "有人关掉了录音机",
            "拿走了后半段",
            "这是伪造的现场"
        ],
        "yes_questions": [
            "录音完整吗？",
            "枪声后有声音吗？",
            "应该有倒地声吗？",
            "有人关掉录音机吗？",
            "是伪造的吗？",
            "凶手处理了录音吗？"
        ],
        "hints": [
            "💡 提示 1：录音带的完整性有问题",
            "💡 提示 2：开枪后会发生什么？",
            "💡 提示 3：录音应该录下什么？",
            "💡 提示 4：为什么录音突然停止？"
        ]
    }
]

# 初始化 session state
if 'current_story' not in st.session_state:
    st.session_state.current_story = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'revealed_facts' not in st.session_state:
    st.session_state.revealed_facts = []
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'hint_index' not in st.session_state:
    st.session_state.hint_index = 0

def analyze_question(question, story):
    """分析玩家的问题并给出回答"""
    question_lower = question.strip().lower()
    
    yes_no_patterns = [
        r'是.*吗', r'有.*吗', r'会.*吗', r'能.*吗', 
        r'在.*吗', r'去.*吗', r'喜欢.*吗', r'知道.*吗',
        r'是不是', r'有没有', r'会不会', r'能不能',
        r'吗\?$', r'吗？$'
    ]
    
    is_yes_no = any(re.search(pattern, question) for pattern in yes_no_patterns)
    
    found_keywords = []
    for keyword in story["keywords"]:
        if keyword in question:
            found_keywords.append(keyword)
    
    matched_facts = []
    for fact in story["key_facts"]:
        fact_words = fact.split()
        if any(word in question for word in fact_words):
            matched_facts.append(fact)
    
    if not found_keywords and not matched_facts:
        return "❌ 不相关", "这个问题与故事的核心无关。试着问一些关于人物、事件、原因的问题。"
    
    if is_yes_no:
        important_keywords = [k for k in found_keywords if story["keywords"].get(k, False)]
        
        if important_keywords:
            for fact in story["key_facts"]:
                if any(kw in fact for kw in important_keywords) and fact not in st.session_state.revealed_facts:
                    st.session_state.revealed_facts.append(fact)
            
            return "✅ 是", "你接近真相了！"
        elif found_keywords:
            return "❌ 不是", "这个方向不太对。"
        else:
            return "❌ 不是", "答案是否定的。"
    else:
        if matched_facts:
            return "💡 相关", "这个问题很重要，继续沿着这个思路问下去！"
        elif found_keywords:
            return "💡 部分相关", "这个问题涉及到一些元素，但可能不是核心。"
        else:
            return "❌ 不相关", "建议换个角度提问。"

def check_answer(user_answer, story):
    """检查用户的答案是否正确"""
    user_answer_lower = user_answer.lower()
    
    matched_count = sum(1 for fact in story["key_facts"] if fact in user_answer_lower)
    total_facts = len(story["key_facts"])
    
    accuracy = matched_count / total_facts if total_facts > 0 else 0
    
    if accuracy >= 0.8:
        return True, accuracy
    elif accuracy >= 0.5:
        return False, accuracy
    else:
        return False, accuracy

# 标题
st.title("🐢 海龟汤 - 互动问答版")
st.markdown("---")

# 侧边栏
st.sidebar.title("🎮 游戏控制")

# 难度选择 - 修复了这里，现在包含五星难度
difficulty_options = {
    "全部": "全部",
    "⭐⭐ 简单": "⭐⭐",
    "⭐⭐⭐ 中等": "⭐⭐⭐",
    "⭐⭐⭐⭐ 困难": "⭐⭐⭐⭐",
    "⭐⭐⭐⭐⭐ 地狱": "⭐⭐⭐⭐⭐"
}

selected_difficulty = st.sidebar.selectbox(
    "选择难度",
    list(difficulty_options.keys())
)

# 开始游戏按钮
if st.sidebar.button("🎲 开始新游戏", type="primary"):
    difficulty_value = difficulty_options[selected_difficulty]
    
    if difficulty_value == "全部":
        filtered_stories = stories
    else:
        filtered_stories = [s for s in stories if s["difficulty"] == difficulty_value]
    
    if filtered_stories:
        st.session_state.current_story = random.choice(filtered_stories)
        st.session_state.chat_history = []
        st.session_state.game_started = True
        st.session_state.revealed_facts = []
        st.session_state.show_answer = False
        st.session_state.hint_index = 0
        st.rerun()
    else:
        st.sidebar.error(f"该难度下没有找到题目，请选择其他难度")

# 显示提示按钮
if st.sidebar.button("💡 查看提示"):
    if st.session_state.game_started and st.session_state.current_story:
        story = st.session_state.current_story
        hints = story.get("hints", [])
        if hints and st.session_state.hint_index < len(hints):
            st.session_state.hint_index += 1
            st.rerun()
        elif not hints:
            st.sidebar.warning("这道题暂无提示")

# 游戏主界面
if st.session_state.game_started and st.session_state.current_story:
    story = st.session_state.current_story
    
    st.markdown(f"""
    <div class="game-box">
        <h2 style="color: #2E86C1;">📖 {story['title']}</h2>
        <p style="font-size: 18px; line-height: 1.8;">{story['story']}</p>
        <p><strong>难度：</strong>{story['difficulty']}</p>
        <p><strong>已揭示线索：</strong>{len(st.session_state.revealed_facts)}/{len(story['key_facts'])}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💬 提问记录")
    
    if st.session_state.chat_history:
        chat_container = st.container()
        with chat_container:
            for chat in st.session_state.chat_history[-10:]:
                if chat["type"] == "question":
                    st.markdown(f"""
                    <div class="question-box">
                        <strong>🤔 你问：</strong>{chat["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    css_class = chat.get("css_class", "answer-related")
                    icon = chat.get("icon", "💡")
                    hint = chat.get("hint", "")
                    st.markdown(f"""
                    <div class="{css_class}">
                        <strong>{icon} 回答：</strong>{chat["content"]}
                        {f"<br><small>{hint}</small>" if hint else ""}
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("👆 在下面输入你的问题开始推理吧！你可以问是非题，也可以直接猜测答案！")
    
    st.markdown("---")
    
    user_input = st.text_input(
        "提出你的问题或猜测答案：",
        key="user_input",
        placeholder="例如：'这个男人以前经历过什么吗？' 或 '我认为答案是...'"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        submit_button = st.button("提交问题", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("清空记录", use_container_width=True)
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    if submit_button and user_input:
        guess_keywords = ["我认为", "答案是", "真相是", "因为", "所以", "我猜", "我觉得"]
        is_guess = any(kw in user_input for kw in guess_keywords)
        
        if is_guess or len(user_input) > 20:
            result, accuracy = check_answer(user_input, story)
            
            st.session_state.chat_history.append({
                "type": "question",
                "content": user_input
            })
            
            if result:
                st.session_state.chat_history.append({
                    "type": "answer",
                    "content": f"🎉 恭喜你答对了！正确率：{accuracy*100:.0f}%",
                    "css_class": "answer-yes",
                    "icon": "✅"
                })
                st.balloons()
            else:
                hint_text = ""
                if accuracy >= 0.5:
                    hint_text = "你已经接近真相了！继续思考一下遗漏的部分。"
                else:
                    hint_text = "还差得比较远，再问问其他问题吧。"
                
                st.session_state.chat_history.append({
                    "type": "answer",
                    "content": f"❌ 不完全正确。正确率：{accuracy*100:.0f}%",
                    "css_class": "answer-no",
                    "icon": "❌",
                    "hint": hint_text
                })
            
            st.rerun()
        else:
            answer_type, answer_content = analyze_question(user_input, story)
            
            st.session_state.chat_history.append({
                "type": "question",
                "content": user_input
            })
            
            css_map = {
                "✅ 是": ("answer-yes", "✅"),
                "❌ 不是": ("answer-no", "❌"),
                "💡 相关": ("answer-related", "💡"),
                "💡 部分相关": ("answer-related", "💡"),
                "❌ 不相关": ("answer-unrelated", "❌")
            }
            
            css_class, icon = css_map.get(answer_type, ("answer-related", "💡"))
            
            st.session_state.chat_history.append({
                "type": "answer",
                "content": f"{answer_type} - {answer_content}",
                "css_class": css_class,
                "icon": icon
            })
            
            st.rerun()
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👁️ 查看答案", use_container_width=True):
            st.session_state.show_answer = not st.session_state.show_answer
            st.rerun()
    
    with col2:
        if st.button("🔄 下一题", use_container_width=True):
            available = [s for s in stories if s != story]
            if available:
                st.session_state.current_story = random.choice(available)
                st.session_state.chat_history = []
                st.session_state.revealed_facts = []
                st.session_state.show_answer = False
                st.session_state.hint_index = 0
                st.rerun()
    
    with col3:
        if st.button("📋 参考问题", use_container_width=True):
            with st.expander("参考问题示例"):
                for q in story["yes_questions"][:5]:
                    st.write(f"- {q}")
    
    hints = story.get("hints", [])
    if st.session_state.hint_index > 0 and hints:
        st.markdown("### 💡 已获得的提示")
        for i in range(st.session_state.hint_index):
            if i < len(hints):
                st.markdown(f"""
                <div class="clue-box">
                    {hints[i]}
                </div>
                """, unsafe_allow_html=True)
        
        if st.session_state.hint_index >= len(hints):
            st.warning("⚠️ 已经没有更多提示了！要不要直接看答案？")
    
    if st.session_state.show_answer:
        st.markdown("### ✅ 真相揭晓")
        st.markdown(f"""
        <div class="answer-box">
            <p style="font-size: 16px; line-height: 1.8;">{story['answer']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 关键事实")
        for fact in story["key_facts"]:
            revealed = fact in st.session_state.revealed_facts
            icon = "✅" if revealed else "⬜"
            st.write(f"{icon} {fact}")

else:
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1 style="color: #2E86C1;">欢迎来到海龟汤问答游戏！🐢</h1>
        <p style="font-size: 18px; line-height: 1.8;">
            这是一款互动推理游戏，你可以通过提问来寻找真相。<br>
            系统会回答：<strong>✅ 是</strong>、<strong>❌ 不是</strong>、<strong>💡 相关</strong>、<strong>❌ 不相关</strong>
        </p>
        <p style="color: #7F8C8D;">
            点击左侧的 <strong>"🎲 开始新游戏"</strong> 按钮开始挑战！
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🐢 海龟汤问答游戏 | 锻炼你的逻辑思维</p>", 
            unsafe_allow_html=True)