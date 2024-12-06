from pathlib import Path
from .ultilities import make_dir
import pandas as pd
import polars as pl
from concurrent.futures import ThreadPoolExecutor
from time import sleep, perf_counter
from datetime import timedelta
import trino
import os
from rich import print
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    SpinnerColumn
)


class DataPipeLine:
    def __init__(
            self,
            query: str,
            count_rows: bool = False,
            use_polars: bool = True,
    ):
        self.query = f"SELECT COUNT(*) FROM ({query})" if count_rows else query
        self.use_polars = use_polars or count_rows
        self.count_rows = count_rows
        self.df = None
        self.status = '[bright_blue]🤖 JDBC[/bright_blue]'

    def debug_query(self):
        print(self.query)

    def _records_to_df(self, records, columns: list):
        if self.use_polars:
            self.df = pl.DataFrame(records, orient='row', schema=columns)
        else:
            self.df = pd.DataFrame(records, columns=columns)

        # message
        message = (
            f"Total rows: {self.df.to_numpy()[0][0]:,.0f}" if self.count_rows
            else f"Data Shape: ({self.df.shape[0]:,.0f}, {self.df.shape[1]})"
        )
        return message

    def export_df(self, save_path: Path, file_name: str):
        make_dir(save_path.parent)
        if self.count_rows:
            self.df = self.df.rename({'_col0': file_name})
            self.df.write_ndjson(save_path.parent / f'log_count_{file_name}.json')
        elif self.use_polars:
            self.df.write_parquet(save_path)
        else:
            self.df.to_parquet(save_path, index=False, compression='zstd')

    def run_presto_to_df(
            self,
            save_path: Path = None,
            verbose: bool = True,
            file_name: str = '',
    ):
        username, password = os.environ['PRESTO_USER'], os.environ['PRESTO_PASSWORD']
        conn = trino.dbapi.connect(
            host='presto-secure.data-infra.shopee.io',
            port=443,
            user=username,
            catalog='hive',
            http_scheme='https',
            source=f'(50)-(vnbi-dev)-({username})-(jdbc)-({username})-(SG)',
            auth=trino.auth.BasicAuthentication(username, password)
        )
        cur = conn.cursor()

        # verbose
        start = perf_counter()
        print(f"{self.status} Starting: Query file [{file_name}], Count rows: [{self.count_rows}]")
        if verbose:
            thread = ThreadPoolExecutor(1)
            async_result = thread.submit(cur.execute, self.query)

            progress_bar = Progress(
                TextColumn("{task.description}"),
                SpinnerColumn("simpleDots"),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                BarColumn(),
                TextColumn("•"),
                TimeElapsedColumn(),
                transient=True
            )
            with progress_bar as progress:
                task = progress.add_task("[cyan]Presto to Local", total=100)
                while not async_result.done():
                    memory = cur.stats.get('peakMemoryBytes', 0) * 10 ** -9
                    perc = 0
                    stt = cur.stats.get('state', 'Not Ready')
                    if stt == "RUNNING":
                        perc = round((cur.stats.get('completedSplits', 1e-3) * 100.0) / (cur.stats.get('totalSplits', 0)), 2)
                    status = f"{self.status} {stt} - Memory {memory:,.0f}GB"
                    progress.update(task, description=status, advance=perc)
                    sleep(5)
        else:
            cur.execute(self.query)
        records = cur.fetchall()

        # result
        columns = [i[0] for i in cur.description]
        text = self._records_to_df(records, columns)
        if save_path:
            self.export_df(save_path, file_name)

        # log
        duration = timedelta(seconds=(perf_counter() - start))
        message = f"{self.status} Finish in: {str(duration).split('.')[0]}, {text}"
        print(message)
        return self.df
