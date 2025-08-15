# ☁️ Cloud Game Starter (CGS)

<p align="center">
</p>

<p align="center">
  <strong>Deploy your game server to the cloud with a single command.</strong>
  <br />
  An open-source automation tool for students, indie developers, and everyone new to the cloud.
</p>

<p align="center">
  <!-- Language Switcher -->
  Also available in: <a href="README.ko.md">🇰🇷 한국어</a>
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

## What's the Problem? (Why CGS?)

"I want to test my multiplayer game, but AWS is too complex and intimidating."
"How do I deploy a server, find its IP, and safely delete it afterward to avoid surprise bills?"

Cloud Game Starter is here to solve these problems. Let CGS handle the complex cloud settings and tedious repetitive tasks, so you can focus on what truly matters: developing your game.

## ✨ Features

*   **One-Command Deployment:** Automatically create and deploy a test game server on AWS with a single command line.
*   **Real-time Log Streaming:** Monitor your remote server's logs in real-time from your local machine for easy debugging.
*   **Safe Resource Destruction:** Cleanly delete all created cloud resources with one command, eliminating the fear of unexpected costs.
*   **Template-Based:** Designed to be extensible, allowing easy addition of sample servers in various languages like Go, C#, etc. (Currently supports Go).

## 🚀 Getting Started

Deploy your first game server in less than 10 minutes.

### 1. Prerequisites

Before you begin, ensure you have the following tools installed on your computer:

*   ✅ **An AWS Account:** The cloud account where your server will be created.
*   ✅ **Python (3.8+):** Required to run the CGS CLI tool.
*   ✅ **Terraform:** The tool CGS uses internally to build infrastructure. ([Official Installation Guide](https://developer.hashicorp.com/terraform/downloads))
*   ✅ **AWS CLI:** The tool that connects your computer to your AWS account. ([Official Installation Guide](https://aws.amazon.com/cli/))

### 2. Installation & Setup

#### STEP 1: Install `cgs-cli`

Open your terminal (PowerShell, Command Prompt, or Terminal on Mac/Linux) and install CGS with this simple command:

```bash
pip install cgs-cli
```

Once installed, the `cgs` command will be available system-wide. Verify the installation by running:

```bash
cgs --help
```
> If you see a list of commands and options, the installation was successful.

#### STEP 2: Configure AWS Credentials

You need to grant CGS permission to manage resources in your AWS account.

1.  **Create an IAM Access Key:** In your AWS Console, create an **Access Key ID** and a **Secret Access Key** for programmatic access. (For security, we strongly recommend using keys from an IAM User, not your root account.)

2.  **Configure AWS CLI:** Run the following command in your terminal and enter your key information.

    ```bash
    aws configure
    ```
    ```
    AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
    AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
    Default region name [None]: ap-northeast-2  (Seoul region is recommended)
    Default output format [None]:               (Just press Enter)
    ```

#### STEP 3: Prepare an SSH Key (for the `logs` command)

To use the `cgs logs` command for real-time log streaming, you need a "secret key" to access the server.

1.  **Create a Key Pair:** In your AWS Console > EC2 > Key Pairs, **create a new key pair**.
2.  **Download the `.pem` file:** When creating the key, **download the `.pem` file** and store it in a safe, memorable location on your computer (e.g., `D:\Keys\my-aws-key.pem`).

### 3. The Workflow

You're all set! Follow this simple workflow to manage your server.

#### STEP 1: Deploy the Server (`deploy`)

Deploy the default Go echo server to the cloud.

```bash
cgs deploy
```
> Starting server deployment...  
> ✅ Deployment successful!

*Deployment takes about 2-3 minutes.*

#### STEP 2: Get Server Info (`info`)

Check the IP address of your deployed server.

```bash
cgs info
```
> Fetching server info...  
> Server IP Address: 54.180.xx.xx

#### STEP 3: Connect and Test

It's time to connect to your server with your game client or a simple test tool.

*   **Windows (PowerShell):**
    ```powershell
    Test-NetConnection -ComputerName 54.180.xx.xx -Port 7777
    ```
    > `TcpTestSucceeded : True` means the connection is successful!

*   **macOS / Linux (Terminal):**
    ```bash
    nc 54.180.xx.xx 7777
    ```
    > If the cursor is blinking, the connection is successful. Type any text, and the server will echo it back.

#### STEP 4: Stream Real-time Logs (`logs`)

See what's happening on your server in real-time. Provide the path to the `.pem` key file you downloaded in Step 3 of the setup.

```bash
cgs logs --key-path "D:\Keys\my-aws-key.pem"
```
> 📡 Connecting to server to stream logs... (Press Ctrl+C to exit)  
> 2024/05/15 10:30:00 Server started on port 7777  
> 2024/05/15 10:31:15 Client connected from ...

#### STEP 5: Destroy the Server (`destroy`) (Very Important!)

When you're done testing, **you must destroy the server** to prevent any further charges.

```bash
cgs destroy
```
> ⚠️ Destroying all resources...  
> Are you sure you want to destroy all resources? ... [y/N]: y  
> ✅ All resources have been destroyed.

--- 

### System Architecture
![Cloud Game Starter Architecture Diagram](https://raw.githubusercontent.com/rosmontisu/cloud-game-starter/main/.github/assets/architecture-diagram.png)

---

## 🗺️ Roadmap

Cloud Game Starter is just getting started. We have ambitious plans to evolve this tool into an even more powerful utility for developers. Your ideas and contributions are always welcome!

### Short-term Goals

Our immediate focus is on enhancing the core functionality and expanding support.

*   [x] Package and release the CLI tool on PyPI
*   [ ] Add support for C# (.NET) sample servers for Unity developers
*   [ ] Implement a CI/CD pipeline (with GitHub Actions) to ensure code stability and automate testing

### Mid/Long-term Vision

Looking ahead, we aim to make CGS a more versatile and comprehensive platform.

*   [ ] Support for other major cloud providers (GCP, Azure)
*   [ ] Introduce a container-based deployment option (Docker + AWS ECS/Fargate)
*   [ ] Provide templates for simple database integration

> 💡 Have an idea or interested in a specific feature? Feel free to open a discussion in our [GitHub Issues](https://github.com/rosmontisu/cloud-game-starter/issues)!

## 🤝 Contributing

Contributions are welcome! Whether it's bug reports, feature suggestions, or code contributions, any form of participation is appreciated.

## 📝 License

This project is licensed under the [MIT License](LICENSE).
