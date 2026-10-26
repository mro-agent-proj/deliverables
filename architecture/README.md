# AWS 아키텍처 다이어그램

[infra](https://github.com/mro-agent-proj/infra) 레포 Terraform으로 정의한 최종 배포 구성입니다.

![AWS 아키텍처](aws-architecture.png)

| 파일 | 내용 |
| --- | --- |
| `aws-architecture.png` | 보고서·발표용 이미지 (4000×2280) |
| `aws-architecture.html` | 원본. 브라우저로 열면 확대해도 선명합니다 (아이콘 내장, 글꼴만 Google Fonts) |

## 읽는 법

- **요청 처리:** 사용자 → CloudFront(WAF) → ALB → backend → Amazon MQ → ai → business-mcp / rag-mcp → RDS
- **배포:** GitHub Actions가 이미지를 ECR에 올리고(Push Image), infra 레포에서만 `terraform apply`로 ECS에 배포(Deploy)
- **1회성 작업:** db-init(DB 계정), rag-restore(S3 rag-data → RDS)
- 주황 테두리는 ECS Fargate 서비스, 작은 원은 그 위에서 쓰는 기술입니다.

기준: infra 레포 `fd0e8e4` 이후 구성 (2026-10-26). 아직 AWS에 배포하지 않았고 `terraform validate`까지 확인한 정의입니다.

## 출처

생성 스크립트(`source/build_diagram.py`)는 정리했으며 커밋 [`4236b47`](https://github.com/mro-agent-proj/deliverables/tree/4236b47/architecture/source)에서 볼 수 있습니다.

아이콘 출처: [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/)(aws-icons 패키지), 기술 로고는 [gilbarbara/logos](https://github.com/gilbarbara/logos)(@iconify-json/logos, CC0). 각 로고는 해당 프로젝트·회사의 상표입니다.
