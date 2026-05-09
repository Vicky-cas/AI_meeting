# RAG 知識庫索引

## 索引用途

本檔案是 `data/knowledge/` 的知識庫目錄索引，提供 RAG 建索引前的資料總覽。每份 markdown 都是一個可被檢索的 knowledge note，內容涵蓋食品機械設備公司、訂單流程、工廠排程、角色訪談、風險規則與 app 開發案例。

後續若要做 chunk-based RAG，可優先依照本索引的主題、關鍵字與適用問題切分 metadata。

## 知識文件清單

| 檔案 | 類型 | 主題 | 適用問題 |
| --- | --- | --- | --- |
| `company_background.md` | 公司資料 | 公司背景、營運特色、系統願景 | 公司是做什麼的？為什麼需要訂單資源調度 app？ |
| `company_culture.md` | 公司資料 | 公司文化、協作原則、角色責任 | 哪些角色會使用系統？AI 輸出要遵守什麼原則？ |
| `order_process.md` | 流程資料 | 詢價、訪談、報價、接單、工程、採購、出貨 | 訂單從詢價到出貨有哪些流程？ |
| `factory_production_process.md` | 流程資料 | 工程圖、材料、加工、焊接、拋光、組裝、FAT | 工廠生產流程怎麼跑？哪些狀態不能跳過？ |
| `order_system.md` | 訂單資料 | 假訂單、客戶需求、BOM、排程重點 | SO-2026-0509-001 有哪些需求？某訂單需要哪些零件？ |
| `factory_app.md` | 生產資料 | 工作站產能、零件工時、資源衝突、app 功能 | 哪些工作站是瓶頸？CNC 滿載時怎麼辦？ |
| `scheduling_rules.md` | 規則資料 | 排程規則、工單保護、風險分類、建議策略 | 哪些工單不能重排？風險等級怎麼判斷？ |
| `data_dictionary.md` | 系統資料 | orders、parts、work_orders、risks 等資料欄位 | API 或資料庫需要哪些欄位？AI 輸出要保留哪些 id？ |
| `sales_interview_notes.md` | 訪談資料 | 業務接單、交期承諾、客戶需求整理 | 業務最需要什麼功能？接單前要確認什麼？ |
| `production_interview_notes.md` | 訪談資料 | 生管排程、插單、工作站負荷、缺料 | 生管如何看待重排？插單會影響什麼？ |
| `engineering_interview_notes.md` | 訪談資料 | 工程圖、BOM、機械與電控規格 | 工程需要哪些待確認項目？BOM 版本怎麼管理？ |
| `sample_meeting_records.md` | 會議資料 | 交期討論、插單、外購件延誤 | 會議後有哪些決議、TODO 與風險？ |
| `bug_case.md` | 開發資料 | bug、測試案例、API 草稿、app 待辦 | app 開發中有哪些測試情境與 API 需求？ |

## 建議 RAG metadata

每個 chunk 建議保留以下 metadata：

| 欄位 | 說明 | 範例 |
| --- | --- | --- |
| source | 原始檔名 | `order_system.md` |
| doc_type | 文件類型 | `order_data`、`process`、`interview`、`rule` |
| topic | 主題 | `order_flow`、`capacity_risk`、`engineering_review` |
| role | 主要角色 | `sales`、`production_control`、`engineering` |
| order_id | 關聯訂單 | `SO-2026-0509-001` |
| risk_type | 風險類型 | `capacity`、`procurement`、`engineering` |
| updated_at | 假資料更新日 | `2026-05-09` |

## 建議查詢範例

### 公司與文化

- 這家公司主要做什麼產品？
- 這個 app 要解決公司哪一些痛點？
- 業務、工程、生管、採購各自負責什麼？

### 訂單與需求

- SO-2026-0509-001 的交期風險是什麼？
- 福盛食品的訂單有哪些客製需求？
- 訂單成立後要拆成哪些任務？

### 工廠與排程

- 哪些工作站最容易成為瓶頸？
- CNC 超載時可以採取哪些策略？
- 哪些工單不可被自動重排？
- 外購件未到時，組裝排程應該怎麼處理？

### 訪談與產品需求

- 業務最希望系統提供哪些功能？
- 生管對自動重排有什麼限制？
- 工程部希望 AI 幫忙整理哪些待確認問題？

### App 開發

- 排程建議 API 需要哪些 request 欄位？
- 風險查詢 API 應該回傳什麼？
- AI 輸出為什麼要保留 order_id、part_id、workstation_id？

## 建議優先索引順序

1. `knowledge_index.md`
2. `company_background.md`
3. `order_process.md`
4. `factory_production_process.md`
5. `order_system.md`
6. `factory_app.md`
7. `scheduling_rules.md`
8. `data_dictionary.md`
9. `sales_interview_notes.md`
10. `production_interview_notes.md`
11. `engineering_interview_notes.md`
12. `sample_meeting_records.md`
13. `bug_case.md`

## 維護規則

- 新增知識文件時，需同步更新本索引。
- 若文件含訂單編號、零件編號或工作站代碼，需列入適用問題或 metadata。
- 若文件是訪談紀錄，需標明角色與訪談主題。
- 若文件是規則資料，需標明風險類型與判斷條件。
- 不確定的資訊應標示為待確認，不要寫成已確認事實。
