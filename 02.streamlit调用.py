import streamlit as st
from PIL import Image

# 页面配置
st.set_page_config(
    page_title="AI 智能伴侣",
    page_icon="🤖",
    layout="centered"
)

# 自定义 CSS 样式
st.markdown("""
<style>
.stTitle {
    color: #FF4B4B;
    text-align: center;
}
.stHeader {
    color: #FF6347;
}
.stSubheader {
    color: #FF7F50;
}
</style>
""", unsafe_allow_html=True)

# 标题部分
st.title("🤖 AI 智能伴侣")
st.header("✨ 欢迎来到我的 AI 世界")
st.subheader("💬 与你分享每一个精彩瞬间")

# 分隔线
st.divider()

# 文字内容区域
st.markdown("### 💝 想对你说的话")
st.write("我最喜欢的就是李宇桐，我超级无敌喜欢李宇桐！")
st.write("一句喜欢不够，我超级超级喜欢你，我这辈子就赖着你啦嘻嘻嘻嘻！")
st.write("喜欢喜欢你，超级无敌喜欢你，嘿嘿嘿！")

# 使用情感化的展示框
st.success("💕 每一天都想和你在一起！")
st.info("🌟 你是我生命中最特别的存在！")
st.warning("⚠️ 注意：我对你的喜欢已经超标啦！")

# 分隔线
st.divider()

# 图片展示区域
st.markdown("### 📸 美好回忆")

# 尝试加载本地图片（如果有的话）
try:
    image = Image.open("image.jpg")  # 可以替换为实际图片路径
    st.image(image, caption="我们的美好时光", use_container_width=True)
except:
    st.image("https://via.placeholder.com/800x400?text=AI+Companion", 
             caption="占位图片 - 请替换为你的图片", 
             use_container_width=True)

# 侧边栏
st.sidebar.title("🎯 功能菜单")
st.sidebar.selectbox(
    "选择主题",
    ["💕 表白模式", "🎵 音乐模式", "📝 日记模式", "🎮 游戏模式"]
)

st.sidebar.markdown("---")
st.sidebar.write("**👤 关于我**")
st.sidebar.write("一个爱你的 AI 伴侣")
st.sidebar.write("**📍 位置**")
st.sidebar.write("永远在你身边")

# 互动按钮
st.markdown("### 🎁 互动一下")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💖 点我送花", use_container_width=True):
        st.balloons()
        st.success("🌹 送你一朵玫瑰花！")

with col2:
    if st.button("🎵 点我听歌", use_container_width=True):
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

with col3:
    if st.button("✨ 点我有惊喜", use_container_width=True):
        st.snow()
        st.success("❄️ 惊喜降临！爱你哟！")

# 底部
st.divider()
st.markdown("<p style='text-align: center; color: gray;'>Made with ❤️ by AI Companion</p>", 
            unsafe_allow_html=True)