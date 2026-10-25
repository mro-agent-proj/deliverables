# 항공기 정비요청 Agent 산출물

보고서·발표자료·평가 원자료처럼 **코드가 아닌 산출물**을 모아 관리하는 레포입니다.
코드·커밋 조합·배포는 아래 표의 각 레포에서 관리합니다.

| 폴더 | 내용 |
| --- | --- |
| `final-report/` | 최종 결과보고서와 근거 자료 (2026-10 기준, 아래 참고) |
| `architecture/` | AWS 아키텍처 다이어그램 (PNG·HTML·생성 스크립트) |
| `design/` | 아키텍처 설계서: MVP, 문제와 AI 적용 지점, 구성도, 정상·실패 처리 흐름, LangGraph 노드, MCP 도구 |
| [`evaluations/2026-10-23-isolated-200/`](evaluations/2026-10-23-isolated-200/) | 실제 LLM·HTTP MCP 서비스 평가 200건의 결과·감사 메타데이터·체크섬. 보고서와 별도 보관 |

## 레포 구성

| 레포 | 역할 |
| --- | --- |
| [dashboard](https://github.com/mro-agent-proj/dashboard) | 신고자·정비팀·관리자 화면 (Vue 3) |
| [backend](https://github.com/mro-agent-proj/backend) | 계정·요청·배정 API, DB·RabbitMQ, MCP 토큰 발급 (Spring Boot) |
| [LLM](https://github.com/mro-agent-proj/LLM) | AI 서버: LLM1 분류 → LLM2 조사 → LLM3 검토 (FastAPI + LangGraph) |
| [agent](https://github.com/mro-agent-proj/agent) | MCP 서버 2개: business-mcp, rag-mcp (읽기 전용) |
| [integration](https://github.com/mro-agent-proj/integration) | 서비스 4개의 검증된 커밋 조합, 로컬 실행·평가 스크립트 (봇이 자동 갱신) |
| [infra](https://github.com/mro-agent-proj/infra) | AWS 인프라(Terraform)와 운영 배포. 배포는 여기서만 합니다 |
| **deliverables** | **이 레포.** 최종 결과보고서, 아키텍처 다이어그램 등 산출물 |
| [data](https://github.com/mro-agent-proj/data) | RAG 데이터 전달본 (비공개, 외부 저작물 가공 데이터 포함) |

## final-report

- `항공기_정비요청_Agent_최종결과보고서.pdf` (26쪽), 같은 내용의 `.html`
- `final_report.template.html`: 원본 HTML. 고친 뒤 Chrome으로 PDF 인쇄
- `images/`: 아키텍처·LangGraph 그림, 화면 캡처 13장 (시연 데이터 11건으로 촬영)
- `raw/`: 시나리오 실행 결과(`scenario_results.json`), S10 에이전트 추적, 인증·DLQ·테스트 기록
- `트러블슈팅.md`: 통합하며 겪은 문제 20건과 해결
- `v1/`: 팀이 처음 쓴 v1 보고서와 체크리스트

보고서의 수치와 실행 결과는 작성 당시 [integration](https://github.com/mro-agent-proj/integration)이 고정한 커밋 조합(2026-10-23) 기준입니다.
이 폴더는 원래 integration 레포의 `report/`에 있었고, 커밋 기록을 그대로 가져왔습니다.

## 운영 규칙

- 산출물마다 최상위 폴더를 하나씩 둡니다 (예: `final-report/`, `presentation/`).
- 보고서가 특정 커밋 조합이나 평가 결과를 근거로 하면, 그 조합(`verified-*` 태그나 커밋 SHA)을 해당 폴더 README나 본문에 적습니다.
- 변경은 PR로 올립니다.
