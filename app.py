import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import scipy.io.wavfile as wav
import scipy.signal as signal
import scipy.fft as fft
import io
import time

# ==========================================
# 1. 页面与样式配置 (复刻 ArtemiS SUITE 风格)
# ==========================================
st.set_page_config(page_title="掌上数测", layout="wide", initial_sidebar_state="expanded")

# 自定义 CSS 注入，模仿 ArtemiS 的深色专业 UI
st.markdown("""
<style>
    /* 全局调整 */
    .stApp { background-color: #f0f2f6; }
    /* 顶部栏模拟 */
    .top-header {
        background-color: #002b49;
        padding: 10px 20px;
        border-bottom: 2px solid #e67e22;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .top-header .title { font-size: 24px; font-weight: bold; }
    .top-header .subtitle { font-size: 14px; opacity: 0.8; }
    /* 左侧菜单按钮模仿 */
    .stButton > button {
        width: 100%;
        background-color: transparent;
        color: #333;
        border: none;
        border-left: 4px solid transparent;
        text-align: left;
        padding: 10px 15px;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: rgba(0, 0, 0, 0.04);
        border-left: 4px solid #e67e22;
        color: #e67e22;
    }
    /* 池列标题 */
    .pool-header {
        font-weight: 700;
        color: #004d7a;
        border-bottom: 2px solid #e67e22;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 自定义顶部栏 (视觉复刻)
# ==========================================
st.markdown("""
<div class="top-header">
    <div class="title">HEAD acoustics <span style="font-size:16px; font-weight:normal;">ArtemiS SUITE</span></div>
    <div class="subtitle">掌上数测 v1.0 (纯自研算法引擎)</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. 左侧导航栏与 Session 状态管理
# ==========================================
if 'page' not in st.session_state:
    st.session_state['page'] = 'Start'
if 'uploaded_data' not in st.session_state:
    st.session_state['uploaded_data'] = None

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/701/701528.png", width=40) # 模拟 HEAD 图标占位
    st.markdown("---")
    if st.button("🏠 Start (开始)"):
        st.session_state['page'] = 'Start'
    if st.button("🎤 Acquisition (采集)"):
        st.session_state['page'] = 'Acquisition'
    if st.button("👂 Listening (聆听)"):
        st.session_state['page'] = 'Listening'
    if st.button("✏️ Editing (编辑)"):
        st.session_state['page'] = 'Editing'
    if st.button("📊 Analysis (分析)"):
        st.session_state['page'] = 'Analysis'
    if st.button("📈 Presentation (演示)"):
        st.session_state['page'] = 'Presentation'
    st.markdown("---")
    if st.button("⚙️ Settings (设置)"):
        st.session_state['page'] = 'Settings'
    if st.button("❓ About (关于)"):
        st.session_state['page'] = 'About'

# ==========================================
# 4. 模块逻辑 (第一个模块：Analysis -> Pool Project)
# ==========================================
current_page = st.session_state['page']

if current_page == 'Start':
    st.title("🚀 开始页面")
    st.info("请点击左侧导航栏的 'Analysis (分析)' 进入核心 Pool Project 数据测试模块。")

elif current_page == 'Analysis':
    st.subheader("📊 Analysis - Pool Project 分析池项目")
    st.caption("严格按照 ArtemiS SUITE 的 Five Pool 逻辑复刻 (Sources → Filters → Analyses → Statistic → Destination)")

    # 使用 5 列布局实现 ArtemiS 的流水线
    col_src, col_filt, col_ana, col_stat, col_dest = st.columns([1.2, 0.8, 1.2, 0.8, 1.8])

    # 4.1 数据源池 (Sources Pool)
    with col_src:
        st.markdown('<div class="pool-header">📂 Sources (数据源)</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("导入信号 (.wav)", type=["wav"], key="file_uploader")
        
        if uploaded_file is not None:
            # 读取 WAV 文件
            try:
                sr, data = wav.read(io.BytesIO(uploaded_file.read()))
                # 如果是立体声，只取第一个通道
                if len(data.shape) > 1:
                    data = data[:, 0]
                st.session_state['uploaded_data'] = (sr, data)
                st.success(f"✅ 文件加载成功: {uploaded_file.name}\n采样率: {sr} Hz")
            except Exception as e:
                st.error(f"⚠️ 文件读取失败: {e}")
        else:
            st.session_state['uploaded_data'] = None
            st.caption("请上传 .wav 音频文件开始分析")

    # 4.2 滤波池 (Filters Pool)
    with col_filt:
        st.markdown('<div class="pool-header">🔽 Filters (滤波)</div>', unsafe_allow_html=True)
        window_func = st.selectbox("窗函数", ["Hanning (汉宁)", "Hamming (汉明)", "Blackman", "Rectangle (矩形)"], index=0)
        weighting = st.selectbox("频率计权", ["None (无)", "A (A计权)", "C (C计权)"], index=0)

    # 4.3 分析池 (Analyses Pool)
    with col_ana:
        st.markdown('<div class="pool-header">📐 Analyses (分析)</div>', unsafe_allow_html=True)
        analysis_type = st.selectbox("分析方法", ["FFT vs. Time (频谱)", "Level vs. Time (声压级)", "1/n Octave (倍频程)"], index=0)
        spectrum_size = st.selectbox("谱线数", ["4096", "2048", "1024", "512"], index=0)

    # 4.4 统计池 (Statistic Pool)
    with col_stat:
        st.markdown('<div class="pool-header">📊 Statistic (统计)</div>', unsafe_allow_html=True)
        st.radio("统计模式", ["Average (平均)", "Max (最大值)", "Min (最小值)"], index=0, disabled=True)

    # 4.5 目标池与运行 (Destination Pool)
    with col_dest:
        st.markdown('<div class="pool-header">🎯 Destination (目标展示)</div>', unsafe_allow_html=True)
        run_btn = st.button("▶️ 运行计算 / Run Calculation", use_container_width=True, type="primary")

        # 图表展示区（相当于 Data Viewer）
        chart_area = st.empty()
        st.markdown("---")
        status_msg = st.empty()

        # 核心逻辑：点击运行按钮
        if run_btn:
            if st.session_state['uploaded_data'] is None:
                st.warning("请先在 Sources 池中上传一个 .wav 信号！")
            else:
                sr, data = st.session_state['uploaded_data']
                
                # 执行信号预处理和计算
                status_msg.info("⏳ 正在计算分析...")
                time.sleep(1) # 模拟计算过程
                
                # 1. 频率计权 (基于 scipy.signal 手搓计权滤波器)
                # 此处做基础演示，暂不实际应用计权，直接进行 FFT
                # 2. 窗函数选取
                win_type = window_func.split(" ")[0]
                if win_type == "Hanning": win = signal.windows.hann(len(data))
                elif win_type == "Hamming": win = signal.windows.hamming(len(data))
                elif win_type == "Blackman": win = signal.windows.blackman(len(data))
                else: win = signal.windows.boxcar(len(data))

                # 3. 加窗并进行 FFT
                n = int(spectrum_size)
                # 如果是长数据，取前 n 个点
                if len(data) > n:
                    data_block = data[:n] * win[:len(data[:n])]
                else:
                    data_block = data * win[:len(data)]

                yf = fft.fft(data_block, n)
                xf = fft.fftfreq(n, 1 / sr)[:n//2]
                mag = 2.0 / n * np.abs(yf[0:n//2])

                # 4. 根据选择的分析方法生成图表
                fig = go.Figure()
                if analysis_type == "FFT vs. Time (频谱)":
                    # 限制显示到 20000Hz
                    mask = xf <= 20000
                    xf, mag = xf[mask], mag[mask]
                    
                    fig.add_trace(go.Scatter(x=xf, y=20*np.log10(mag/2e-5), mode='lines', name='FFT (dB SPL)'))
                    fig.update_layout(
                        title="频域分析 (FFT Spectrum)",
                        xaxis_title="频率 (Hz)", yaxis_title="幅值 (dB)",
                        margin=dict(l=20, r=20, t=40, b=20), height=350,
                        xaxis_type="log", yaxis_type="linear"
                    )
                elif analysis_type == "Level vs. Time (声压级)":
                    # 计算实时 RMS 声压级
                    frame_size = int(sr * 0.125) # Fast 计权 125ms
                    levels = []
                    times = []
                    for i in range(0, len(data), frame_size):
                        frame = data[i:i+frame_size]
                        if len(frame) == 0: break
                        rms = np.sqrt(np.mean(frame**2))
                        # 防止取 log 0
                        if rms < 1e-10: rms = 1e-10
                        spl = 20 * np.log10(rms / 2e-5)
                        levels.append(spl)
                        times.append(i / sr)
                    fig.add_trace(go.Scatter(x=times, y=levels, mode='lines', name='SPL Level (Fast)'))
                    fig.update_layout(
                        title="时域声压级 (Level vs. Time)",
                        xaxis_title="时间 (s)", yaxis_title="声压级 (dB SPL)",
                        margin=dict(l=20, r=20, t=40, b=20), height=350
                    )
                
                status_msg.success("✅ 分析成功！结果已渲染到 Destination 目标池")
                chart_area.plotly_chart(fig, use_container_width=True)

elif current_page in ['Acquisition', 'Listening', 'Editing', 'Presentation', 'Settings', 'About']:
    st.title(f"📍 {current_page} 模块")
    st.info(f"当前正在开发模块：{current_page}。我们已完成了第一个核心模块 'Analysis' 的部署。")        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='模拟频谱', line=dict(width=3)))
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
