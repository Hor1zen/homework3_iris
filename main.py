import webbrowser
import os
import task1_2d, task2_3d_bound, task3_3d_prob, task4_3d_final


def generate_index_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>鸢尾花分类可视化项目 - Hor1zen</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; padding-top: 60px; font-family: 'Microsoft YaHei', sans-serif; }
            .container { background: rgba(255,255,255,0.98); padding: 40px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
            .card { transition: all 0.3s ease; height: 100%; border: none; background: #fff; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
            .card:hover { transform: translateY(-8px); box-shadow: 0 15px 30px rgba(13, 110, 253, 0.15); }
            .icon-box { font-size: 3rem; margin-bottom: 15px; }
            h1 { font-weight: 700; color: #2c3e50; letter-spacing: 1px; }

            .info-box {
                background-color: #f8f9fa;
                border-radius: 6px;
                padding: 12px;
                margin: 15px 0;
                text-align: left;
                font-size: 0.85rem;
                color: #555;
                border-left: 4px solid #0d6efd;
            }
            .info-row { margin-bottom: 4px; display: flex; align-items: flex-start; }
            .info-title { font-weight: 700; color: #2c3e50; min-width: 45px; margin-right: 5px; }
            .info-content { color: #666; line-height: 1.4; }

            .btn-group-custom { display: flex; gap: 8px; margin-top: auto; }
            .btn-custom { flex: 1; font-size: 0.85rem; padding: 8px 2px; }
            .footer-link { color: #6c757d; text-decoration: none; transition: 0.2s; }
            .footer-link:hover { color: #0d6efd; }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1 class="mb-3">🌸 鸢尾花数据集分类与可视化</h1>
            <p class="lead text-muted mb-5">多维度 · 多模型 · 交互式 3D 分析大作业</p>

            <div class="row g-4">
                <!-- 任务一 -->
                <div class="col-md-6 col-lg-3">
                    <div class="card p-4">
                        <div class="icon-box">📊</div>
                        <h4 class="card-title">任务一：2D 分类矩阵</h4>
                        <p class="card-text text-muted small">4x4 模型对比矩阵，包含平滑概率热力图与决策边界。</p>

                        <div class="info-box">
                            <div class="info-row">
                                <span class="info-title">特征:</span>
                                <span class="info-content">花瓣长度, 花瓣宽度 (2D)</span>
                            </div>
                            <div class="info-row">
                                <span class="info-title">类别:</span>
                                <span class="info-content">3类 (Setosa, Versicolor, Virginica)</span>
                            </div>
                        </div>

                        <a href="task1.html" class="btn btn-outline-primary mt-auto w-100">查看分析</a>
                    </div>
                </div>

                <!-- 任务二 -->
                <div class="col-md-6 col-lg-3">
                    <div class="card p-4">
                        <div class="icon-box">🧊</div>
                        <h4 class="card-title">任务二：3D 决策切面</h4>
                        <p class="card-text text-muted small">逻辑回归与SVM的空间分割，立体等值面可视化。</p>

                        <div class="info-box">
                            <div class="info-row">
                                <span class="info-title">特征:</span>
                                <span class="info-content">花萼长/宽, 花瓣长 (3D)</span>
                            </div>
                            <div class="info-row">
                                <span class="info-title">类别:</span>
                                <span class="info-content">2类 (Setosa, Versicolor)</span>
                            </div>
                        </div>

                        <a href="task2.html" class="btn btn-outline-primary mt-auto w-100">进入 3D 视图</a>
                    </div>
                </div>

                <!-- 任务三 -->
                <div class="col-md-6 col-lg-3">
                    <div class="card p-4">
                        <div class="icon-box">🌫️</div>
                        <h4 class="card-title">任务三：3D 概率体</h4>
                        <p class="card-text text-muted small">基于CT扫描风格的体绘制。雾浓度代表概率，灰色网格为决策墙。</p>

                        <div class="info-box">
                            <div class="info-row">
                                <span class="info-title">特征:</span>
                                <span class="info-content">花萼长/宽, 花瓣长 (3D)</span>
                            </div>
                            <div class="info-row">
                                <span class="info-title">类别:</span>
                                <span class="info-content">2类 (Setosa, Versicolor)</span>
                            </div>
                        </div>

                        <a href="task3.html" class="btn btn-outline-primary mt-auto w-100">查看概率体</a>
                    </div>
                </div>

                <!-- 任务四 (双按钮) -->
                <div class="col-md-6 col-lg-3">
                    <div class="card p-4">
                        <div class="icon-box">🎲</div>
                        <h4 class="card-title">任务四：多类综合分析</h4>
                        <p class="card-text text-muted small">复杂多类问题的两种视角：空间硬分割 vs 概率核心气泡。</p>

                        <div class="info-box">
                            <div class="info-row">
                                <span class="info-title">特征:</span>
                                <span class="info-content">花萼长/宽, 花瓣长 (3D)</span>
                            </div>
                            <div class="info-row">
                                <span class="info-title">类别:</span>
                                <span class="info-content">3类 (Setosa, Versicolor, Virginica)</span>
                            </div>
                        </div>

                        <div class="btn-group-custom">
                            <a href="task4_boundary.html" class="btn btn-outline-primary btn-custom">
                                🧊 决策边界
                            </a>
                            <a href="task4_probability.html" class="btn btn-outline-success btn-custom">
                                🫧 概率气泡
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <hr class="my-5">

            <footer class="text-muted">
                <p class="mb-2"><strong>Hor1zen</strong> | Project Homework 3</p>
                <div>
                    <a href="https://github.com/Hor1zen/homework3_iris" target="_blank" class="footer-link">GitHub Repository</a>
                </div>
            </footer>
        </div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding='utf-8') as f:
        f.write(html_content)
    print("Main Dashboard Updated.")


def main():
    print("Initializing Project Build...")

    print("1. Building Task 1...")
    task1_2d.run()
    print("2. Building Task 2...")
    task2_3d_bound.run()
    print("3. Building Task 3...")
    task3_3d_prob.run()
    print("4. Building Task 4...")
    task4_3d_final.run()

    generate_index_html()

    print("Build Complete. Opening Dashboard...")
    webbrowser.open('file://' + os.path.realpath("index.html"))


if __name__ == "__main__":
    main()