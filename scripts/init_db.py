import duckdb
from pathlib import Path
from common.config_loader import load_config

def get_duckdb_conn():
    config = load_config()
    project_root = Path(__file__).resolve().parents[1]
    db_path = (project_root / config['duckdb']['path']).resolve()
    print(f"使用数据库文件：{db_path}")
    conn = duckdb.connect(str(db_path))
    return conn

def run_sql_file(conn, sql_file: Path):
    print(f"执行 SQL 文件：{sql_file}")
    with sql_file.open("r", encoding="utf-8") as f:
        sql_content = f.read()
        # DuckDB 支持执行多条 SQL 语句
        conn.execute(sql_content)

def init_db():
    conn = get_duckdb_conn()

    # 安装和加载 spatial 扩展
    conn.execute("INSTALL spatial;")
    conn.execute("LOAD spatial;")

    # 依次加载 SQL 文件
    sql_dir = Path(__file__).resolve().parent / "sql"
    sql_files = sorted(sql_dir.glob("*.sql"))  # 按文件名顺序执行

    for sql_file in sql_files:
        run_sql_file(conn, sql_file)
    conn.close()
    print("数据库初始化完成。")


if __name__ == '__main__':
    init_db()