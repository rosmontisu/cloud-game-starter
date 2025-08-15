# ☁️ Cloud Game Starter (CGS)

<p align="center">
  <!-- TODO: 추후에 프로젝트 로고등을 추가. -->
  <!-- <img src="PROJECT_LOGO_URL" alt="Cloud Game Starter Logo" width="200"/> -->
</p>

<p align="center">
  <strong>단 하나의 명령어로 클라우드에 게임 서버를 배포하세요.</strong>
  <br />
  학생, 인디 개발자, 그리고 클라우드를 처음 접하는 모든 이를 위한 오픈소스 자동화 툴입니다.
</p>

<p align="center">
  <!-- Language Switcher -->
  Available in: <a href="README.us.md">🇺🇸 English</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/cgs-cli/">
    <img src="https://img.shields.io/pypi/v/cgs-cli" alt="PyPI version">
  </a>
  <a href="https://github.com/rosmontisu/cloud-game-starter/blob/main/LICENSE">
    <img src="https://img.shields.io/pypi/l/cgs-cli" alt="License">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
  </a>
</p>

---

## 무엇을 해결하나요?

"클라우드 서버와의 통신을 테스트하고 싶은데, AWS는 너무 복잡하고 어려워요."
"서버를 어떻게 배포하고, IP는 어떻게 확인하고, 테스트 후엔 어떻게 지워야 요금 폭탄을 피할 수 있죠?"

Cloud Game Starter는 이러한 고민을 해결하기 위해 태어났습니다. 복잡한 클라우드 설정, 지루한 반복 작업은 CGS에게 맡기세요. 여러분은 오직 클라이언트 개발에만 집중할 수 있습니다.

## ✨ 주요 기능

*   **원-커맨드 배포:** 단 한 줄의 명령어로 AWS에 테스트용 샘플 서버를 자동으로 생성하고 배포합니다.
*   **실시간 로그 스트리밍:** 내 컴퓨터에서 원격 서버의 로그를 실시간으로 확인하며 디버깅할 수 있습니다.
*   **안전한 리소스 삭제:** 테스트가 끝난 후, 생성된 모든 클라우드 리소스를 명령어 하나로 깨끗하게 삭제하여 비용 걱정을 덜어줍니다.
*   **확장 가능한 구조:** Go, C# 등 다양한 언어의 샘플 서버를 쉽게 추가하고 선택할 수 있는 구조를 지향합니다. (현재 Go 지원)

## 🚀 시작하기

CGS를 사용하여 첫 번째 게임 서버를 배포하는 데는 10분도 채 걸리지 않습니다.

### 1. 사전 준비 

CGS를 사용하기 전에, 당신의 컴퓨터에 아래의 도구들이 설치되어 있어야 합니다.

