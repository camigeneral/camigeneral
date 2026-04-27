from datetime import datetime
from zoneinfo import ZoneInfo

import gifos
import os
from dotenv import load_dotenv


FONT_FILE = "fonts/gohufont-uni-14.pil"
FONT_FILE_MONA = "fonts/Inversionz.otf"

def make_bar(percent, width=20):
    filled = int(width * percent / 100)
    empty = width - filled
    return "#" * filled + "-" * empty

def main():
    result = load_dotenv()
    print(f"load_dotenv found file: {result}")
    print(f"cwd: {os.getcwd()}")
    print(f"token: {os.getenv('GITHUB_TOKEN')}")

    # Initialize terminal (width, height, padding, font, fps)
    t = gifos.Terminal(750, 500, 15, 15, FONT_FILE, 15)

    # Initial delay (empty frames)
    t.gen_text("", 1, count=20)

    # Disable cursor for BIOS animation
    t.toggle_show_cursor(False)

    # Current year (used in BIOS text)
    year_now = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).strftime("%Y")

    t.toggle_show_cursor(False)
    t.gen_text("\x1b[93mCAMI-OS v00.12.17\x1b[0m", 1, count=5)

    # Login simulation
    t.gen_text("login: ", 3, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("camigeneral", 3, contin=True)

    t.gen_text("", 4, count=5)
    t.toggle_show_cursor(False)

    t.gen_text("password: ", 4, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("*********", 4, contin=True)

    t.toggle_show_cursor(False)

    # Last login timestamp
    time_now = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).strftime(
        "%a %b %d %I:%M:%S %p %Z %Y"
    )
    t.gen_text(f"Last login: {time_now}", 6)

    # Simulate typing "clear" command with correction
    t.gen_prompt(7, count=5)
    prompt_col = t.curr_col

    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mclea", 7, contin=True)  # typo
    t.delete_row(7, prompt_col)  # erase typo
    t.gen_text("\x1b[92mclear\x1b[0m", 7, count=3, contin=True)
    t.clone_frame(8)  # short pause

    # Fetch GitHub stats
    ignore_repos = ["archiso-zfs", "archiso-zfs-archive"]
    git_user_details = gifos.utils.fetch_github_stats("camigeneral", ignore_repos)

    # Calculate age (used as "uptime")
    user_age = gifos.utils.calc_age(17, 12, 2000)

    # Clear screen → stats view
    t.clear_frame()

    # Extract top languages
    top_languages = [lang[0] for lang in git_user_details.languages_sorted]

    # Multiline formatted "neofetch-style" block
    user_details_lines = f"""
    \x1b[96m\x1bCamila General - Software engineering student - UBA\x1b[0m
    """

    contact_details_lines = f"""
    \x1b[96mEmail:      \x1b[93mcgeneral@fi.uba.ar\x1b[0m
    \x1b[96mLinkedIn:   \x1b[93mcamigen\x1b[0m
    """

    stats_details_lines = f"""
    \x1b[96mTotal Contributions: \x1b[93m{git_user_details.total_contributions}\x1b[0m
    \x1b[96mTotal PRs: \x1b[93m{git_user_details.total_pull_requests_made}\x1b[0m
    \x1b[96mCurrent streak: \x1b[93m{git_user_details.current_streak} days\x1b[0m
    \x1b[96mLongest streak: \x1b[93m{git_user_details.longest_streak} days\x1b[0m
    """


    # Simulate running whoami
    t.gen_prompt(1)
    prompt_col = t.curr_col
    t.clone_frame(10)

    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mwhoami", 1, contin=True)

    t.gen_text(user_details_lines, 1, 1, count=5, contin=True)


    # Simulate running contact info
    t.gen_prompt(t.curr_row)
    prompt_col = t.curr_col
    t.clone_frame(10)

    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mcat contact.txt", t.curr_row, contin=True)

    t.gen_text(contact_details_lines, 4, 1, count=5, contin=True)


    # Simulate running fetch script
    t.gen_prompt(t.curr_row)
    prompt_col = t.curr_col
    t.clone_frame(10)

    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mfetch", t.curr_row, contin=True)
    t.delete_row(t.curr_row, prompt_col)
    t.gen_text("\x1b[92mfetch\x1b[0m", t.curr_row, contin=True)
    t.gen_typing_text(" --github-stats", t.curr_row, contin=True)

    t.gen_text(stats_details_lines, 8, 1, count=5, contin=True)


    # Simulate running languages
    t.gen_prompt(t.curr_row)
    prompt_col = t.curr_col
    t.clone_frame(10)

    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mcat languages.txt", t.curr_row, contin=True)

    start_row = 15

    top = git_user_details.languages_sorted[:4]
    total = sum(p for _, p in top)

    normalized_top = []
    for lang, p in top:
        new_p = round((p / total) * 100)
        normalized_top.append((lang, new_p))

    diff = 100 - sum(p for _, p in normalized_top)
    lang, p = normalized_top[0]
    normalized_top[0] = (lang, p + diff)

    for i, (lang, percent) in enumerate(normalized_top):
        for p in range(0, int(percent)+1, 4):
            bar = make_bar(p)
            line = f"\x1b[96m{lang:<12}\x1b[0m [{bar}] \x1b[93m{p:3d}%\x1b[0m"

            t.delete_row(start_row + i)
            t.gen_text(line, start_row + i, 5, contin=True)

        bar = make_bar(percent)
        line = f"\x1b[96m{lang:<12}\x1b[0m [{bar}] \x1b[93m{percent:3d}%\x1b[0m"
        t.delete_row(start_row + i)
        t.gen_text(line, start_row + i, 5, contin=True)


    # Final message
    t.gen_prompt(t.curr_row+2)
    t.gen_typing_text(
        "\x1b[92m# Have a nice day! Thanks for stopping by :)",
        t.curr_row,
        contin=True,
    )


    # Ending delay
    t.gen_text("", t.curr_row, count=120, contin=True)


    # Generate GIF
    t.gen_gif()


if __name__ == "__main__":
    main()