import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import get_data, get_models, make_3d_grid, save_html
import numpy as np


def run():
    # 1. 准备数据 (3特征, 二分类)
    X, y, f_names, t_names = get_data(dims=3, binary=True)

    # 适当的分辨率，平衡平滑度和性能
    resolution = 25
    xx, yy, zz, grid_points = make_3d_grid(X, resolution=resolution)
    models = get_models()

    # 2. 创建 2x2 3D子图
    specs = [[{'type': 'scene'}, {'type': 'scene'}], [{'type': 'scene'}, {'type': 'scene'}]]
    fig = make_subplots(rows=2, cols=2, specs=specs,
                        subplot_titles=[m[0] for m in models],
                        vertical_spacing=0.08, horizontal_spacing=0.01)

    print("Task 3: Calculating 3D Volume & Decision Surfaces...")

    for idx, (name, model) in enumerate(models):
        row, col = idx // 2 + 1, idx % 2 + 1
        model.fit(X, y)

        # 预测概率 (取 Class 1 的概率)
        probs = model.predict_proba(grid_points)[:, 1]

        # --- 核心可视化 1: 概率体积 (Probability Volume) ---
        # 类似 CT 扫描，用透明度表示概率密度 (0.1 ~ 0.9)
        # 越接近 0 (Class 0 核心) 为蓝色，越接近 1 (Class 1 核心) 为红色
        # 中间区域透明，两端不透明
        fig.add_trace(go.Volume(
            x=xx.flatten(), y=yy.flatten(), z=zz.flatten(),
            value=probs,
            isomin=0.1, isomax=0.9,
            opacity=0.1,  # 整体透明度
            surface_count=15,  # 15层切片，细腻的渐变
            colorscale='RdBu_r',  # 蓝(0)-白(0.5)-红(1)
            showscale=(idx == 1),  # 只显示一个色标
            caps=dict(x_show=False, y_show=False, z_show=False),  # 不封口，看内部
            name='Prob Volume',
            hoverinfo='skip'
        ), row=row, col=col)

        # --- 核心可视化 2: 决策面 (Decision Surface P=0.5) ---
        # 精确画出概率为 0.5 的分界墙 (灰色网格)
        fig.add_trace(go.Isosurface(
            x=xx.flatten(), y=yy.flatten(), z=zz.flatten(),
            value=probs,
            isomin=0.5, isomax=0.5,  # 锁定在 0.5
            surface_fill=0.6,  # 半透明填充
            colorscale=[[0, 'gray'], [1, 'gray']],  # 灰色中立
            showscale=False,
            slices=dict(z=dict(show=True, locations=[0])),  # 增加切片感
            name='Boundary (P=0.5)'
        ), row=row, col=col)

        # --- 原始散点 ---
        colors = ['#1f77b4', '#d62728']  # 蓝 vs 红
        for cls_id in np.unique(y):
            fig.add_trace(go.Scatter3d(
                x=X[y == cls_id, 0], y=X[y == cls_id, 1], z=X[y == cls_id, 2],
                mode='markers',
                marker=dict(size=4, color=colors[cls_id], line=dict(width=1, color='black')),
                name=t_names[cls_id],
                showlegend=(idx == 0)
            ), row=row, col=col)

        scene_key = f'scene{idx + 1 if idx > 0 else ""}'
        fig.layout[scene_key].update(
            xaxis_title=f_names[0],
            yaxis_title=f_names[1],
            zaxis_title=f_names[2]
        )

    save_html(fig, "task3.html", "Task 3: 3D Probability Map (Volume + Iso-Surface)")


if __name__ == "__main__": run()