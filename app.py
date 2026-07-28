import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# 页面配置，专为手机/平板竖屏和PC双端适配
st.set_page_config(page_title="掌上数测", layout="centered", initial_sidebar_state="expanded")

st.title("🚗 掌上数测 V0.0")
st.caption("纯自研算法 · 安卓/PC 双端开发调试版")

# 侧边栏（参数配置区）
with st.sidebar:
    st.header("⚙️ 参数设置")
    window = st.selectbox("加窗类型", ["Hanning (汉宁)", "Hamming (汉明)", "Rectangle (矩形)"])
    st.markdown("---")
    # 大按钮，方便手机触控
    if st.button("🚀 生成模拟数据", use_container_width=True):
        st.session_state["run"] = True

# 主界面（数据展示区）
st.write("上传或生成测试信号进行验证：")

# 模拟计算逻辑
if st.session_state.get("run", False):
    with st.spinner("🔬 正在计算频谱..."):
        time.sleep(1.2)  # 模拟实际计算耗时
        
        # ----- 这里是模拟数据，下周把它替换成真实 FFT -----
        x = np.linspace(0, 1000, 500)
        # 模拟带噪声的频谱曲线
        y = np.sin(x/50) * np.exp(-x/500) + 0.1 * np.random.normal(0, 1, 500)
        # -------------------------------------------------
        
        # 使用 Plotly 生成交互式图表（可缩放、可拖动）
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='模拟频谱', line=dict(width=3)))
        fig.update_layout(
            title="📊 当前频谱图 (模拟数据)",
            height=450,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="频率 (Hz)",
            yaxis_title="幅值"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.success("✅ 分析完成！环境验证通过。")
        st.session_state["run"] = False
else:
    st.info("👈 请在左侧点击 '生成模拟数据' 查看效果")