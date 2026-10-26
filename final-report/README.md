# 최종 결과보고서

2026-10-26 코드 기준으로 본문·구조도·평가 표를 갱신했습니다. 기존 A4 HTML의 표지, 6개 장, 색상, 글꼴, 표·캡처 배치를 유지했습니다. AWS 산출물은 이번 변경에서 제외했습니다.

- [PDF · 24쪽](항공기_정비요청_Agent_최종결과보고서.pdf)
- [동일 내용 HTML](항공기_정비요청_Agent_최종결과보고서.html)
- [편집 템플릿](final_report.template.html)
- [기준 버전](source/provenance.json)
- [과거 트러블슈팅과 후속 상태](트러블슈팅.md)

## 기준을 구분해서 읽기

| 대상 | 기준 | 의미 |
| --- | --- | --- |
| 구현 설명·새 구조도 | 2026-10-26 각 서비스 main | LLM e5d3798, backend ff47ad5, agent a30c900, dashboard 99f25f1. integration ebbc10e의 서비스 포인터와 일치 |
| 대표 성능 | [2026-10-23 격리 후 서비스 평가 200건](../evaluations/2026-10-23-isolated-200/README.md) | 기존 결과를 재집계. 이번 문서 개정에서 모델·서비스 평가를 새로 실행하지 않음 |
| 단위·기능 테스트 | 본문 5.2의 커밋별 GitHub Actions | LLM 186건, agent 일반 46건·1 skip 및 별도 business DB 17건, backend Gradle test·평가 도구 7건, dashboard 타입 검사·빌드 |
| 화면·S10 trace·인증·DLQ·구 시나리오 23건 | 2026-10-21 기존 자료 | 과거 동작 증빙. 현재 성능이나 현재 LLM2 격리 구조의 예시로 사용하지 않음 |

현재 수치는 전체 통과 97/200, 자동배정 중 통과 96/145, 실패 자동배정 49건, 사람 검토 55건입니다. LLM2 부서 일치 71/82와 최종 보류 42건은 별도 지표입니다. 팀 기대 라벨 기준이며 실제 항공 정비 안전성을 입증하는 수치는 아닙니다.

평가 실행 파일 34개 해시와 현재 LLM의 동일 파일이 일치함을 대조했습니다. 평가 `freeze.repositories.ai`는 격리 수정 전 기준 커밋이므로 해당 SHA만으로 당시 실행을 재현할 수 없습니다. 실제 실행 해시·수정 후 커밋·한계는 평가 번들의 manifest/README를 따릅니다.

## 변경한 부분

- LLM2 전용 상태·B02/HISTORY 차단, LLM3 병합·대조, LLM1 맥락 비교를 본문·구조도에 반영.
- MCP 9개, R04 구현, R03 번호 조회, AMM 참고자료 분리, SDR 하이브리드 검색과 모델 범위 확장 반영.
- OpenAI 검색 임베딩 1024차원, Flyway V1~V11, V9 업무 뷰, 수리이력 1,600건·정비 인원 38명 반영.
- 200건 결과·분모·실패 유형·현재 CI를 표로 교체하고 과거 23건 원자료는 보존.
- 설계서의 신고자 조회 API·재조사 분기·임베딩 API 연결을 정정.

## 미완료: 최신 화면 재촬영

문서 작업 당시 Docker daemon과 localhost 앱 서버가 실행 중이지 않아 최신 화면을 직접 촬영하지 못했습니다. 코드에서 확인한 기능은 설명하되, 화면을 합성하거나 과거 캡처를 최신 화면으로 표시하지 않았습니다.

| 필요한 캡처 | 확인할 내용 | 현재 처리 |
| --- | --- | --- |
| 관리자 콘솔 | 인원 현황 진입 버튼 | 기존 `images/10_admin_console.png`는 10/21 촬영본으로 유지 |
| `/admin/staffing` | 38명·8부서, 총원/현재 근무/배정 가능, 15초 갱신 | 본문 기능·권한·API만 반영. 실제 캡처 미추가 |
| 요청 상세 | 판단 evidence와 `reference_amm` 별도 패널, AMM 번호·SDR ID·인용 맥락 | 과거 근거 화면은 역사 기록으로 표시. 새 패널 재촬영 필요 |

다음에 앱 환경이 준비되면 위 세 화면을 새 파일로 촬영하고 본문 캡션·PDF를 함께 갱신하면 됩니다. 이번 문서 갱신을 위해 DB 볼륨 초기화·덤프 복원·새 평가를 실행하지 않았습니다.

## 생성·검증

HTML은 Python 표준 라이브러리로 생성합니다. 평가 SHA256을 확인하고 `summary.json`에서 주요 수치·경로·MCP trace 표를 채웁니다. `source/draw_diagrams.py`는 기존 색상에 맞춘 편집 가능한 SVG 네 장을 만듭니다.

```bash
python3 final-report/source/build_report.py
```

PDF는 Chrome과 `puppeteer-core`를 사용합니다. 렌더링 도구는 저장소 밖에 설치합니다. 개정 시 사용한 버전은 puppeteer-core 25.16.0입니다. Node 22.12 이상과 로컬 Chrome이 필요하며 다른 OS에서는 `CHROME_PATH`로 실행 파일을 지정합니다. 원본 글꼴은 macOS의 Apple SD Gothic Neo를 우선 사용하므로 다른 환경에서는 페이지 수·줄바꿈을 다시 확인해야 합니다.

```bash
npm install --prefix /tmp/mro-report-render puppeteer-core@25.16.0
node final-report/source/render_report.mjs \
  /tmp/mro-report-render/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js
```

생성 후 PDF 전체 페이지를 이미지로 렌더링해 잘림·빈 페이지·표 분리·도식 가독성을 확인합니다. 원본 `raw/`, `v1/`, 기존 캡처와 `images/v1/`, 평가 번들의 체크섬은 변경하지 않습니다.

이번 개정 검증: 하위 에이전트의 AI·MCP/DB·평가/UI 교차 검토를 반영했고, 원자료 체크섬·평가 재집계·이미지 경로·전체 PDF 페이지 렌더링을 확인했습니다. PDF는 24쪽이며, 반복 표 머리글과 페이지 번호를 포함합니다.
