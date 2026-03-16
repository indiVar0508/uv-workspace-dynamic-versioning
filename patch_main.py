import re
with open('src/uv_workspace_dynamic_versioning/vendored/main.py', 'r') as f:
    text = f.read()

# patch 1: add path argument to _get_version
text = text.replace('def _get_version(config: schemas.UvDynamicVersioning) -> Version:', 'def _get_version(config: schemas.UvDynamicVersioning, project_dir: Path) -> Version:')

# patch 2: add path to Version.from_vcs
text = text.replace('config.vcs,', 'config.vcs,\n            path=project_dir,')

# patch 3: add path argument to get_version
text = text.replace('def get_version(config: schemas.UvDynamicVersioning) -> tuple[str, Version]:', 'def get_version(config: schemas.UvDynamicVersioning, project_dir: Path) -> tuple[str, Version]:')

# patch 4: call _get_version with project_dir
text = text.replace('got = _get_version(config)', 'got = _get_version(config, project_dir)\n    got = patch_version_for_directory(got, project_dir)')

# patch 5: inject patch_version_for_directory function before _get_version
patch_code = """
import subprocess
def patch_version_for_directory(version: Version, path: Path) -> Version:
    matched_tag = getattr(version, "_matched_tag", None)
    
    try:
        if matched_tag:
            rev_list_cmd = ["git", "rev-list", f"{matched_tag}..HEAD", "--", str(path)]
            out = subprocess.check_output(rev_list_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL).strip()
            distance = len(out.splitlines()) if out else 0
            
            log_cmd = ["git", "log", "-1", "--format=%H", f"{matched_tag}..HEAD", "--", str(path)]
            commit_out = subprocess.check_output(log_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL).strip()
        else:
            rev_list_cmd = ["git", "rev-list", "HEAD", "--", str(path)]
            out = subprocess.check_output(rev_list_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL).strip()
            distance = len(out.splitlines()) if out else 0
            
            log_cmd = ["git", "log", "-1", "--format=%H", "HEAD", "--", str(path)]
            commit_out = subprocess.check_output(log_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL).strip()

        if commit_out:
            commit_length = len(version.commit) if version.commit else 7
            version.commit = commit_out[:commit_length]
            version.distance = distance
        else:
            version.distance = 0

        status_cmd = ["git", "status", "--porcelain", "--", str(path)]
        status_out = subprocess.check_output(status_cmd, cwd=path, text=True, stderr=subprocess.DEVNULL).strip()
        version.dirty = bool(status_out)
    except Exception:
        pass
        
    return version

"""
text = text.replace('def _get_version', patch_code + 'def _get_version')

with open('src/uv_workspace_dynamic_versioning/vendored/main.py', 'w') as f:
    f.write(text)
