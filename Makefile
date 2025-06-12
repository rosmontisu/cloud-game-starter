# .PHONY 지시어는 이 타겟들이 실제 파일이 아니라 항상 실행되어야 하는 가상의 명령어 집합임을 나타냄 (이름이 실제 파일과 충돌하지 않도록 함)
.PHONY: init deploy destroy info

# Terraform 초기화
init:
	terraform init

# 인프라 배포
deploy:
	terraform apply -auto-approve

# 인프라 삭제
destroy:
	terraform destroy -auto-approve

# 배포 정보 확인
info:
	terraform output server_public_ip