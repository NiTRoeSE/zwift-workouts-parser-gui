import os,platform


def get_latest_git_tag():
    try:
        git_tag = os.popen("git describe --tags --abbrev=0").read().strip()
    except:
       pass
    #print(git_tag)

    if git_tag == '':
        git_tag = "0.0.0"
    return git_tag

def get_git_commit_id():
    git_hash = os.popen("git rev-parse HEAD").read().strip()
    return git_hash



sr_version = get_latest_git_tag()
git_commit = get_git_commit_id()

# this file is used in optiosn about modal to display information
with open("versions.py", "w") as f:
    f.write(f"sr_version='{sr_version}'\n")
    f.write(f"commit='{git_commit}'")

if platform.system() == 'Windows':
    os.system(f'flet build windows --copyright "NiTRoSoft" --project "ZWP"  --company "NiTRoSoft" --build-version {sr_version}')
else:
    os.system(f'flet build macos --copyright "NiTRoSoft" --project "ZWP"  --company "NiTRoSoft" --build-version {sr_version}')