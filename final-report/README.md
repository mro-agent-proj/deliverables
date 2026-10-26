# 최종 결과보고서

2026-10-26 코드 기준으로 본문·구조도·평가 표를 갱신했습니다. 기존 A4 HTML의 표지, 6개 장, 색상, 글꼴, 표 형식을 유지했습니다. 새 화면 3장은 글자를 읽을 수 있도록 한 행에 한 장씩 배치했습니다. AWS 산출물은 이번 변경에서 제외했습니다.

- [PDF · 26쪽](항공기_정비요청_Agent_최종결과보고서.pdf)
- [동일 내용 HTML](항공기_정비요청_Agent_최종결과보고서.html)
- [편집 템플릿](final_report.template.html)
- [기준 버전](source/provenance.json)
- [과거 트러블슈팅과 후속 상태](트러블슈팅.md)

## 기준을 구분해서 읽기

| 대상 | 기준 | 의미 |
| --- | --- | --- |
| 구현 설명·새 구조도 | 2026-10-26 각 서비스 main | LLM e5d3798, backend ff47ad5, agent a30c900, dashboard 99f25f1. integration ebbc10e의 서비스 포인터와 일치 |
| 대표 성능 | [2026-10-23 격리 후 서비스 평가 200건](../evaluations/2026-10-23-isolated-200/README.md) | 기존 결과를 재집계. 이번 문서 개정에서 모델·서비스 평가를 새로 실행하지 않음 |
| 새 관리자 화면 3장 | 2026-10-26 로컬 실행 | 기존 DB 조회. 누적 206건 통계는 평가 200건 지표와 별개 |
| 단위·기능 테스트 | 본문 5.2의 커밋별 GitHub Actions | LLM 186건, agent 일반 46건·1 skip 및 별도 business DB 17건, backend Gradle test·평가 도구 7건, dashboard 타입 검사·빌드 |
| 기존 화면·S10 trace·인증·DLQ·구 시나리오 23건 | 2026-10-21 기존 자료 | 과거 동작 증빙. 현재 성능이나 현재 LLM2 격리 구조의 예시로 사용하지 않음 |

현재 수치는 전체 통과 97/200, 자동배정 중 통과 96/145, 실패 자동배정 49건, 사람 검토 55건입니다. LLM2 부서 일치 71/82와 최종 보류 42건은 별도 지표입니다. 팀 기대 라벨 기준이며 실제 항공 정비 안전성을 입증하는 수치는 아닙니다.

평가 실행 파일 34개 해시와 현재 LLM의 동일 파일이 일치함을 대조했습니다. 평가 `freeze.repositories.ai`는 격리 수정 전 기준 커밋이므로 해당 SHA만으로 당시 실행을 재현할 수 없습니다. 실제 실행 해시·수정 후 커밋·한계는 평가 번들의 manifest/README를 따릅니다.

## 변경한 부분

- LLM2 전용 상태·B02/HISTORY 차단, LLM3 병합·대조, LLM1 맥락 비교를 본문·구조도에 반영.
- MCP 9개, R04 구현, R03 번호 조회, AMM 참고자료 분리, SDR 하이브리드 검색과 모델 범위 확장 반영.
- OpenAI 검색 임베딩 1024차원, Flyway V1~V11, V9 업무 뷰, 수리이력 1,600건·정비 인원 38명 반영.
- 200건 결과·분모·실패 유형·현재 CI를 표로 교체하고 과거 23건 원자료는 보존.
- 설계서의 신고자 조회 API·재조사 분기·임베딩 API 연결을 정정.

## 최신 화면 반영 완료

2026-10-26에 기존 로컬 DB와 Backend·RabbitMQ·business-mcp·rag-mcp·AI 서버, 프런트엔드를 기동하고 관리자 계정으로 조회한 실제 화면을 반영했습니다. 이미지 크기는 각각 2880×2000이며, 원본 파일을 그대로 사용했습니다.

| 캡처 | 확인한 내용 | 본문 |
| --- | --- | --- |
| [관리자 콘솔](images/current/screenshots-20261026/01-admin-console.png) | 인원 현황 진입 버튼, RAG 상태, 누적 요청 통계 | 그림 3-8 |
| [인원 현황](images/current/screenshots-20261026/02-staffing.png) | 8부서·38명, 출근 25·작업 가능 15·작업 불가 10·미출근 13 | 그림 3-9 |
| [SDR 근거와 참고 AMM](images/current/screenshots-20261026/03-evidence-reference-amm.png) | #d380aebd, AMM 참조번호·인용 맥락·SDR ID 별도 패널 | 그림 3-10 |

콘솔 통계는 **누적 206건** 기준이므로 평가 200건 결과와 합산하거나 대체하지 않습니다. AMM 화면도 10/23에 저장된 결과를 조회한 것이며 모델을 새로 호출한 결과가 아닙니다. 인원 화면의 15초 갱신 주기는 코드 근거이고 정지 이미지가 주기 동작 자체를 입증하지는 않습니다.

DB 볼륨 초기화·덤프 복원·업무 데이터 변경·새 평가 없이 촬영했습니다. 기존 컨테이너와 로컬 체크아웃을 사용했으며, 보고서 기준 main과 런타임 소스의 차이가 없음을 대조했습니다. 로컬 체크아웃 커밋, 파일 해시와 화면별 근거는 [provenance.json](source/provenance.json)에 기록했습니다. 10/21 원본 이미지 파일은 보존했습니다.

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

코드·평가 개정에서는 하위 에이전트 교차 검토를 반영했습니다. 이번 화면 갱신에서는 원자료 체크섬·캡처 해시·이미지 경로와 PDF 렌더링을 확인했습니다. PDF는 26쪽이며, 반복 표 머리글과 페이지 번호를 포함합니다.
