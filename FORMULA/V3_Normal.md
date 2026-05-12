# BiliVBoard V3 Normal / V3 普通版

## Formula / 公式

```

Score = 10000 + H_base × I_booster × D_decay × A_scale
Score = 10000 + 基础热度 × 互动增强因子 × 时间衰减 × 放大系数

```

---

## Step-by-Step / 逐步计算

### Step 1: Base Heat / 基础热度
```

H_base = ln(P + 1) × (1 + 0.3 × ln(C + 1))

```
| Symbol / 符号 | Meaning / 含义 |
|:---:|---|
| `P` | Play count / 播放量 |
| `C` | Coin count / 投币数 |

---

### Step 2: Interaction Rate / 互动率
```

I_rate = ─────────────────────────────────────────────
P

```
| Symbol / 符号 | Weight / 权重 | Meaning / 含义 |
|:---:|:---:|---|
| `L` | ×1.0 | Likes / 点赞 |
| `C` | ×2.0 | Coins / 投币 |
| `F` | ×1.5 | Favorites / 收藏 |
| `M` | ×1.5 | Comments / 评论 |
| `D_m` | ×0.5 | Danmaku / 弹幕 |
| `S` | ×1.0 | Shares / 分享 |

---

### Step 3: Interaction Booster / 互动增强因子
```

I_booster = 1 + 1.5 × I_rate

```

---

### Step 4: Time Decay / 时间衰减
```

D_decay = e^(-T / 30)
Half-life ≈ 20.79 days / 半衰期约 20.79 天

```
| Symbol / 符号 | Meaning / 含义 |
|:---:|---|
| `T` | Days since publish / 发布后天数 |

---

### Step 5: Final Score / 最终得分
```

Score = 10000 + ( H_base × I_booster × D_decay × 800 )

```
| Param / 参数 | Value / 值 | Meaning / 含义 |
|:---:|:---:|---|
| `A_scale` | `800` | Amplification scale / 放大系数 |

---

## Edge Cases / 边界处理

| Condition / 条件 | Handling / 处理方式 |
|---|---|
| `P = 0` | `I_rate = 0` |
| `C = 0` | `ln(C + 1) = 0`, H_base degrades to `ln(P + 1)` / 退化为纯播放热度 |
