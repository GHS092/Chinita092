import sys
import re

file_path = "hermes-agent-main-original/hermes_state.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add _repair_attempted_paths
if "_repair_attempted_paths" not in content:
    content = re.sub(
        r"logger = logging\.getLogger\(__name__\)",
        "logger = logging.getLogger(__name__)\n\n_repair_attempted_paths = set()",
        content,
        count=1
    )

# 2. Add functions
funcs = """

def is_malformed_db_error(exc: Exception) -> bool:
    import sqlite3
    if not isinstance(exc, sqlite3.DatabaseError):
        return False
    msg = str(exc).lower()
    return "malformed database schema" in msg or "database disk image is malformed" in msg

def repair_state_db_schema(db_path) -> dict:
    import shutil
    import sqlite3
    report = {"repaired": False, "strategy": None, "backup_path": None, "error": None}
    try:
        backup_path = db_path.with_name(f"{db_path.name}.corrupt.bak")
        shutil.copy2(db_path, backup_path)
        report["backup_path"] = str(backup_path)
        
        # Repair strategy: remove duplicate messages_fts entries
        conn = sqlite3.connect(str(db_path))
        conn.execute("PRAGMA writable_schema=ON")
        conn.execute("DELETE FROM sqlite_master WHERE name='messages_fts' AND rowid NOT IN (SELECT min(rowid) FROM sqlite_master WHERE name='messages_fts')")
        conn.execute("DELETE FROM sqlite_master WHERE name='messages_fts_trigram' AND rowid NOT IN (SELECT min(rowid) FROM sqlite_master WHERE name='messages_fts_trigram')")
        conn.commit()
        conn.execute("PRAGMA writable_schema=OFF")
        conn.execute("VACUUM")
        conn.close()
        
        report["repaired"] = True
        report["strategy"] = "dedup_schema"
    except Exception as e:
        report["error"] = str(e)
    return report

class SessionDB:"""

if "def repair_state_db_schema" not in content:
    content = content.replace("class SessionDB:", funcs)

# 3. Patch __init__
orig_catch = """        except Exception as exc:
            # Capture the cause so /resume and friends can surface WHY the"""

new_catch = """        except sqlite3.DatabaseError as exc:
            if is_malformed_db_error(exc):
                if self.db_path not in _repair_attempted_paths:
                    _repair_attempted_paths.add(self.db_path)
                    logger.error("state.db is malformed; attempting automatic repair...")
                    report = repair_state_db_schema(self.db_path)
                    if report.get("repaired"):
                        logger.warning(f"state.db was successfully repaired! Backup: {report.get('backup_path')}")
                        self._conn = sqlite3.connect(
                            str(self.db_path),
                            check_same_thread=False,
                            timeout=1.0,
                            isolation_level=None,
                        )
                        self._conn.row_factory = sqlite3.Row
                        apply_wal_with_fallback(self._conn, db_label="state.db")
                        self._conn.execute("PRAGMA foreign_keys=ON")
                        self._init_schema()
                    else:
                        logger.error(f"state.db repair failed: {report.get('error')}")
                        _set_last_init_error(f"{type(exc).__name__}: {exc}")
                        raise
                else:
                    _set_last_init_error(f"{type(exc).__name__}: {exc}")
                    raise
            else:
                _set_last_init_error(f"{type(exc).__name__}: {exc}")
                raise
        except Exception as exc:
            # Capture the cause so /resume and friends can surface WHY the"""

if "is_malformed_db_error(exc):" not in content:
    content = content.replace(orig_catch, new_catch)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Patched hermes_state.py successfully.")
