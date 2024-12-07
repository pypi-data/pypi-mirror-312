from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy import text

import pytest
import tomli


@pytest.fixture(scope="session")
def it_conn_url():
    config_file = Path(__file__).parent / "integ.toml"
    if not config_file.exists():
        raise ValueError(f"{config_file} does not exist")
    config = tomli.load(open(config_file, "rb"))
    p = config["connection"]
    return (
        f"clickzetta://{p['username']}:{p['password']}@"
        f"{p['instance']}.{p['service']}/{p['workspace']}"
        f"?schema={p['schema']}&vcluster={p['vcluster']}"
    )


def test_select_expr(it_conn_url):
    engine = create_engine(it_conn_url)
    sql = text("select abs(42)")
    with engine.connect() as conn:
        rows = conn.execute(sql).fetchall()
    assert len(rows) == 1
    assert rows[0][0] == 42
