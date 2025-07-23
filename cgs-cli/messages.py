# cgs-cli/messages.py

MESSAGES = {
    "en": {
        "DEPLOY_START": "Starting server deployment...",
        "DEPLOY_SUCCESS": "✅ Deployment successful!",
        "DEPLOY_FAILED": "❌ Deployment failed:",
        "DESTROY_START": "⚠️ Destroying all resources...",
        "DESTROY_CONFIRM": "Are you sure you want to destroy all resources? This action cannot be undone.",
        "DESTROY_ABORTED": "Aborted.",
        "DESTROY_SUCCESS": "✅ All resources have been destroyed.",
        "DESTROY_FAILED": "❌ Destroy failed:",
        "INFO_FETCHING": "Fetching server info...",
        "INFO_IP_ADDRESS": "Server IP Address:",
        "INFO_FAILED": "❌ Could not get server info. Is the server deployed?",
        "LOGS_CONNECTING": "Connecting to server to stream logs... (Press Ctrl+C to exit)",
        "LOGS_FAILED": "❌ Log streaming failed:",
        "TERRAFORM_NOT_FOUND": "❌ Terraform command not found. Is it installed and in your PATH?",
        "SSH_NOT_FOUND": "❌ ssh command not found. Is OpenSSH client installed?",
    },
    "ko": {
        "DEPLOY_START": "서버 배포를 시작합니다...",
        "DEPLOY_SUCCESS": "✅ 배포에 성공했습니다!",
        "DEPLOY_FAILED": "❌ 배포에 실패했습니다:",
        "DESTROY_START": "⚠️ 모든 리소스를 삭제합니다...",
        "DESTROY_CONFIRM": "정말로 모든 리소스를 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.",
        "DESTROY_ABORTED": "작업이 중단되었습니다.",
        "DESTROY_SUCCESS": "✅ 모든 리소스가 삭제되었습니다.",
        "DESTROY_FAILED": "❌ 리소스 삭제에 실패했습니다:",
        "INFO_FETCHING": "서버 정보를 가져오는 중...",
        "INFO_IP_ADDRESS": "서버 IP 주소:",
        "INFO_FAILED": "❌ 서버 정보를 가져올 수 없습니다. 서버가 배포되었나요?",
        "LOGS_CONNECTING": "원격 서버에 연결하여 로그를 스트리밍합니다... (Ctrl+C를 눌러 종료)",
        "LOGS_FAILED": "❌ 로그 스트리밍에 실패했습니다:",
        "TERRAFORM_NOT_FOUND": "❌ Terraform 명령어를 찾을 수 없습니다. 설치되어 있고 PATH에 등록되어 있나요?",
        "SSH_NOT_FOUND": "❌ ssh 명령어를 찾을 수 없습니다. OpenSSH 클라이언트가 설치되어 있나요?",
    }
}