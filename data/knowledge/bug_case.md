# 開發中 App 假 bug 與測試案例

## 背景

目前 app 還在開發中，第一階段會先讓使用者輸入訂單與會議紀錄，再由 AI 協助整理需求、任務、API 草稿與 knowledge note。後續會加入 RAG 查詢、SQLite 訂單資料庫、排程演算法與 Streamlit 儀表板。

## Bug Case 1：訂單優先級改變後，已開工工單被覆蓋

- 編號：BUG-2026-0509-001
- 嚴重度：高
- 情境：
  - SO-2026-0509-001 原本優先級為中
  - 工廠已開始加工 P-VALVE-316L 充填閥座
  - 業務將 SO-2026-0509-003 改成高優先
  - 系統重新排程後，直接把已開工的 CNC 時段改掉
- 預期行為：
  - 已開工工單不可被系統自動覆蓋
  - 系統只能產生「建議排程版本」
  - 主管確認後才可變更未開工工單
- 測試資料：
  - 已開工工單狀態：in_progress
  - 可調整工單狀態：planned
  - 不可調整工單狀態：in_progress、completed、qa_locked

## Bug Case 2：外購件未到，系統仍顯示可準時組裝

- 編號：BUG-2026-0509-002
- 嚴重度：高
- 情境：
  - SO-2026-0509-002 需要溫度記錄模組
  - 採購預計到貨日為 2026-06-28
  - 組裝排程被安排在 2026-06-22
  - 系統仍顯示可準時組裝
- 預期行為：
  - 組裝工單不可早於必要外購件到貨日
  - 訂單應標記為 procurement_risk
  - 看板應顯示「溫度記錄模組未到貨」

## Bug Case 3：同一工作站超過每日可用工時

- 編號：BUG-2026-0509-003
- 嚴重度：中
- 情境：
  - WS-CNC-01 每日可用工時為 16 小時
  - 系統同一天排入 24 小時加工任務
  - UI 只顯示完成率，沒有提醒產能超載
- 預期行為：
  - 工作站日負荷超過 100% 時需標示紅色風險
  - 超過 85% 但未滿 100% 時標示黃色提醒
  - 排程 API 回傳 overload_hours

## Bug Case 4：AI 摘要沒有保留訂單編號

- 編號：BUG-2026-0509-004
- 嚴重度：中
- 情境：
  - 使用者輸入會議紀錄包含 SO-2026-0509-001 與 SO-2026-0509-003
  - AI 摘要只寫「第一張訂單」與「第二張訂單」
  - 後續任務無法對應到實際訂單
- 預期行為：
  - AI 輸出必須保留 order_id、part_id、workstation_id
  - 如果原文沒有明確 id，需標示為 unknown，不可自行編造正式 id

## API 草稿假資料

### 建立訂單

```http
POST /orders
```

```json
{
  "order_id": "SO-2026-0509-001",
  "customer": "福盛食品股份有限公司",
  "product": "全自動醬料充填封口線",
  "quantity": 2,
  "priority": "high",
  "delivery_date": "2026-06-20",
  "customization": ["SUS316L", "CIP", "快速換線"],
  "status": "engineering_review"
}
```

### 查詢排程風險

```http
GET /orders/{order_id}/risks
```

```json
{
  "order_id": "SO-2026-0509-001",
  "risk_level": "high",
  "risks": [
    {
      "type": "capacity",
      "resource": "WS-CNC-01",
      "message": "CNC 未來 7 天負荷超過 100%"
    },
    {
      "type": "material",
      "resource": "SUS316L",
      "message": "材料到貨日晚於充填閥座預計開工日"
    }
  ]
}
```

### 產生排程建議

```http
POST /schedule/suggestions
```

```json
{
  "order_ids": ["SO-2026-0509-001", "SO-2026-0509-003"],
  "strategy": "meet_delivery_date",
  "allow_overtime": true,
  "allow_outsource": true,
  "protect_started_jobs": true
}
```

## 測試會議紀錄範例

今天業務提到福盛食品的醬料充填封口線交期不能延，客戶 6 月底要進行新產品試產。工廠端回報 CNC 已經排滿，充填閥座和活塞缸體會卡在同一台車銑複合機。工程部說電控箱可以先做，但是金屬檢測機訊號規格還沒收到。主管希望 app 可以自動列出延誤風險，並建議哪些零件可以外包，哪些工單不能動。

## App 待辦事項

- 新增 knowledge note 匯入流程，將 `data/knowledge/*.md` 載入 RAG。
- 建立訂單、零件、工作站、工單與採購件資料模型。
- 在 prompt 中要求 AI 保留訂單編號、零件編號與工作站代碼。
- 增加排程風險分類：capacity、material、engineering、quality、delivery。
- Streamlit UI 需要新增「訂單風險看板」與「RAG 問答」兩個頁籤。