*   ✅ **AWS 계정:** 서버가 생성될 클라우드 계정입니다.
*   ✅ **Python (3.8 이상):** CGS 툴을 실행하기 위해 필요합니다.
*   ✅ **Terraform:** CGS가 내부적으로 인프라를 구축할 때 사용하는 도구입니다. ([공식 설치 가이드](https://developer.hashicorp.com/terraform/downloads))
*   ✅ **AWS CLI:** 당신의 컴퓨터와 AWS 계정을 연결해주는 도구입니다. ([공식 설치 가이드](https://aws.amazon.com/ko/cli/))

### 2. 설치 및 초기 설정

#### STEP 1: `cgs-cli` 설치하기

터미널(PowerShell, cmd, 또는 Mac/Linux의 터미널)을 열고 아래의 명령어를 입력하여 CGS를 설치합니다.

```bash
pip install cgs-cli
```

설치가 완료되면, 터미널 어디에서든 `cgs` 명령어를 사용할 수 있게 됩니다. 아래 명령어로 설치를 확인해 보세요.

```bash
cgs --help
```
> `cgs` 명령어 목록과 옵션이 나타나면 성공적으로 설치된 것입니다.

#### STEP 2: AWS 계정 연결하기

CGS가 당신의 AWS 계정에 서버를 만들 수 있도록 '허가증'을 발급해 줘야 합니다.

1.  **IAM 액세스 키 발급:** AWS 콘솔에서 프로그래밍 방식 접근을 위한 **액세스 키 ID**와 **비밀 액세스 키**를 발급받습니다. (보안을 위해 Root 계정 대신 IAM 사용자의 키를 사용하는 것을 권장합니다.)

2.  **AWS CLI 설정:** 터미널에 아래 명령어를 입력하고, 발급받은 키 정보를 순서대로 입력합니다.

    ```bash
    aws configure
    ```
    ```
    AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
    AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
    Default region name [None]: ap-northeast-2  (서울 리전을 추천합니다)
    Default output format [None]:               (그냥 엔터)
    ```

#### STEP 3: SSH 키 준비하기 (`logs` 명령어용)

실시간 로그를 확인하는 `cgs logs` 명령어를 사용하려면, 서버에 접속하기 위한 '비밀 열쇠'가 필요합니다.

1.  **키 페어 생성:** AWS 콘솔 > EC2 > 키 페어 메뉴에서 **새로운 키 페어를 생성**합니다.
2.  **`.pem` 파일 다운로드:** 생성 시 **`.pem` 파일을 다운로드**하여, 당신의 컴퓨터 안전한 곳에 잘 보관합니다. (예: `D:\Keys\my-aws-key.pem`)

### 3. 핵심 사용법

이제 모든 준비가 끝났습니다. 아래의 간단한 워크플로우를 따라 서버를 운영해 보세요.

#### STEP 1: 서버 배포하기 (`deploy`)

Go 언어로 된 기본 에코 서버를 클라우드에 배포합니다.

```bash
cgs deploy
```
> 서버 배포를 시작합니다...  
> ✅ 배포에 성공했습니다!

*배포에는 약 2~3분이 소요됩니다.*

#### STEP 2: 서버 정보 확인하기 (`info`)

배포된 서버의 IP 주소를 확인합니다.

```bash
cgs info
```
> 서버 정보를 가져오는 중...  
>   서버 IP 주소: 54.180.xx.xx

#### STEP 3: 서버에 접속하여 테스트하기

이제 당신의 게임 클라이언트나 간단한 테스트 도구로 서버에 접속할 차례입니다.

*   **Windows (PowerShell):**
    ```powershell
    Test-NetConnection -ComputerName 54.180.xx.xx -Port 7777
    ```
    > `TcpTestSucceeded : True` 가 나오면 연결 성공!

*   **macOS / Linux (터미널):**
    ```bash
    nc 54.180.xx.xx 7777
    ```
    > 커서가 깜빡이면 연결 성공! 아무 글자나 입력하면 서버가 그대로 되돌려줍니다.

#### STEP 4: 실시간 로그 확인하기 (`logs`)

서버에서 어떤 일이 일어나고 있는지 실시간으로 확인합니다. `사전 준비 3단계`에서 다운로드한 `.pem` 키 파일의 경로를 지정해 주세요.

```bash
cgs logs --key-path "D:\Keys\my-aws-key.pem"
```
> 원격 서버에 연결하여 로그를 스트리밍합니다... (Ctrl+C를 눌러 종료)  
> 2024/05/15 10:30:00 Server started on port 7777  
> 2024/05/15 10:31:15 Client connected from ...

#### STEP 5: 서버 파괴하기 (`destroy`) (가장 중요!)

테스트가 끝났다면, 불필요한 비용이 발생하지 않도록 **반드시 서버를 파괴해야 합니다.**

```bash
cgs destroy
```
> ⚠️ 모든 리소스를 삭제합니다...  
> 정말로 모든 리소스를 삭제하시겠습니까? ... [y/N]: y  
> ✅ 모든 리소스가 삭제되었습니다.

--- 

### 시스템 아키텍처
![Cloud Game Starter Architecture Diagram](https://raw.githubusercontent.com/rosmontisu/cloud-game-starter/main/.github/assets/architecture-diagram.png)

---

## 🗺️ 로드맵

Cloud Game Starter는 이제 막 첫걸음을 뗐습니다. 앞으로 아래와 같은 기능들을 추가하여 더욱 강력한 툴로 발전해 나갈 계획입니다. 여러분의 아이디어나 기여는 언제나 환영합니다!

### 단기 목표 

현재 팀의 최우선 목표는 핵심 기능을 강화하고 지원 범위를 확장하는 것입니다.

*   [x] `pip`을 통한 CLI 툴 패키징 및 PyPI 배포
*   [ ] C# (.NET) 샘플 서버 지원 추가 (Unity 개발자 대상)
*   [ ] CI/CD (자동 테스트) 파이프라인 구축으로 안정성 향상

### 중장기 비전 

궁극적으로 CGS를 더욱 다재다능하고 포괄적인 플랫폼으로 만드는 것을 목표로 합니다.

*   [ ] 다른 클라우드 제공사 지원 (GCP, Azure)
*   [ ] 컨테이너 기반 배포 옵션 추가 (Docker + AWS ECS/Fargate)
*   [ ] 간단한 데이터베이스 연동 템플릿 제공

> 💡 특정 기능에 관심이 있거나 좋은 아이디어가 있다면, [GitHub Issues](https://github.com/rosmontisu/cloud-game-starter/issues)에 자유롭게 의견을 남겨주세요!

## 🤝 기여하기

이 프로젝트는 여러분의 기여를 환영합니다! 버그 리포트, 기능 제안, 코드 기여 등 어떤 형태의 참여도 좋습니다.

## 📝 라이선스

이 프로젝트는 [MIT License](LICENSE)를 따릅니다.
