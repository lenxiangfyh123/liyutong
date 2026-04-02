import streamlit as st
import re

# 页面配置
st.set_page_config(
    page_title="🐢 海龟汤 - 问答版",
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
            "服务": False,
            "今天": False,
            "明天": False
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
            "报复": False,
            "仇恨": False
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
            "服务": False,
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

def analyze_question(question, story):
    """分析玩家的问题并给出回答"""
    question = question.strip().lower()
    
    # 检查是否是需要回答"是/否"的问题
    yes_no_patterns = [
        r'是.*吗', r'有.*吗', r'会.*吗', r'能.*吗', 
        r'在.*吗', r'去.*吗', r'喜欢.*吗', r'知道.*吗',
        r'是不是', r'有没有', r'会不会', r'能不能'
    ]
    
    is_yes_no = any(re.search(pattern, question) for pattern in yes_no_patterns)
    
    # 提取关键词
    found_keywords = []
    for keyword in story["keywords"]:
        if keyword in question:
            found_keywords.append(keyword)
    
    # 检查是否接近关键事实
    matched_facts = []
    for fact in story["key_facts"]:
        if any(word in question for word in fact.split()):
            matched_facts.append(fact)
    
    # 生成回答
    if not found_keywords and not matched_facts:
        return "❌ 不相关", "这个问题与故事的核心无关。试着问一些关于人物、事件、原因的问题。"
    
    if is_yes_no:
        # 检查问题中的关键词是否是重要的
        important_keywords = [k for k in found_keywords if story["keywords"].get(k, False)]
        
        if important_keywords:
            # 检查是否已经揭示过这个事实
            for fact in story["key_facts"]:
                if any(kw in fact for kw in important_keywords) and fact not in st.session_state.revealed_facts:
                    st.session_state.revealed_facts.append(fact)
            
            return "✅ 是", "你接近真相了！"
        elif found_keywords:
            return "❌ 不是", "这个方向不太对。"
        else:
            return "❌ 不是", "答案是否定的。"
    else:
        # 特殊疑问句
        if matched_facts:
            return "💡 相关", "这个问题很重要，继续沿着这个思路问下去！"
        elif found_keywords:
            return "💡 部分相关", "这个问题涉及到一些元素，但可能不是核心。"
        else:
            return "❌ 不相关", "建议换个角度提问。"

def check_answer(user_answer, story):
    """检查用户的答案是否正确"""
    user_answer = user_answer.lower()
    
    # 计算匹配的关键事实数量
    matched_count = sum(1 for fact in story["key_facts"] if fact in user_answer)
    total_facts = len(story["key_facts"])
    
    accuracy = matched_count / total_facts
    
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

# 难度选择
difficulty = st.sidebar.selectbox(
    "选择难度",
    ["全部", "⭐⭐ 简单", "⭐⭐⭐ 中等", "⭐⭐⭐⭐ 困难"]
)

# 开始游戏按钮
if st.sidebar.button("🎲 开始新游戏", type="primary"):
    filtered_stories = stories
    if difficulty != "全部":
        filtered_stories = [s for s in stories if s["difficulty"] == difficulty]
    
    import random
    st.session_state.current_story = random.choice(filtered_stories)
    st.session_state.chat_history = []
    st.session_state.game_started = True
    st.session_state.revealed_facts = []
    st.rerun()

# 显示提示按钮
if st.sidebar.button("💡 查看提示"):
    if st.session_state.game_started:
        story = st.session_state.current_story
        st.sidebar.info(f"""
        🔑 关键事实已揭示：{len(st.session_state.revealed_facts)}/{len(story['key_facts'])}
        
        💬 可以尝试问：
        {random.choice(story['yes_questions'])}
        """)

# 游戏主界面
if st.session_state.game_started and st.session_state.current_story:
    story = st.session_state.current_story
    
    # 显示题目
    st.markdown(f"""
    <div class="game-box">
        <h2 style="color: #2E86C1;">📖 {story['title']}</h2>
        <p style="font-size: 18px; line-height: 1.8;">{story['story']}</p>
        <p><strong>难度：</strong>{story['difficulty']}</p>
        <p><strong>已揭示线索：</strong>{len(st.session_state.revealed_facts)}/{len(story['key_facts'])}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 聊天历史区域
    st.markdown("### 💬 提问记录")
    
    if st.session_state.chat_history:
        chat_container = st.container()
        with chat_container:
            for chat in st.session_state.chat_history[-10:]:  # 显示最近 10 条
                if chat["type"] == "question":
                    st.markdown(f"""
                    <div class="question-box">
                        <strong>🤔 你问：</strong>{chat["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    css_class = chat.get("css_class", "answer-related")
                    st.markdown(f"""
                    <div class="{css_class}">
                        <strong>{chat['icon']} 回答：</strong>{chat["content"]}
                        {f"<br><small>{chat.get('hint', '')}</small>" if chat.get('hint') else ""}
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("👆 在下面输入你的问题开始推理吧！")
    
    # 输入区域
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_input(
            "提出你的问题或猜测答案：",
            key="user_input",
            placeholder="例如：'这个男人以前经历过什么吗？' 或 '我认为答案是...'"
        )
    
    with col2:
        submit_button = st.button("提交", type="primary", use_container_width=True)
    
    # 处理用户输入
    if submit_button and user_input:
        # 检查是否是答案猜测
        if any(word in user_input.lower() for word in ["我认为", "答案是", "真相是", "因为", "所以"]):
            # 用户猜测答案
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
            # 用户提问
            answer_type, answer_content = analyze_question(user_input, story)
            
            st.session_state.chat_history.append({
                "type": "question",
                "content": user_input
            })
            
            # 根据回答类型设置样式
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
    
    # 查看答案按钮
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👁️ 查看答案", use_container_width=True):
            with st.expander("点击查看完整答案", expanded=True):
                st.warning("⚠️ 确定要放弃自己推理的机会吗？")
                if st.button("是的，我要查看答案"):
                    st.success(f"✅ **真相：** {story['answer']}")
                    st.info("💡 **关键事实：**\n" + "\n".join(f"- {fact}" for fact in story["key_facts"]))
    
    with col2:
        if st.button("🔄 下一题", use_container_width=True):
            import random
            available = [s for s in stories if s != story]
            st.session_state.current_story = random.choice(available)
            st.session_state.chat_history = []
            st.session_state.revealed_facts = []
            st.rerun()
    
    with col3:
        if st.button("📋 查看提示问题", use_container_width=True):
            with st.expander("参考问题示例"):
                for q in story["yes_questions"][:5]:
                    st.write(f"- {q}")

else:
    # 欢迎界面
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

# 底部
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🐢 海龟汤问答游戏 | 锻炼你的逻辑思维</p>", 
            unsafe_allow_html=True)