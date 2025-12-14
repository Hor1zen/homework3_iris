import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from common import get_data, get_models, save_html  # 复用公共库


def run():
    # 1. 准备数据 (2特征, 3分类)
    X, y, f_names, t_names = get_data(dims=2, binary=False)
    models = get_models()  # 获取 4 个标准化后的模型

    # 2. 创建网格 (用于绘制背景)
    # 分辨率设为 100 以获得细腻的平滑效果(模拟imshow)
    resolution = 100
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, resolution),
                         np.linspace(y_min, y_max, resolution))
    grid_points = np.c_[xx.ravel(), yy.ravel()]

    # 3. 初始化 4x4 子图
    # 行=模型, 列=概率(Class0,1,2) + 决策边界
    model_names = [m[0] for m in models]
    subplot_titles = []
    for name in model_names:
        subplot_titles.extend([f"{name}<br>Class 0 Prob", "Class 1 Prob", "Class 2 Prob", "Decision"])

    fig = make_subplots(
        rows=4, cols=4,
        subplot_titles=subplot_titles,
        vertical_spacing=0.06, horizontal_spacing=0.04,
        shared_xaxes=True, shared_yaxes=True
    )

    # 颜色配置
    prob_colors = ['Blues', 'Oranges', 'Greens']
    # 离散决策边界颜色 (浅蓝, 浅橙, 浅绿)
    decision_colors = [[0, '#a6cee3'], [0.5, '#fdbf6f'], [1, '#b2df8a']]
    scatter_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # 深色用于散点

    print("Calculations started for Task 1 (4x4 Grid)...")

    # 4. 循环建模与绘图
    for row_idx, (name, model) in enumerate(models):
        model.fit(X, y)
        row = row_idx + 1

        # 预测网格
        probs = model.predict_proba(grid_points)  # (N, 3)
        preds = model.predict(grid_points).reshape(xx.shape)

        # --- 绘制前 3 列 (单类概率图) ---
        for cls_idx in range(3):
            col = cls_idx + 1
            prob_grid = probs[:, cls_idx].reshape(xx.shape)

            # A. 概率热力图 (Heatmap)
            fig.add_trace(go.Heatmap(
                x=np.linspace(x_min, x_max, resolution),
                y=np.linspace(y_min, y_max, resolution),
                z=prob_grid,
                colorscale=prob_colors[cls_idx],
                showscale=False,  # 隐藏色条以保持整洁
                zmin=0, zmax=1,
                zsmooth='best',
                name=f'{name} P({cls_idx})'
            ), row=row, col=col)

            # B. 对应类别的散点
            # 只画属于当前 Class 的点
            mask = y == cls_idx
            fig.add_trace(go.Scatter(
                x=X[mask, 0], y=X[mask, 1],
                mode='markers',
                marker=dict(size=6, color='white', line=dict(width=1, color='black')),
                showlegend=False,
                name=f'Class {cls_idx} Data'
            ), row=row, col=col)

        # --- 绘制第 4 列 (最终决策边界) ---
        # C. 决策背景
        fig.add_trace(go.Heatmap(
            x=np.linspace(x_min, x_max, resolution),
            y=np.linspace(y_min, y_max, resolution),
            z=preds,
            colorscale=decision_colors,
            showscale=False,
            zsmooth=False,  # 决策边界不需要平滑，要硬切分
            name='Decision'
        ), row=row, col=4)

        # D. 所有散点 (彩色)
        for cls_idx in range(3):
            mask = y == cls_idx
            fig.add_trace(go.Scatter(
                x=X[mask, 0], y=X[mask, 1],
                mode='markers',
                marker=dict(size=6, color=scatter_colors[cls_idx], line=dict(width=1, color='black')),
                showlegend=(row == 1),  # 图例只在第一行显示
                name=t_names[cls_idx]
            ), row=row, col=4)

    # 5. 布局优化
    fig.update_layout(
        height=1000,  # 增加高度以容纳 4 行
        title_text="Task 1: 2D Classifier Matrix (Probability vs Decision)",
        margin=dict(l=20, r=20, t=80, b=20)
    )


    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    save_html(fig, "task1.html", "Task 1: 2D Model Comparison Matrix")


if __name__ == "__main__": run()