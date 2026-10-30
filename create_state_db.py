import sqlite3

conn = sqlite3.connect("state.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS nodes (
    id TEXT PRIMARY KEY,
    name TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS relationships (
    source_id TEXT,
    relationship TEXT,
    target_id TEXT
)
""")

cur.executemany(
    "INSERT OR IGNORE INTO nodes (id, name) VALUES (?, ?)",
    [
        ("daas-trade-manager", "DAAS Trade Manager"),
        ("kafka", "Kafka"),
        ("sql-server", "SQL Server"),
        ("security-master", "Security Master"),
        ("openshift", "OpenShift"),
    ],
)

cur.executemany(
    "INSERT INTO relationships (source_id, relationship, target_id) VALUES (?, ?, ?)",
    [
        ("daas-trade-manager", "USES", "kafka"),
        ("daas-trade-manager", "STORES_IN", "sql-server"),
        ("daas-trade-manager", "CALLS", "security-master"),
        ("daas-trade-manager", "RUNS_ON", "openshift"),
    ],
)

conn.commit()
conn.close()

print("Created state.db")
