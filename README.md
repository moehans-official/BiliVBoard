<p align="center">
  <img src="logo.png" alt="BiliVBoard Logo" width="200">
</p>

<h1 align="center">BiliVBoard</h1>

<p align="center">
  <strong>B站视频数据采集与智能评分系统</strong>
</p>

---

## 项目概述

BiliVBoard 是一个模块化的B站视频数据采集与分析平台，提供完整的数据抓取、处理、评分和可视化解决方案。系统采用异步架构，支持高并发数据采集，内置多种智能评分算法。

## 评分算法

| 算法 | 半衰期 | 适用场景 |
|------|--------|----------|
| V3 Normal | 20.79天 | 常规周榜评估 |
| V3 Radical | 6.93天 | 热点快速排名 |
| V3 E SP | 无衰减 | 长期价值评估 |

### 评分因子

| 因子 | 权重 | 说明 |
|------|------|------|
| 播放量 (P) | 基准 | 对数标准化处理 |
| 点赞 (L) | ×1.0 | 基础互动指标 |
| 投币 (C) | ×2.0 | 深度参与指标 |
| 收藏 (F) | ×1.5 | 长期价值指标 |
| 评论 (M) | ×1.5 | 社区互动指标 |
| 弹幕 (D) | ×0.5 | 实时互动指标 |
| 分享 (S) | ×1.0 | 传播效果指标 |

## 快速开始

```bash
# 安装依赖
pip install -r DataCollector/requirements.txt

# 配置BV号
echo "BV1qDUPYKEzf" > DataCollector/bvid.txt

# 运行采集
python3 DataCollector/main.py
```

## 环境要求

- Python 3.8+
- pip 20.0+

## 特别感谢

- [BiliBoard Database](https://gitee.com/sembre/biliboard-database) - 数据支持与算法参考

## 声明

本项目为独立开源项目，与 BiliBoard 项目制作组无任何关联。所有算法实现均基于公开数据模型，仅供学习研究使用。