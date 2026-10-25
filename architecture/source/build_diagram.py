"""MRO Agent 최종 AWS 구성도 생성기.

공식 아이콘(aws-icons: AWS Architecture Icons, @iconify-json/logos: 기술 로고)을 SVG 안에 직접 넣어
외부 이미지 없이 그려지는 단일 HTML을 만듭니다. 모든 연결선은 아이콘 중심선에 맞춘 직각 경로입니다.
사용: python -I build_final.py <scratchpad 경로>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
AWS = ROOT / "dl-aws" / "package" / "icons"
LOGOS = json.loads((ROOT / "dl-logos" / "package" / "icons.json").read_text(encoding="utf-8"))
OUT = ROOT / "mro-architecture.html"

_uid = 0


def _prefix_ids(body):
    """같은 로고를 여러 번 넣어도 gradient id가 겹치지 않게 합니다."""
    global _uid
    _uid += 1
    p = f"i{_uid}-"
    body = re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', body)
    body = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{p}{m.group(1)})", body)
    body = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{p}{m.group(1)}"', body)
    return body


def aws(path, x, y, size):
    s = (AWS / f"{path}.svg").read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", s, flags=re.S)
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}">{_prefix_ids(inner)}</svg>'


def logo(name, x, y, size):
    i = LOGOS["icons"][name]
    w, h = i.get("width", LOGOS.get("width", 16)), i.get("height", LOGOS.get("height", 16))
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 {w} {h}">{_prefix_ids(i["body"])}</svg>'


# 타일: 56×56 아이콘, 라벨 기준선은 중심 + 46, 라벨 아래에서 나가는 선은 중심 + 54에서 시작
T, H = 56, 28
LABEL_DY = 46
BELOW = 54


def badge(spec, cx, cy):
    """아이콘 오른쪽 위 모서리의 작은 기술 로고."""
    kind, src = spec
    bx, by = cx + 22, cy - 22
    inner = logo(src, bx - 9, by - 9, 18) if kind == "logo" else aws(src, bx - 9, by - 9, 18)
    return f'<circle cx="{bx}" cy="{by}" r="12" fill="#fff" stroke="#d5dbe1" stroke-width="1.2"/>' + inner


def tile(kind, src, cx, cy, label, badge_spec=None):
    x, y = cx - H, cy - H
    if kind == "aws":
        out = aws(src, x, y, T)
    elif kind == "logo":
        out = logo(src, x, y, T)
    elif kind == "ecs":  # ECS Fargate 서비스: 주황 테두리 안에 기술 로고
        out = (f'<rect x="{x}" y="{y}" width="{T}" height="{T}" rx="8" fill="#fff" stroke="#ed7100" stroke-width="1.8"/>'
               + logo(src, cx - 19, cy - 19, 38))
    else:  # task: 1회성 ECS 태스크
        out = (f'<rect x="{x}" y="{y}" width="{T}" height="{T}" rx="8" fill="#fff" stroke="#ed7100" stroke-width="1.8"/>'
               + aws("resource/AmazonElasticContainerServiceTask", cx - 20, cy - 20, 40))
    if badge_spec:
        out += badge(badge_spec, cx, cy)
    return out + f'<text class="tl" x="{cx}" y="{cy + LABEL_DY}" text-anchor="middle">{label}</text>'


def group(x, y, w, h, icon, label, stroke, fill="none", dash=None, label_color=None, icon_size=32, label_x=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{d}/>'
    out += aws(icon, x, y, icon_size)
    lx = label_x if label_x is not None else x + icon_size + 8
    return out + f'<text class="gl" x="{lx}" y="{y + icon_size / 2 + 5}" fill="{label_color or stroke}">{label}</text>'


def wire(d):
    return f'<path class="wire" d="{d}" marker-end="url(#ar)"/>'


def note(x, y, text, anchor="middle", cls="als"):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{text}</text>'


# ---------- 격자 ----------
# 열
XU, XE, XS3, XGH = 70, 220, 470, 300          # 사용자, 엣지, S3 dashboard·Actions, GitHub
X0, X1, X2, X3 = 630, 760, 890, 1020          # ALB·grafana, backend·prometheus, MQ, ai·EFS
X4, X5, X6 = 1170, 1320, 1450                 # MCP, RDS·db-init, rag-restore·NAT
XR1, XR2, XX = 1600, 1720, 1895               # 리전 오른쪽 2열, 외부
# 행
YCI, YS, YA, YC, Y2 = 100, 330, 520, 770, 950  # CI, S3·ECR 행, public subnet, 요청 처리 행, 아래 행
YR53 = 670
YB, YR = YC - 70, YC + 70                      # business-mcp, rag-mcp
LANE = 650                                     # backend → RDS 경로

parts = []
P = parts.append

# ---------- 그룹 ----------
P(group(140, 190, 1665, 880, "architecture-group/AWSCloudlogo", "AWS Cloud", "#232f3e", icon_size=40))
P(group(300, 240, 1485, 810, "architecture-group/Region", "ap-northeast-2", "#00a4a6", dash="4 3"))
P(group(540, 410, 985, 620, "architecture-group/VirtualprivatecloudVPC", "VPC 10.20.0.0/16", "#8c4fff"))
P(group(555, 450, 955, 135, "architecture-group/Publicsubnet", "Public subnet", "#7aa116",
        fill="#f2f6e8", label_color="#3f6b0a", icon_size=28))
P(group(555, 600, 955, 415, "architecture-group/Privatesubnet", "Private subnet · ECS Fargate", "#00a4a6",
        fill="#e6f6f7", label_color="#00777a", icon_size=28, label_x=X0 + 16))

# ---------- 타일 ----------
P(tile("logo", "github-icon", XGH, YCI, "GitHub"))
P(tile("logo", "github-actions", XS3, YCI, "GitHub Actions"))
P(tile("aws", "resource/Users", XU, YA, "사용자"))
P(tile("aws", "architecture-service/AmazonCloudFront", XE, YA, "CloudFront · WAF", ("aws", "architecture-service/AWSWAF")))
P(tile("aws", "architecture-service/AmazonRoute53", XE, YR53, "Route 53"))
P(tile("aws", "architecture-service/AmazonSimpleStorageService", XS3, YS, "S3 dashboard", ("logo", "vue")))

P(tile("aws", "resource/ElasticLoadBalancingApplicationLoadBalancer", X0, YA, "ALB"))
P(tile("aws", "resource/AmazonVPCNATGateway", X6, YA, "NAT Gateway"))

P(tile("ecs", "spring-icon", X1, YC, "backend"))
P(tile("aws", "architecture-service/AmazonMQ", X2, YC, "Amazon MQ", ("logo", "rabbitmq-icon")))
P(tile("ecs", "python", X3, YC, "ai", ("logo", "fastapi-icon")))
P(tile("ecs", "python", X4, YB, "business-mcp"))
P(tile("ecs", "python", X4, YR, "rag-mcp"))
P(tile("aws", "architecture-service/AmazonRDS", X5, YC, "RDS PostgreSQL", ("logo", "postgresql")))
P(tile("task", None, X6, YC, "rag-restore"))

P(tile("ecs", "grafana", X0, Y2, "grafana"))
P(tile("ecs", "prometheus", X1, Y2, "prometheus"))
P(tile("aws", "architecture-service/AmazonEFS", X3, Y2, "Amazon EFS"))
P(tile("task", None, X5, Y2, "db-init"))

P(tile("aws", "architecture-service/AmazonElasticContainerService", XR1, YS, "Amazon ECS",
       ("aws", "architecture-service/AWSFargate")))
P(tile("aws", "architecture-service/AmazonElasticContainerRegistry", XR2, YS, "Amazon ECR"))
P(tile("aws", "architecture-service/AmazonSimpleStorageService", XR1, YC, "S3 rag-data"))
P(tile("aws", "architecture-service/AWSSecretsManager", XR2, YC, "Secrets Manager"))
P(tile("aws", "architecture-service/AmazonCloudWatch", XR1, Y2, "CloudWatch"))
P(tile("aws", "architecture-service/AmazonSimpleStorageService", XR2, Y2, "S3 tfstate", ("logo", "terraform-icon")))

P(tile("logo", "docker-icon", XX, YS, "Docker Hub"))
P(tile("logo", "openai-icon", XX, YA, "OpenAI API"))

# ---------- 연결선 ----------
# CI/CD
P(wire(f"M{XGH + H},{YCI} H{XS3 - H}") + note((XGH + XS3) / 2, YCI - 10, "PR · merge"))
P(wire(f"M{XS3},{YCI + BELOW} V{YS - H}") + note(XS3 + 8, 222, "dist 업로드", anchor="start"))
P(wire(f"M{XS3 + H},{YCI} H{XR1} V{YS - H}"))
P(wire(f"M{XS3 + H},{YCI} H{XR2} V{YS - H}"))
P(logo("terraform-icon", XR1 - 84, 149, 18) + note(XR1 - 8, 163, "Deploy", anchor="end", cls="al"))
P(note(XR2 + 8, 163, "Push Image", anchor="start", cls="al"))
P(wire(f"M{XR2 - H},{YS} H{XR1 + H}") + note((XR1 + XR2) / 2, YS - 8, "pull"))
P(wire(f"M{XX - H},{YS} H{XR2 + H}"))

# 사용자 → 엣지
P(wire(f"M{XU + H},{YA} H{XE - H}") + note(166, YA - 10, "HTTPS"))
P(wire(f"M{XU},{YA + BELOW} V{YR53} H{XE - H}") + note(166, YR53 - 10, "DNS"))
P(wire(f"M{XE},{YA - H} V{YS} H{XS3 - H}") + note(262, YS - 10, "/* · OAC"))
P(wire(f"M{XE + H},{YA} H{X0 - H}") + note(420, YA - 10, "/api/* · /grafana*"))

# ALB → backend, grafana (한 줄에서 갈라짐)
P(wire(f"M{X0},{YA + BELOW} V{YC} H{X1 - H}") + note((X0 + X1 - H) / 2, YC - 8, ":8080"))
P(wire(f"M{X0},{YA + BELOW} V{Y2 - H}") + note(X0 + 8, Y2 - 60, ":3000", anchor="start"))

# 정비 요청 처리: backend ⇄ MQ ⇄ ai → MCP → RDS
P(wire(f"M{X1 + H},{YC - 7} H{X2 - H}") + note((X1 + X2) / 2, YC - 16, "실행 요청"))
P(wire(f"M{X2 - H},{YC + 7} H{X1 + H}") + note((X1 + X2) / 2, YC + 25, "결과 이벤트"))
P(wire(f"M{X2 + H},{YC - 7} H{X3 - H}") + note((X2 + X3) / 2, YC - 16, "소비"))
P(wire(f"M{X3 - H},{YC + 7} H{X2 + H}") + note((X2 + X3) / 2, YC + 25, "이벤트 발행"))
XF = (X3 + H + X4 - H) // 2
XJ = (X4 + H + X5 - H) // 2
P(wire(f"M{X3 + H},{YC} H{XF} V{YB} H{X4 - H}"))
P(wire(f"M{X3 + H},{YC} H{XF} V{YR} H{X4 - H}") + note(XF - 6, YC - 42, "툴 호출", anchor="end"))
P(wire(f"M{X4 + H},{YB} H{XJ} V{YC} H{X5 - H}"))
P(wire(f"M{X4 + H},{YR} H{XJ} V{YC} H{X5 - H}") + note(XJ + 6, YC - 42, "읽기 전용", anchor="start"))
P(wire(f"M{X1},{YC - H} V{LANE} H{X5} V{YC - H}") + note((X1 + X5) / 2, LANE - 8, "읽기·쓰기"))

# RDS 데이터 준비 (1회성)
P(wire(f"M{X6 - H},{YC} H{X5 + H}") + note((X5 + X6) / 2 + 4, YC - 9, "RAG 복원"))
P(wire(f"M{XR1 - H},{YC} H{X6 + H}"))
P(wire(f"M{X5},{Y2 - H} V{YC + BELOW}") + note(X5 + 8, 880, "계정 생성", anchor="start"))

# 모니터링 · 저장
P(wire(f"M{X0 + H},{Y2} H{X1 - H}") + note((X0 + X1) / 2, Y2 - 9, "PromQL"))
P(wire(f"M{X1},{Y2 - H} V{YC + BELOW}") + note(X1 + 8, 880, "scrape", anchor="start"))
P(wire(f"M{X3},{YC + BELOW} V{Y2 - H}") + note(X3 + 8, 880, "/data", anchor="start"))

# 아웃바운드
P(wire(f"M{X6 + H},{YA} H{XX - H}") + note((XR1 + XR2) / 2, YA - 10, "LLM · 임베딩"))

svg_body = "\n".join(parts)

html = f"""<title>MRO Agent AWS 구성도</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&display=swap">
<style>
/* Layout: 흰 도면 한 장만 (AWS 아키텍처 다이어그램 관례: 그룹 테두리 + 공식 아이콘). 단일 라이트 테마로 고정 */
:root {{
  --paper: #ffffff;
  --ink: #232f3e;
  --font: "IBM Plex Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif;
}}
body {{ background: var(--paper); color: var(--ink); font-family: var(--font); }}
.wrap {{
  padding-block: 24px;
  padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px));
}}
.canvas {{ overflow-x: auto; }}
.canvas svg {{ display: block; width: 100%; min-width: 1400px; max-width: 1960px; height: auto; margin: 0 auto; }}
.tl {{ fill: var(--ink); font-family: var(--font); font-size: 13px; font-weight: 600; }}
.gl {{ font-family: var(--font); font-size: 14px; font-weight: 600; }}
.al {{ fill: var(--ink); font-family: var(--font); font-size: 15px; font-weight: 600; }}
.als {{ fill: var(--ink); font-family: var(--font); font-size: 12px; }}
.wire {{ fill: none; stroke: var(--ink); stroke-width: 1.6; stroke-linejoin: round; }}
</style>

<div class="wrap">
  <div class="canvas">
    <svg viewBox="0 0 1960 1090" role="img" aria-label="항공기 정비요청 Agent AWS 구성도. 사용자 요청은 CloudFront를 거쳐 정적 파일은 S3에서, API와 Grafana는 ALB를 통해 ECS Fargate 서비스로 전달됩니다. backend가 Amazon MQ에 넣은 실행 요청을 ai 워커가 소비해 business-mcp와 rag-mcp로 RDS PostgreSQL을 조회합니다. GitHub Actions가 이미지를 ECR에 올리고 Terraform으로 ECS에 배포합니다.">
      <defs>
        <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" fill="#232f3e"/>
        </marker>
      </defs>
{svg_body}
    </svg>
  </div>
</div>
"""

OUT.write_text(html, encoding="utf-8")
print(OUT, len(html))
