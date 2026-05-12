# BiliVBoard V3 E SP / V3 事件激增版

## Trigger Conditions / 触发条件

```

All three must be met / 三项同时满足:

1. T > 30
2. ΔP_daily / avg_P_7d > 3
3. ΔP_daily ≥ 1000

```

| Symbol / 符号 | Condition / 条件 | Meaning / 含义 |
|:---:|:---:|---|
| `T` | `> 30` | Days since publish / 发布天数 |
| `ΔP_daily` | `≥ 1000` | Daily play increase / 当日播放增量 |
| `ΔP_daily / avg_P_7d` | `> 3` | Spike ratio / 激增比率 |

> If not triggered, fallback to V3 Normal / 未触发时回退至普通版。

---

## Formula / 公式

```

Score = 10000 + H_base × I_booster × E_spike × A_scale
Score = 10000 + 基础热度 × 互动增强因子 × 事件爆发因子 × 放大系数

```

> Time decay cancelled / 时间衰减取消: `D_decay = 1.0`

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

### Step 4: Event Spike Factor / 事件爆发因子
```

E_spike = 1 + k × ln( ΔP_daily / avg_P_7d + 1 )

```
| Symbol / 符号 | Value / 值 | Meaning / 含义 |
|:---:|:---:|---|
| `ΔP_daily` | — | Daily play increase / 当日播放增量 |
| `avg_P_7d` | — | 7-day avg daily plays / 近7日日均播放 |
| `k` | `0.7` | Spike intensity coefficient / 爆发强度系数 |

---

### Step 5: Final Score / 最终得分
```

Score = 10000 + ( H_base × I_booster × E_spike × 800 )

```
| Param / 参数 | Value / 值 | Meaning / 含义 |
|:---:|:---:|---|
| `A_scale` | `800` | Amplification scale / 放大系数 |
| `D_decay` | `1.0` (forced) | Time decay cancelled / 时间衰减取消 |

---

## Edge Cases / 边界处理

| Condition / 条件 | Handling / 处理方式 |
|---|---|
| Trigger not met / 未触发 | Fallback to V3 Normal / 回退普通版 |
| `P = 0` | `I_rate = 0` |
| `C = 0` | `ln(C + 1) = 0` |
