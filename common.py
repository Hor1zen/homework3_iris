import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB


# === 1. 数据获取 ===
def get_data(dims=2, binary=False):
    """
    根据任务需求返回 X, y, feature_names
    dims=2 时强制使用花瓣特征(Petal, 列2/3)，因为区分度最好
    """
    iris = load_iris()

    if dims == 2:
        # 2D模式使用 [Petal Length, Petal Width] (索引 2, 3)
        # 这也是 Iris 数据集中区分度最高的两个特征
        X = iris.data[:, 2:]
        names = [iris.feature_names[2], iris.feature_names[3]]
    else:
        # 3D模式使用 [Sepal Length, Sepal Width, Petal Length] (索引 0, 1, 2)
        X = iris.data[:, :3]
        names = iris.feature_names[:3]

    y = iris.target

    if binary:  # 如果是二分类，移除第3类 (Class 2: Virginica)
        mask = y != 2
        X, y = X[mask], y[mask]

    return X, y, names, iris.target_names


# === 2. 模型定义 ===
def get_models():
    """返回4个标准化的模型管道"""
    return [
        ("Log Reg", make_pipeline(StandardScaler(), LogisticRegression())),
        ("KNN (k=5)", make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))),
        ("SVM (RBF)", make_pipeline(StandardScaler(), SVC(probability=True))),
        ("Naive Bayes", make_pipeline(StandardScaler(), GaussianNB()))
    ]


# === 3. 3D网格生成器 ===
def make_3d_grid(X, resolution=20):
    """生成用于3D预测的坐标网格"""
    margin = 0.5
    x_min, x_max = X[:, 0].min() - margin, X[:, 0].max() + margin
    y_min, y_max = X[:, 1].min() - margin, X[:, 1].max() + margin
    z_min, z_max = X[:, 2].min() - margin, X[:, 2].max() + margin

    x = np.linspace(x_min, x_max, resolution)
    y = np.linspace(y_min, y_max, resolution)
    z = np.linspace(z_min, z_max, resolution)

    xx, yy, zz = np.meshgrid(x, y, z)
    return xx, yy, zz, np.c_[xx.ravel(), yy.ravel(), zz.ravel()]


# === 4. 网页保存助手 (带返回按钮) ===
def save_html(fig, filename, title):
    """保存HTML，并添加原生的悬浮返回按钮"""
    fig.update_layout(
        title=dict(text=title, x=0.5, y=0.98),
        height=950,
        template="plotly_white",
        margin=dict(t=60)
    )

    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            body {{ margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }}
            .back-btn {{
                position: fixed; top: 20px; left: 20px; z-index: 9999;
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid #ddd; padding: 8px 15px; border-radius: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-decoration: none;
                color: #333; font-weight: 600; transition: all 0.3s ease;
                display: flex; align-items: center; gap: 5px;
            }}
            .back-btn:hover {{ background-color: #0d6efd; color: white; box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3); }}
        </style>
    </head>
    <body>
        <a href="index.html" class="back-btn"><span>⬅</span> 返回主页</a>
        {plot_html}
    </body>
    </html>
    """

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ Generated: {filename} (Fixed Navigation)")