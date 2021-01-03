import pytest

from sqlalchemy import func

from log_it.extensions import db
from log_it.user.model import TRole
from log_it.fixtures import roles


def get_scalar_result(engine, sql):
    result_proxy = engine.execute(sql)
    result = result_proxy.scalar()
    result_proxy.close()
    engine.dispose()
    return result


@pytest.fixture(scope="class")
def testdb(request, testdb_engine):
    request.cls.testdb = testdb_engine


@pytest.mark.usefixtures("testdb", "populated_db")
class TestDatabaseCreation(object):
    # def index_exists(self, table_name, index_name):
    #     if self.testdb.dialect.name == "postgresql":
    #         text = (
    #             "SELECT 1 FROM pg_indexes WHERE schemaname = 'public' AND "
    #             f"tablename='{table_name}' AND indexname='{index_name}'"
    #         )
    #         return bool(get_scalar_result(self.testdb, text))
    #     else:
    #         pass

    # @pytest.mark.parametrize(
    #     "view, index_name",
    #     [
    #         (MVCustomerSearch, "idx_fts_customer_search"),
    #         (MVDeviceSearch, "idx_fts_device_search"),
    #         (MVModelSearch, "idx_fts_model_search"),
    #         (MVTestsheetSearch, "idx_fts_testsheet_search"),
    #     ],
    # )
    # def test_view_index(self, view, index_name):
    #     assert self.index_exists(view.__tablename__, index_name)

    def test_populate_roles(self):
        (count,) = db.session.query(func.count(TRole.ixRole)).one()
        assert count == len(roles.fixture)
