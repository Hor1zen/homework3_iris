# 鸢尾花数据集分类可视化

这个项目使用多种机器学习模型对鸢尾花数据集进行分类，并通过交互式图表展示分类结果和决策边界。

[GitHub 仓库](https://github.com/Hor1zen/homework3_iris)

## 功能特性

- **2D 分类矩阵**：4 种模型 × 4 种视图的概率热力图与决策边界
- **3D 决策切面**：逻辑回归与 SVM 的立体等值面可视化
- **3D 概率体**：CT 扫描风格的概率体绘制，雾浓度代表概率
- **多类综合分析**：复杂多类问题的硬分割与软概率核心两种视角

## 技术栈

- Python 3.11.9
- NumPy 2.3.5
- Plotly 6.5.0
- scikit-learn 1.8.0

## 环境要求

- Python 3.11.9 或更高版本
- Chrome/Firefox 等现代浏览器（用于查看交互式图表）

## 安装与运行

1. 克隆仓库
```bash
git clone https://github.com/Hor1zen/homework3_iris.git
cd homework3_iris
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行主程序
```bash
python main.py
```

程序会自动生成所有任务的 HTML 文件，并在浏览器中打开主仪表盘。

## 项目结构

```
homework3_iris/
├── common.py              # 数据加载、模型定义与工具函数
├── main.py                # 主程序，生成报告与索引页
├── task1_2d.py           # 任务一：2D 分类矩阵
├── task2_3d_bound.py     # 任务二：3D 决策切面
├── task3_3d_prob.py      # 任务三：3D 概率体
├── task4_3d_final.py     # 任务四：多类综合分析
├── requirements.txt      # 项目依赖
└── index.html            # 自动生成的主仪表盘
```

## 使用说明

运行 `main.py` 后，所有可视化结果将保存为 HTML 文件，可通过生成的 `index.html` 访问各个任务。

- 任务一：展示四种模型在花瓣长度/宽度二维空间的分类效果
- 任务二：展示二分类问题的三维决策边界
- 任务三：通过概率体展示模型的置信度分布
- 任务四：处理三类鸢尾花的复杂分类问题

## 许可证

MIT License

---
项目作者：Hor1zen | 作业 3：鸢尾花分类可视化