"""Build the report HTML from its existing template and immutable evaluation bundle.

Run from any directory: python3 final-report/source/build_report.py
No API, DB, credentials or third-party Python package is required.
"""
from html import escape
from pathlib import Path
import hashlib
import json
import re
import subprocess

REPORT = Path(__file__).resolve().parents[1]
BUNDLE = REPORT.parent / 'evaluations/2026-10-23-isolated-200'
# Validate source integrity before copying any metrics into the current report.
for line in (BUNDLE / 'SHA256SUMS').read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    source = BUNDLE / name.lstrip('*')
    if hashlib.sha256(source.read_bytes()).hexdigest() != digest:
        raise ValueError(f'Evaluation checksum mismatch: {name}')
s = json.loads((BUNDLE / 'summary.json').read_text())
p = json.loads((REPORT / 'source/provenance.json').read_text())
o = s['overall']
a = o['automatic_assignment_precision']

def table(headers, rows):
    return '<table><tr>' + ''.join(f'<th>{escape(str(x))}</th>' for x in headers) + '</tr>\n' + '\n'.join('<tr>' + ''.join(f'<td>{escape(str(x))}</td>' for x in row) + '</tr>' for row in rows) + '</table>'

def metric(m):
    return f"{m['count']}/{m['total']} ({m['percent']}%)"

metrics = table(['지표', '결과'], [
    ['전체 평가 통과', metric(o['label_agreement'])],
    ['자동배정 중 평가 통과', metric(a)],
    ['배정 기대 사례의 통과', metric(o['assignable_case_success'])],
    ['사람 검토 기대 사례의 보류', metric(o['human_review_recall'])],
    ['최종 사람 검토', f"{o['human_review_count']}/{s['cases']}"],
    ['보류 사유', ' · '.join(f'{k} {v}' for k,v in o['human_review_reasons'].items())],
    ['LLM2 마지막 부서 일치 (배정 기대·출력 존재)', metric(s['llm2_department_agreement'])],
    ['LLM2 부서는 일치했으나 최종 보류', f"{s['correct_llm2_department_held']}건 · 통과에 미합산"],
    ['평균 / 중앙값 / P95', f"{o['sum_request_seconds']/s['cases']:.2f}초 / {o['median_seconds']}초 / {o['p95_seconds']}초"],
    ['접수 실패·타임아웃 / SYSTEM_ERROR', f"{o['client_timeout_or_submission_failure']} / {o['system_error_results']}"],
    ['접수 검증 (별도 실행)', metric(s['validation'])],
])
metrics += table(['경로','사례','통과 자동배정','실패 자동배정','사람 검토'],[
    [name, *(r[k] for k in ['cases','passed_assignments','failed_assignments','human_review'])]
    for name,r in [('LLM1 직접',s['routes']['llm1_direct']),('LLM2·3 조사·검토',s['routes']['llm23'])]
])
ids={'get_request_context':'B01','get_aircraft_history':'B02','search_departments':'B03','search_jasc_codes':'R01','search_sdr_cases':'R02','get_evidence':'R05','get_sdr_amm_references':'SDR→AMM'}
tool_rows = [[node, ' · '.join(f'{ids[k]} {v}' for k,v in calls.items() if k in ids)] for node,calls in s['tool_calls_by_node'].items()]
provenance='<table><tr><th>대상</th><th>기준·출처</th></tr>'
for repo,sha in p['repositories'].items():
    provenance+=f'<tr><td>{escape(repo)}</td><td><a href="https://github.com/mro-agent-proj/{repo}/commit/{sha}">{sha}</a></td></tr>'
provenance+='</table>'
values={
 'pass_count':o['label_agreement']['count'],'pass_rate':o['label_agreement']['percent'],
 'auto_precision':a['percent'],'auto_pass':a['count'],'assigned':a['total'],
 'auto_fail':o['incorrect_automatic_assignments'],'auto_rate':f"{a['total']/s['cases']*100:.1f}",
 'human':o['human_review_count'],'avg':f"{o['sum_request_seconds']/s['cases']:.2f}",'p95':o['p95_seconds'],
 'trace_rows':(REPORT/'raw/trace_rows.html').read_text(),
 'auth_evidence':escape((REPORT/'raw/auth_evidence.txt').read_text()),
 'dlq_evidence':escape((REPORT/'raw/dlq_evidence.txt').read_text()),
 'evaluation_tables':metrics,'tool_table':table(['노드','도구별 trace 수'],tool_rows),
 'provenance_table':provenance,
}
html=(REPORT/'final_report.template.html').read_text()
for key,value in values.items():
    html=html.replace('{{'+key+'}}',str(value))
# Repeat the first row on continued tables and keep headers with their data.
html=re.sub(r'(<table\b[^>]*>\s*)(<tr>.*?</tr>)',r'\1<thead>\2</thead>',html,flags=re.S)
if re.search(r'\{\{.*?\}\}',html): raise ValueError('Unresolved template placeholder')
for src in re.findall(r'<img\b[^>]*src="([^"]+)"',html):
    if not (REPORT/src).is_file(): raise FileNotFoundError(src)
subprocess.run(['python3',str(REPORT/'source/draw_diagrams.py')],check=True)
output=REPORT/'항공기_정비요청_Agent_최종결과보고서.html'
output.write_text(html)
print(f'Built {output.name}; evaluation checksums and image references verified.')
