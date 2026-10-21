import os
import subprocess
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


def run_git_command(args: list[str]) -> str:
    """Executes a git command and handles errors cleanly."""
    try:
        res = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: git {' '.join(args)}")
        print(e.stderr.strip())
        sys.exit(1)


def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set in .env")
        sys.exit(1)

    # 1. Check working directory status
    status = run_git_command(["status", "--porcelain"])
    if not status:
        print("Working tree clean. Nothing to commit.")
        return

    # 2. Stage changes
    run_git_command(["add", "-A"])
    diff = run_git_command(["diff", "--cached"])

    if not diff:
        print("No staged changes detected.")
        return

    diff_summary = diff[:6000]

    # 3. Generate commit message via Gemini
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-3.8-flash",
        google_api_key=api_key,
        temperature=0.2,
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an automated Git assistant. Write a concise, conventional commit message based on the staged diff. Return ONLY the commit message text. Do not wrap in quotes or code blocks.",
        ),
        ("human", "Generate a commit message for this diff:\n\n{diff}"),
    ])

    print("Generating commit message with Gemini...")
    chain = prompt | llm
    response = chain.invoke({"diff": diff_summary})
    commit_msg = response.content.strip().replace('"', '\\"')

    print(f"Commit message: {commit_msg}")

    # 4. Commit changes
    run_git_command(["commit", "-m", commit_msg])

    # 5. Push to current branch
    current_branch = run_git_command(["branch", "--show-current"])
    print(f"Pushing to origin/{current_branch}...")
    run_git_command(["push", "origin", current_branch])

    print("Successfully synced to GitHub.")


if __name__ == "__main__":
    main()
