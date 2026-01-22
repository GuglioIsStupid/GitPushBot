import subprocess
import dotenv
import os

dot_env = dotenv.find_dotenv()
dotenv.load_dotenv(dot_env)

PREFIX = dotenv.get_key(dot_env, 'PREFIX')
REPO_DIR = dotenv.get_key(dot_env, 'REPO_DIR')

name = "push"

async def run(client, message, args):
    if not message.author.guild_permissions.administrator:
        await message.channel.send("burger")
        return
    
    file_path = None
    commit_message = None
    full_path = None

    if len(args) >= 1 and os.path.isfile(os.path.join(REPO_DIR, args[0])):
        file_path = args[0]
        commit_message = " ".join(args[1:]) if len(args) > 1 else None
        full_path = os.path.join(REPO_DIR, file_path)

    elif message.reference:
        ref = await message.channel.fetch_message(message.reference.message_id)

        if ref.attachments:
            attachment = ref.attachments[0]

            file_path = args[0] if args else attachment.filename
            commit_message = " ".join(args[1:]) if len(args) > 1 else None
            full_path = os.path.join(REPO_DIR, file_path)

            try:
                subprocess.run(["git", "pull"], cwd=REPO_DIR, check=True)
            except subprocess.CalledProcessError as e:
                await message.channel.send(f"Failed to pull latest changes:\n```{e}```")
                return
            
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            await attachment.save(full_path)

        elif ref.content.strip():
            if not args:
                await message.channel.send(
                    f"Please provide a filename when replying to text. Usage: `{PREFIX}push filename commit message`"
                )
                return

            file_path = args[0]
            commit_message = " ".join(args[1:]) if len(args) > 1 else None
            full_path = os.path.join(REPO_DIR, file_path)

            try:
                subprocess.run(["git", "pull"], cwd=REPO_DIR, check=True)
            except subprocess.CalledProcessError as e:
                await message.channel.send(f"Failed to pull latest changes!!!!:\n```{e}```")
                return

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(ref.content)

    if not file_path:
        await message.channel.send("Please provide a file path or reply to a message.")
        return

    if not commit_message:
        await message.channel.send("Please provide a commit message.")
        return

    if not os.path.isfile(full_path):
        await message.channel.send(f"File not found: `{file_path}`")
        return

    try:
        subprocess.run(["git", "add", file_path], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "push"], cwd=REPO_DIR, check=True)

        await message.channel.send(
            f"Pushed `{file_path}`\n`{commit_message}`"
        )
    except subprocess.CalledProcessError as e:
        await message.channel.send(f"WHAT THE FUCXK!!!!!!!!!:\n```{e}```")
