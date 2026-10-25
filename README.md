# 항공기 정비요청 Agent 산출물

보고서·발표자료·평가 원자료처럼 **코드가 아닌 산출물**을 모아 관리하는 레포입니다.
코드는 각 서비스 레포(backend, dashboard, agent, LLM), 커밋 조합은 `mro-agent-integration`, 배포는 `infra`에서 관리합니다.

| 폴더 | 내용 |
| --- | --- |
| `final-report/` | 최종 결과보고서와 근거 자료 (2026-10 기준, 아래 참고) |

## final-report

- `항공기_정비요청_Agent_최종결과보고서.pdf` (26쪽), 같은 내용의 `.html`
- `final_report.template.html`: 원본 HTML. 고친 뒤 Chrome으로 PDF 인쇄
- `images/`: 아키텍처·LangGraph 그림, 화면 캡처 13장 (시연 데이터 11건으로 촬영)
- `raw/`: 시나리오 실행 결과(`scenario_results.json`), S10 에이전트 추적, 인증·DLQ·테스트 기록
- `트러블슈팅.md`: 통합하며 겪은 문제 20건과 해결
- `v1/`: 팀이 처음 쓴 v1 보고서와 체크리스트

보고서의 수치와 실행 결과는 작성 당시 `mro-agent-integration`이 고정한 커밋 조합 기준입니다.
이 폴더는 원래 `mro-agent-integration/report/`에 있었고, 커밋 기록을 그대로 가져왔습니다.

## 운영 규칙

- 산출물마다 최상위 폴더를 하나씩 둡니다 (예: `final-report/`, `presentation/`).
- 보고서가 특정 커밋 조합이나 평가 결과를 근거로 하면, 그 조합(`verified-*` 태그나 커밋 SHA)을 해당 폴더 README나 본문에 적습니다.
- 변경은 PR로 올립니다.
