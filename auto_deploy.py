import paramiko
import sys
import os

# ── CONFIG — reads from env vars when run in GitHub Actions ──────────────────
EC2_HOST  = os.environ.get("EC2_HOST",  "YOUR-EC2-PUBLIC-IP")
EC2_USER  = os.environ.get("EC2_USER",  "ubuntu")
KEY_PATH  = os.environ.get("KEY_PATH",  os.path.expanduser("~/.ssh/deploy_key.pem"))
REPO_URL  = "https://github.com/tejasbargujepatil/aws-codebuild-multilang.git"
CLONE_DIR = "/home/ubuntu/projects"
REPO_NAME = "aws-codebuild-multilang"
# ─────────────────────────────────────────────────────────────────────────────


def run_command(client, command, description=""):
    if description:
        print(f"\n{'='*50}")
        print(f"  {description}")
        print(f"{'='*50}")

    print(f"$ {command}")
    stdin, stdout, stderr = client.exec_command(command)

    for line in stdout:
        print(line.strip())

    errors = stderr.read().decode().strip()
    if errors:
        print(f"[STDERR] {errors}")

    exit_code = stdout.channel.recv_exit_status()
    print(f"[exit code: {exit_code}]")
    return exit_code


def connect_ssh():
    print(f"\n🔌 Connecting to {EC2_USER}@{EC2_HOST} ...")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname     = EC2_HOST,
            username     = EC2_USER,
            key_filename = KEY_PATH,
            timeout      = 10
        )
        print(f"✅ Connected to {EC2_HOST}")
        return client
    except FileNotFoundError:
        print(f"❌ Key file not found: {KEY_PATH}")
        sys.exit(1)
    except paramiko.AuthenticationException:
        print("❌ Authentication failed — check your key and username")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)


def deploy():
    client = connect_ssh()

    try:
        run_command(client, "git --version", "Checking Git")

        run_command(
            client,
            "which git || (sudo apt update -y && sudo apt install -y git)",
            "Installing Git if needed"
        )

        run_command(client, f"mkdir -p {CLONE_DIR}", "Creating projects directory")

        print(f"\n{'='*50}")
        print("  Checking if repo already exists")
        print(f"{'='*50}")

        _, stdout, _ = client.exec_command(
            f"test -d {CLONE_DIR}/{REPO_NAME}/.git && echo 'EXISTS' || echo 'NOT_FOUND'"
        )
        result = stdout.read().decode().strip()

        if result == "EXISTS":
            print("📦 Repo exists — pulling latest changes...")
            run_command(
                client,
                f"cd {CLONE_DIR}/{REPO_NAME} && git pull origin main",
                "Pulling latest changes"
            )
        else:
            print("📥 Fresh clone...")
            run_command(
                client,
                f"cd {CLONE_DIR} && git clone {REPO_URL}",
                "Cloning repository"
            )

        run_command(
            client,
            f"ls -la {CLONE_DIR}/{REPO_NAME}/",
            "Repo contents on EC2"
        )

        run_command(
            client,
            f"cd {CLONE_DIR}/{REPO_NAME} && git log --oneline -3",
            "Last 3 commits"
        )

        print(f"\n{'='*50}")
        print(f"  ✅ DEPLOYMENT COMPLETE")
        print(f"  Repo is at: {CLONE_DIR}/{REPO_NAME}")
        print(f"{'='*50}\n")

    finally:
        client.close()
        print("🔌 SSH connection closed.")


if __name__ == "__main__":
    deploy()
