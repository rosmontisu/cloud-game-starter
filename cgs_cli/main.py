import typer
from rich.console import Console
import subprocess
import os
import locale
import sys
from pathlib import Path
from .messages import MESSAGES # messages.py
TERRAFORM_DIR = Path(__file__).parent / "terraform"


def get_system_language():
    """
    시스템의 기본 언어 코드를 반환합니다 ('ko', 'en')
    윈도우, macOS, 리눅스 모두에서 동작하도록 설계되었습니다.
    감지 실패 시 'en'을 반환합니다.
    """
    try:
        # 1. 윈도우 환경
        if sys.platform == "win32":
            import ctypes
            # 윈도우 API를 직접 호출하여 사용자 기본 UI 언어 ID를 가져옴
            windll = ctypes.windll.kernel32
            lang_id = windll.GetUserDefaultUILanguage()
            lang_map = {
                0x0409: 'en', 0x0c09: 'en', 0x0809: 'en',   # 영어(미국, 호주, 영국)
                0x0412: 'ko', 0x0812: 'ko',                 # 한국어
                0x0411: 'ja',                               # 일본어
                0x0804: 'zh',                               # 중국어(간체)
            }
            if lang_id in lang_map:
                return lang_map[lang_id]

        # 2. 유닉스 계열(macOS, Linux)
        # 환경 변수를 먼저 확인
        for env_var in ['LANG', 'LC_MESSAGES', 'LC_ALL', 'LANGUAGE']:
            if env_var in os.environ:
                return os.environ[env_var].split('.')[0].split('_')[0] # 'ko_KR.UTF-8' -> 'ko'
        
        # 3. locale.getlocale()
        locale_info = locale.getlocale()
        if locale_info and locale_info[0]:
            lang_code = locale_info[0].split('_')[0].lower() # 'ko_KR', 'UTF-8' -> 'ko'
            if 'korean' in lang_code: return 'ko' # 'Korean_Korea' -> 'korean' -> 'ko'
            if 'english' in lang_code: return 'en'
            if 'japanese' in lang_code: return 'ja'
            return lang_code

    except Exception:
        pass
    # 위 모든 방법으로 실패 시, 기본값 'en' 반환
    return 'en'

lang = get_system_language()
if lang not in MESSAGES:
    lang = 'en'

msg = MESSAGES[lang] # 딕셔너리에서 선택한 land으로 불러오기
console = Console() # rich console 객체 (예쁘게 출력하는거)
app = typer.Typer() # Typer app


@app.command()
def deploy():
    """
    Terraform을 사용하여 클라우드에 게임 서버를 배포합니다.
    """
    console.print(f"[bold blue]{msg['DEPLOY_START']}[/bold blue]")
    try:
        # 1 init, 출력 숨김
        console.print("  - [yellow]Initializing Terraform...[/yellow]")
        init_command = ["terraform", "init", "-upgrade"]
        subprocess.run(init_command, check=True, cwd=TERRAFORM_DIR, capture_output=True)

        # 2 Terraform 배포 apply, 출력 허용
        console.print("  - [yellow]Applying infrastructure plan...[/yellow]")
        apply_command = ["terraform", "apply", "-auto-approve"]
        subprocess.run(apply_command, check=True, cwd=TERRAFORM_DIR)
        
        console.print(f"[bold green]{msg['DEPLOY_SUCCESS']}[/bold green]")
        info() # 배포 성공 후 자동으로 서버 정보 출력
        
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.decode() if e.stderr else (e.stdout.decode() if e.stdout else "No error output.")
        console.print(f"❌ [bold red]{msg['DEPLOY_FAILED']}[/bold red]")
        console.print(f"  [italic]Failed command: {' '.join(e.cmd)}[/italic]")
        console.print(f"  [italic]Error details:[/italic]")
        # 에러 메시지를 좀 더 보기 좋게 들여쓰기 중
        # 중간에 멈추면 그냥 다시 시작하라고 정보 출력
        console.print("\n💡 [bold yellow]Tip:[/bold yellow] Please check the error message above and resolve the issue.")
        console.print("   Once resolved, you can run [cyan]`cgs deploy`[/cyan] again to continue the deployment.")
        console.print(f"  > {error_output.strip().replace('\n', '\n  > ')}")
    except FileNotFoundError:
        console.print(f"[bold red]{msg['TERRAFORM_NOT_FOUND']}[/bold red]")




@app.command()
def destroy():
    """
    배포된 모든 클라우드 리소스를 삭제합니다.
    """
    console.print(f"[bold yellow]{msg['DESTROY_START']}[/bold yellow]")
    if not typer.confirm(msg['DESTROY_CONFIRM']):
        console.print(msg['DESTROY_ABORTED'])
        raise typer.Abort()
    
    try:
        subprocess.run(["terraform", "destroy", "-auto-approve"], check=True, cwd=TERRAFORM_DIR)
        console.print(f"[bold green]{msg['DESTROY_SUCCESS']}[/bold green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]{msg['DESTROY_FAILED']}[/bold red] {e}")


@app.command()
def info():
    """
    배포된 서버의 공인 IP 주소를 출력합니다.
    """
    console.print(f"[bold blue]{msg['INFO_FETCHING']}[/bold blue]")
    try:
        result = subprocess.run(["terraform", "output", "-raw", "server_public_ip"], 
                                capture_output=True, text=True, check=True, cwd=TERRAFORM_DIR)
        ip_address = result.stdout.strip()
        console.print(f"[bold]{msg['INFO_IP_ADDRESS']}[/bold] [yellow]{ip_address}[/yellow]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]{msg['INFO_FAILED']}[/bold red]")

@app.command()
def logs(
    # typer.Option을 사용해 --key-path 라는 옵션으로 .pem 경로를 받기
    key_path: str = typer.Option(..., "--key-path", "-i", help="Path to your .pem private key file.")
):
    """
    원격 서버의 로그를 실시간으로 스트리밍합니다.
    """
    console.print(f"[bold blue]{msg['LOGS_CONNECTING']}[/bold blue]")
    
    # 1. 서버 IP 가져오기
    try:
        result = subprocess.run(["terraform", "output", "-raw", "server_public_ip"], 
                                capture_output=True, text=True, check=True, cwd=TERRAFORM_DIR)
        ip_address = result.stdout.strip()
        if not ip_address:
            console.print(f"[bold red]{msg['INFO_FAILED']}[/bold red]")
            raise typer.Abort()
    except subprocess.CalledProcessError:
        console.print(f"[bold red]{msg['INFO_FAILED']}[/bold red]")
        raise typer.Abort()

    # 2. SSH 명령 실행
    ssh_command = [
        "ssh",
        "-i", key_path,
        f"ec2-user@{ip_address}",
        "tail -f /home/ec2-user/server.log" # 실시간으로 로그를 보기 위한 명령어
    ]
    
    try:
        subprocess.run(ssh_command, check=True) # 이 프로세스는 사용자가 Ctrl+C를 누를 때까지 계속 실행
    except FileNotFoundError:
        console.print(f"[bold red]{msg['SSH_NOT_FOUND']}[/bold red]")
    except subprocess.CalledProcessError as e:
        # 사용자가 Ctrl+C로 종료한 경우가 아니면 에러 출력
        if e.returncode != 130: # 130은 Ctrl+C 종료 코드
             console.print(f"[bold red]{msg['LOGS_FAILED']}[/bold red] {e}")

             

if __name__ == "__main__":
    app()