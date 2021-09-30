from typing import List, Optional, Union
from airflow.hooks.base import BaseHook
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models import BaseOperator


class MigrationOperator(BaseOperator):
    """
    Custom Operator to move data in batches of a hundred. Can handle larger datasets than the generic transfer operator.
    :param sql: SQL query to execute against the source database. (templated)
    :type sql: str
    :param destination_table: target table. (templated)
    :type destination_table: str
    :param source_conn_id: source connection
    :type source_conn_id: str
    :param destination_conn_id: source connection
    :type destination_conn_id: str
    :param preoperator: sql statement or list of statements to be
        executed prior to loading the data. (templated)
    :type preoperator: str or list[str]
    :param insert_args: extra params for `insert_rows` method.
    :type insert_args: dict
    """

    template_fields = ('sql', 'destination_table', 'preoperator')
    template_ext = (
        '.sql',
        '.hql',
    )
    template_fields_renderers = {"preoperator": "sql"}
    ui_color = '#b0f07c'

    def __init__(
        self,
        *,
        sql: str,
        destination_table: str,
        source_conn_id: str,
        destination_conn_id: str,
        preoperator: Optional[Union[str, List[str]]] = None,
        insert_args: Optional[dict] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.sql = sql
        self.destination_table = destination_table
        self.source_conn_id = source_conn_id
        self.destination_conn_id = destination_conn_id
        self.preoperator = preoperator
        self.insert_args = insert_args or {}

    def execute(self, context):
        source_hook = MySqlHook.get_hook(self.source_conn_id)
        destination_hook = BaseHook.get_hook(self.destination_conn_id)
        offset=0
        while True:
            self.log.info("Extracting data from %s", self.source_conn_id)
            filter="LIMIT 100 OFFSET {};".format(offset)
            final_sql=self.sql+filter
            self.log.info("Executing: \n %s", self.sql+filter)
            results = source_hook.get_records(self.sql+filter)
            
            if results:
                self.log.info("Result: \n %s", results)
                if self.preoperator:
                    self.log.info("Running preoperator")
                    self.log.info(self.preoperator)
                    destination_hook.run(self.preoperator)

                self.log.info("Inserting rows into %s", self.destination_conn_id)
                destination_hook.insert_rows(table=self.destination_table, rows=results, **self.insert_args)
                offset+=100
            else:
                self.log.info("Done, Success!")
                break