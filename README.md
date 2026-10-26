# 항공기 정비요청 Agent 산출물

보고서·설계서·다이어그램·평가 결과처럼 **완성된 산출물만** 두는 레포입니다. 산출물을 만드는 코드·템플릿·중간 자료는 두지 않습니다.
코드·커밋 조합·배포는 아래 표의 각 레포에서 관리합니다.

| 폴더 | 내용 |
| --- | --- |
| `final-report/` | 최종 결과보고서 PDF·HTML(2026-10-26 개정), 초기 보고서 v1, 트러블슈팅 |
| `architecture/` | AWS 아키텍처 다이어그램 (PNG·HTML) |
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

- [최종 결과보고서 PDF](final-report/항공기_정비요청_Agent_최종결과보고서.pdf)와 같은 내용의 HTML: 2026-10-26 코드 기준 개정
- [초기 보고서 v1](final-report/v1/MRO_Agent_최종결과보고서_v1.pdf), [트러블슈팅](final-report/트러블슈팅.md)

대표 성능은 2026-10-23 서비스 평가 200건 기준입니다. 읽는 기준은 [보고서 README](final-report/README.md)에 있습니다.

생성 스크립트·편집 템플릿·원자료(`source/`, `raw/`, 구 캡처)는 정리했습니다. 보고서 본문이 인용하는 `source/provenance.json`, `raw/trace_final.html` 등은 커밋 [`4236b47`](https://github.com/mro-agent-proj/deliverables/tree/4236b47)에서 볼 수 있습니다.

## 운영 규칙

- 산출물마다 최상위 폴더를 하나씩 둡니다 (예: `final-report/`, `presentation/`).
- 완성본만 올립니다. 생성 스크립트·템플릿은 코드 레포나 개인 작업 폴더에 둡니다.
- 보고서가 특정 커밋 조합이나 평가 결과를 근거로 하면, 그 조합(`verified-*` 태그나 커밋 SHA)을 해당 폴더 README나 본문에 적습니다.
- 변경은 PR로 올립니다.
