import streamlit as st
import random

# 页面配置
st.set_page_config(
    page_title="🐢 海龟汤游戏",
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
</style>
""", unsafe_allow_html=True)

# 海龟汤题目数据库
stories = [
    {
        "title": "经典的海龟汤",
        "difficulty": "⭐⭐",
        "story": "一个男人走进一家餐厅，点了一碗海龟汤。他喝了一口后，突然脸色大变，立刻冲出餐厅，回到家后就自杀了。为什么？",
        "answer": "这个男人曾经和妻子一起遭遇海难，漂流到一个荒岛上。妻子不幸去世，其他幸存者告诉他说，他们找到了食物（海龟汤）才救了他。他一直以为是海龟汤救了自己。直到今天在餐厅喝了真正的海龟汤，才发现味道完全不同。他瞬间明白，当年在荒岛上吃的'海龟汤'其实是...他妻子的肉。无法承受这个真相的他选择了自杀。",
        "hints": [
            "💡 提示 1：这个故事发生在很久以前",
            "💡 提示 2：男人曾经经历过一场灾难",
            "💡 提示 3：他以为自己在荒岛上吃的是海龟",
            "💡 提示 4：实际上他在荒岛上吃的不是海龟"
        ],
        "key_questions": [
            "男人以前是否经历过什么特殊的事情？→ 是，海难",
            "海龟汤的味道和他记忆中的一样吗？→ 不一样",
            "他在荒岛上吃的真的是海龟吗？→ 不是",
            "那是什么？→ 是他妻子的肉"
        ]
    },
    {
        "title": "半夜的敲门声",
        "difficulty": "⭐⭐⭐",
        "story": "一个独居的女人，每天晚上 12 点都会听到敲门声。她每次打开门都没人。就这样持续了一个月，最后她疯了。为什么？",
        "answer": "这个女人其实已经失明了。她听到的敲门声是真的，但开门后因为看不见，所以以为没人。实际上，敲门的是她的邻居，一个好心人每天来确认她是否安全。但她不知道，以为是自己精神出了问题，最终崩溃了。",
        "hints": [
            "💡 提示 1：女人的身体有什么特殊情况",
            "💡 提示 2：敲门的人是真实存在的",
            "💡 提示 3：开门后真的'没人'吗？",
            "💡 提示 4：敲门的目的是什么？"
        ],
        "key_questions": [
            "女人身体有残疾吗？→ 是，她失明了",
            "敲门的是人吗？→ 是",
            "门外真的没有人吗？→ 不是，有人在",
            "为什么她看不到？→ 因为她失明"
        ]
    },
    {
        "title": "红色的房间",
        "difficulty": "⭐⭐",
        "story": "小明住进了一家便宜的旅馆。他发现隔壁房间的门缝下总是渗出红色的液体。他好奇地舔了一下，发现是甜的。第二天，小明死了。为什么？",
        "answer": "小明舔到的是血。隔壁房间发生了谋杀案，凶手发现小明在偷看，为了灭口就杀了他。红色液体是血，甜味是因为血中含有糖分（或者混合了其他甜的物质）。",
        "hints": [
            "💡 提示 1：红色液体是什么？",
            "💡 提示 2：小明的死和隔壁房间有关吗？",
            "💡 提示 3：有人知道小明发现了秘密吗？",
            "💡 提示 4：凶手会怎么做？"
        ],
        "key_questions": [
            "红色液体是血吗？→ 是",
            "小明被杀了吗？→ 是",
            "凶手知道吗？→ 是",
            "为什么要杀小明？→ 灭口"
        ]
    },
    {
        "title": "消失的乘客",
        "difficulty": "⭐⭐⭐⭐",
        "story": "一辆公交车在深夜行驶，司机在每个站都停车，但没有任何人上车或下车。可是车上的人数却一直在减少。为什么？",
        "answer": "这是一辆运送尸体的殡仪馆专用车。司机每到一个站点就卸下一具尸体（送到不同的火葬场或墓地），所以车上的人数（尸体数量）在减少，但没有活人上下车。",
        "hints": [
            "💡 提示 1：这不是普通的公交车",
            "💡 提示 2：'人数'指的是活人吗？",
            "💡 提示 3：车上装的是什么？",
            "💡 提示 4：司机的职业可能是什么？"
        ],
        "key_questions": [
            "这是普通公交车吗？→ 不是",
            "车上的是活人吗？→ 不是",
            "那是什么？→ 尸体",
            "司机是做什么的？→ 殡仪馆工作人员"
        ]
    },
    {
        "title": "完美的不在场证明",
        "difficulty": "⭐⭐⭐⭐⭐",
        "story": "一个男人在警察局报案说他妻子失踪了。警察调查发现，案发时间男人正在电影院看电影，有很多人可以作证。但警察还是逮捕了他。为什么？",
        "answer": "男人确实去了电影院，但他提前录制好了电影，在家里播放给妻子看，然后杀害了妻子，再赶到电影院制造不在场证明。警察发现电影院的监控中，男人看的电影时间和他说的不一致（比如片尾字幕、广告等细节露馅）。",
        "hints": [
            "💡 提示 1：男人的证词是真的吗？部分是",
            "💡 提示 2：他真的在电影院吗？是，但不是全程",
            "💡 提示 3：他是如何制造时间差的？",
            "💡 提示 4：警察发现了什么破绽？"
        ],
        "key_questions": [
            "男人去了电影院吗？→ 去了",
            "他案发时也在电影院吗？→ 不是",
            "他杀了妻子吗？→ 是",
            "破绽在哪里？→ 电影时间对不上"
        ]
    }
]

# 初始化 session state
if 'current_story' not in st.session_state:
    st.session_state.current_story = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'hint_index' not in st.session_state:
    st.session_state.hint_index = 0
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# 标题
st.title("🐢 海龟汤推理游戏")
st.markdown("---")

# 侧边栏 - 选择模式
st.sidebar.title("🎮 游戏设置")
game_mode = st.sidebar.selectbox(
    "选择游戏模式",
    ["📖 单人模式", "👥 多人模式（主持人 + 玩家）"]
)

if game_mode == "📖 单人模式":
    st.sidebar.info("💡 系统会自动显示提示，你可以随时查看答案")
else:
    st.sidebar.info("💡 一人当主持人（知道答案），其他人提问推理")

# 选择难度
difficulty = st.sidebar.selectbox(
    "选择难度",
    ["全部", "⭐⭐ 简单", "⭐⭐⭐ 中等", "⭐⭐⭐⭐ 困难", "⭐⭐⭐⭐⭐ 地狱"]
)

# 开始游戏按钮
if st.sidebar.button("🎲 随机开始", type="primary"):
    filtered_stories = stories
    if difficulty != "全部":
        filtered_stories = [s for s in stories if s["difficulty"] == difficulty]
    
    st.session_state.current_story = random.choice(filtered_stories)
    st.session_state.show_answer = False
    st.session_state.hint_index = 0
    st.session_state.game_started = True

# 游戏区域
if st.session_state.game_started and st.session_state.current_story:
    story = st.session_state.current_story
    
    # 显示题目
    st.markdown(f"""
    <div class="game-box">
        <h2 style="color: #2E86C1;">📖 {story['title']}</h2>
        <p style="font-size: 18px; line-height: 1.8;">{story['story']}</p>
        <p><strong>难度：</strong>{story['difficulty']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 控制面板
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💡 获取提示", use_container_width=True):
            if st.session_state.hint_index < len(story["hints"]):
                st.session_state.hint_index += 1
                st.rerun()
    
    with col2:
        if st.button("🤔 参考答案", use_container_width=True):
            st.session_state.show_answer = not st.session_state.show_answer
            st.rerun()
    
    with col3:
        if st.button("🔄 下一题", use_container_width=True):
            filtered_stories = stories
            if difficulty != "全部":
                filtered_stories = [s for s in stories if s["difficulty"] == difficulty]
            available_stories = [s for s in stories if s != story]
            if available_stories:
                st.session_state.current_story = random.choice(available_stories)
            else:
                st.session_state.current_story = random.choice(stories)
            st.session_state.show_answer = False
            st.session_state.hint_index = 0
            st.rerun()
    
    # 显示提示
    if st.session_state.hint_index > 0:
        st.markdown("### 💡 已获得的提示")
        for i in range(st.session_state.hint_index):
            if i < len(story["hints"]):
                st.markdown(f"""
                <div class="clue-box">
                    {story['hints'][i]}
                </div>
                """, unsafe_allow_html=True)
        
        if st.session_state.hint_index >= len(story["hints"]):
            st.warning("⚠️ 已经没有更多提示了！要不要直接看答案？")
    
    # 显示答案
    if st.session_state.show_answer:
        st.markdown("### ✅ 真相揭晓")
        st.markdown(f"""
        <div class="answer-box">
            <p style="font-size: 16px; line-height: 1.8;">{story['answer']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 关键提问示例")
        for q in story["key_questions"]:
            st.write(f"- {q}")
    
    # 游戏规则说明
    with st.expander("📚 海龟汤游戏规则"):
        st.markdown("""
        ### 什么是海龟汤？
        海龟汤是一种情境猜谜游戏，也被称为"横向思维游戏"。
        
        ### 游戏玩法：
        1. **出题者**（或系统）讲述一个不完整的故事
        2. **猜题者**通过提问来推理真相
        3. 出题者只能回答："是"、"不是"、"不重要"或"与此无关"
        4. 猜题者需要找出故事的完整真相
        
        ### 游戏技巧：
        - 从基本信息开始问起（人物、时间、地点）
        - 逐步缩小范围
        - 注意故事中的矛盾点
        - 发挥想象力，但要符合逻辑
        
        ### 注意事项：
        - 有些故事可能包含恐怖、悬疑元素
        - 保持开放思维，不要局限于常规想法
        """)

else:
    # 未开始游戏时的欢迎界面
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1 style="color: #2E86C1;">欢迎来到海龟汤游戏！🐢</h1>
        <p style="font-size: 18px; line-height: 1.8;">
            这是一款锻炼逻辑思维和推理能力的益智游戏。<br>
            点击左侧的 <strong>"🎲 随机开始"</strong> 按钮开始游戏！
        </p>
        <p style="color: #7F8C8D;">
            准备好挑战你的智商了吗？😏
        </p>
    </div>
    """, unsafe_allow_html=True)

# 底部
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🐢 海龟汤游戏 | 锻炼你的推理能力</p>", 
            unsafe_allow_html=True)