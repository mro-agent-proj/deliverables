# 항공기 정비요청 Agent 산출물

보고서·설계서·다이어그램·평가 결과처럼 **완성된 산출물만** 두는 레포입니다. 산출물을 만드는 코드·템플릿·중간 자료는 두지 않습니다.
코드·커밋 조합·배포는 아래 표의 각 레포에서 관리합니다.

```
deliverables/
├── report/                      최종 결과보고서
│   ├── 항공기_정비요청_Agent_최종결과보고서.pdf · .html
│   ├── 트러블슈팅.md
│   ├── images/screens/          화면 캡처 01~10 (보고서 순서)
│   ├── images/diagrams/         보고서 구조도 SVG
│   └── archive/                 초기 보고서 v1
├── design/                      아키텍처 설계서 (README 본문)
│   ├── images/                  유즈케이스·구성도·시퀀스·LangGraph 순서도
│   └── aws/                     AWS 배포 구성도 PNG · HTML
└── evaluations/
    └── 2026-10-23-isolated-200/ 서비스 평가 200건 결과·감사 메타데이터·체크섬
```

| 폴더 | 바로 가기 |
| --- | --- |
| [`report/`](report/) | [최종 결과보고서 PDF](report/항공기_정비요청_Agent_최종결과보고서.pdf) · [HTML](report/항공기_정비요청_Agent_최종결과보고서.html) · [트러블슈팅](report/트러블슈팅.md) · [초기 보고서 v1](report/archive/최종결과보고서_v1_2026-10-21.pdf) |
| [`design/`](design/) | [설계서](design/README.md): MVP, 문제와 AI 적용 지점, 유즈케이스, 구성도, 처리 흐름, LangGraph, MCP 도구, [AWS 배포 구성](design/README.md#aws-배포-구성) |
| [`evaluations/`](evaluations/2026-10-23-isolated-200/) | 실제 LLM·HTTP MCP 서비스 평가 200건. 보고서와 별도 보관 |

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

## 운영 규칙

- 산출물마다 최상위 폴더를 하나씩 둡니다 (예: `report/`, `design/`, 나중에 `presentation/`). 그림은 각 폴더의 `images/` 아래에 둡니다.
- 이미지를 바꿀 때는 새 파일명을 씁니다. 같은 이름으로 덮어쓰면 GitHub 이미지 캐시 때문에 예전 그림이 보입니다.
- 완성본만 올립니다. 생성 스크립트·템플릿은 코드 레포나 개인 작업 폴더에 둡니다.
- 변경은 PR로 올립니다.
