import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import get_data, get_models, make_3d_grid, save_html
import numpy as np


# ==========================================
# Part A: 3D 边界 (硬分类, 3特征)
# ==========================================
def run_boundary_task():
    print("Generating Task 4 Part A: Hard Decision Boundaries...")
    X, y, f_names, t_names = get_data(dims=3, binary=False)
    xx, yy, zz, grid_points = make_3d_grid(X, resolution=20)
    models = get_models()

    specs = [[{'type': 'scene'}, {'type': 'scene'}], [{'type': 'scene'}, {'type': 'scene'}]]
    fig = make_subplots(rows=2, cols=2, specs=specs,
                        subplot_titles=[m[0] for m in models],
                        vertical_spacing=0.08, horizontal_spacing=0.01)

    for idx, (name, model) in enumerate(models):
        row, col = idx // 2 + 1, idx % 2 + 1
        model.fit(X, y)
        preds = model.predict(grid_points)

        # 1. 绘制实体区域 (Solid Blocks)
        fig.add_trace(go.Volume(
            x=xx.flatten(), y=yy.flatten(), z=zz.flatten(), value=preds.flatten(),
            isomin=0, isomax=2, opacity=0.15, surface_count=3,
            colorscale=[[0, '#1f77b4'], [0.5, '#ff7f0e'], [1, '#2ca02c']],
            showscale=False, name='Boundary Region'
        ), row=row, col=col)

        # 2. 绘制散点
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        for cls_id in np.unique(y):
            fig.add_trace(go.Scatter3d(
                x=X[y == cls_id, 0], y=X[y == cls_id, 1], z=X[y == cls_id, 2],
                mode='markers', marker=dict(size=4, color=colors[cls_id], line=dict(width=1, color='black')),
                name=t_names[cls_id], showlegend=(idx == 0)
            ), row=row, col=col)

        scene_key = f'scene{idx + 1 if idx > 0 else ""}'
        fig.layout[scene_key].update(xaxis_title=f_names[0], yaxis_title=f_names[1], zaxis_title=f_names[2])

    save_html(fig, "task4_boundary.html", "Task 4A: Multi-Class Decision Boundaries (Hard Split)")


# ==========================================
# Part B: 3D 概率核心 (软分类, 3特征)
# ==========================================
def run_probability_task():
    print("Generating Task 4 Part B: Probability Clouds (Soft Cores)...")
    # 保持 3个特征 !
    X, y, f_names, t_names = get_data(dims=3, binary=False)

    # 分辨率稍高一点，为了画出好看的气泡
    xx, yy, zz, grid_points = make_3d_grid(X, resolution=25)
    models = get_models()

    specs = [[{'type': 'scene'}, {'type': 'scene'}], [{'type': 'scene'}, {'type': 'scene'}]]
    fig = make_subplots(rows=2, cols=2, specs=specs,
                        subplot_titles=[m[0] for m in models],
                        vertical_spacing=0.08, horizontal_spacing=0.01)

    for idx, (name, model) in enumerate(models):
        row, col = idx // 2 + 1, idx % 2 + 1
        model.fit(X, y)
        probs = model.predict_proba(grid_points)  # (N, 3)

        # 颜色定义
        colors = ['Blues', 'Oranges', 'Greens']  # 对应 Plotly 内置 colorscale 名

        # 为每个类别画一个 "信心气泡"
        for cls_id in range(3):
            # 取出该类的概率场
            prob_field = probs[:, cls_id]

            # 使用 Isosurface 画出概率 > 0.5 的核心区域
            # 这显示了模型认为"绝对属于该类"的空间范围
            fig.add_trace(go.Isosurface(
                x=xx.flatten(), y=yy.flatten(), z=zz.flatten(),
                value=prob_field,
                isomin=0.5,  # 只显示概率 > 50% 的部分
                isomax=0.99,
                surface_count=3,  # 画3层壳 (e.g., 0.5, 0.7, 0.9)
                colorscale=colors[cls_id],
                showscale=False,
                opacity=0.3,  # 半透明，允许看到互相穿插
                name=f'{t_names[cls_id]} Core',
                caps=dict(x_show=False, y_show=False),
                hoverinfo='skip'
            ), row=row, col=col)

        # 绘制散点
        point_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        for cls_id in range(3):
            fig.add_trace(go.Scatter3d(
                x=X[y == cls_id, 0], y=X[y == cls_id, 1], z=X[y == cls_id, 2],
                mode='markers', marker=dict(size=4, color=point_colors[cls_id], line=dict(width=1, color='black')),
                name=t_names[cls_id], showlegend=(idx == 0)
            ), row=row, col=col)

        scene_key = f'scene{idx + 1 if idx > 0 else ""}'
        fig.layout[scene_key].update(xaxis_title=f_names[0], yaxis_title=f_names[1], zaxis_title=f_names[2])

    save_html(fig, "task4_probability.html", "Task 4B: Multi-Class Probability Cores (3D)")


def run():
    run_boundary_task()
    run_probability_task()


if __name__ == "__main__": run()