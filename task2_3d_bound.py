# task2_3d_bound.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import get_data, get_models, make_3d_grid, save_html
import numpy as np


def run():
    # 1. 准备数据 (3特征, 2分类)
    X, y, f_names, t_names = get_data(dims=3, binary=True)
    xx, yy, zz, grid_points = make_3d_grid(X, resolution=20)  # 降低分辨率保速度
    models = get_models()

    # 2. 创建 2x2 3D子图
    specs = [[{'type': 'scene'}, {'type': 'scene'}], [{'type': 'scene'}, {'type': 'scene'}]]
    fig = make_subplots(rows=2, cols=2, specs=specs, subplot_titles=[m[0] for m in models])

    # 3. 循环建模
    for idx, (name, model) in enumerate(models):
        row, col = idx // 2 + 1, idx % 2 + 1
        model.fit(X, y)

        # 预测概率用于寻找边界
        probs = model.predict_proba(grid_points)[:, 1].reshape(xx.shape)

        # 绘制等值面 (Decision Boundary Surface)
        fig.add_trace(go.Isosurface(
            x=xx.flatten(), y=yy.flatten(), z=zz.flatten(), value=probs.flatten(),
            isomin=0.45, isomax=0.55, surface_count=1,  # 只显示 0.5 附近的曲面
            colorscale='Gray', opacity=0.6, showscale=False, name='Boundary'
        ), row=row, col=col)

        # 绘制散点
        for cls_id in np.unique(y):
            fig.add_trace(go.Scatter3d(
                x=X[y == cls_id, 0], y=X[y == cls_id, 1], z=X[y == cls_id, 2],
                mode='markers', marker=dict(size=5), name=t_names[cls_id],
                showlegend=(idx == 0)
            ), row=row, col=col)

        # 设置坐标轴标签
        scene_name = f'scene{idx + 1 if idx > 0 else ""}'
        fig.layout[scene_name].update(xaxis_title=f_names[0], yaxis_title=f_names[1], zaxis_title=f_names[2])

    save_html(fig, "task2.html", "Task 2: 3D Decision Boundaries (Binary)")


if __name__ == "__main__": run()