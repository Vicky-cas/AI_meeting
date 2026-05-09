# 資料字典假資料

## orders

| 欄位 | 型別 | 說明 |
| --- | --- | --- |
| order_id | string | 訂單編號 |
| customer | string | 客戶名稱 |
| product | string | 設備名稱 |
| quantity | integer | 數量 |
| priority | string | urgent、high、medium、low |
| delivery_date | date | 承諾交期 |
| status | string | 訂單狀態 |
| risk_level | string | normal、warning、high、critical |

## parts

| 欄位 | 型別 | 說明 |
| --- | --- | --- |
| part_id | string | 零件編號 |
| order_id | string | 關聯訂單 |
| part_name | string | 零件名稱 |
| material | string | 材質 |
| quantity | integer | 數量 |
| drawing_status | string | 圖面狀態 |
| food_contact | boolean | 是否接觸食品 |

## workstations

| 欄位 | 型別 | 說明 |
| --- | --- | --- |
| workstation_id | string | 工作站代碼 |
| name | string | 工作站名稱 |
| daily_capacity_hours | number | 每日可用工時 |
| process_type | string | CNC、welding、polishing、assembly、qa |

## work_orders

| 欄位 | 型別 | 說明 |
| --- | --- | --- |
| work_order_id | string | 工單編號 |
| order_id | string | 關聯訂單 |
| part_id | string | 關聯零件 |
| workstation_id | string | 工作站 |
| planned_start | datetime | 預計開始 |
| planned_end | datetime | 預計結束 |
| status | string | 工單狀態 |
| locked | boolean | 是否鎖定不可自動重排 |

## procurement_items

| 欄位 | 型別 | 說明 |
| --- | --- | --- |
| item_id | string | 採購項目編號 |
| order_id | string | 關聯訂單 |
| item_name | string | 品名 |
| supplier | string | 供應商 |
| expected_arrival_date | date | 預計到貨日 |
| status | string | ordered、delayed、received |

## risks

| 欄位 | 型別 | 說明 |
| --- | --- | --- |
| risk_id | string | 風險編號 |
| order_id | string | 關聯訂單 |
| type | string | capacity、material、procurement、engineering、quality、delivery |
| level | string | warning、high、critical |
| message | string | 風險說明 |
| owner | string | 負責角色 |
| due_date | date | 預計處理期限 |

## AI 輸出格式要求

AI 在整理需求時，應盡量對應上述欄位。若資料缺失，應使用 null 或 unknown，並列入待確認問題。不可自行編造正式訂單編號、零件編號或工單編號。
