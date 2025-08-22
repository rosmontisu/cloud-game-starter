# 1. ECR 저장소 생성

resource "aws_ecr_repository" "cgs_repo" {
  name                 = "cgs-game-server-repo" # ECR 저장소 이름
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.cgs_repo.repository_url
}