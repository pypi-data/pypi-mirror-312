from typing import Sequence

import ibis
import pandas as pd

from ibis import _, literal, desc, asc

import ibis.selectors as s

CON = ibis.duckdb.connect()


def col(name):
    return getattr(_, name)


def lit(val, dtype=None):
    return literal(val, type=dtype)


class DataFrame:
    def __init__(self, data, expr=None):
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        if expr is None:
            self.expr = CON.read_in_memory(data)
        else:
            self.expr = expr

    @property
    def columns(self):
        return list(self.expr.as_table().schema().names)

    def select(self, *exprs, **named_exprs):
        self.expr = self.expr.select(*exprs, **named_exprs)
        return self

    def head(self, n=5):
        self.expr = self.expr.head(n)
        return self

    def collect(self):
        return self.expr.execute()

    def with_columns(self, *exprs, **named_exprs):
        self.expr = self.expr.mutate(*exprs, **named_exprs)
        return self

    def drop_nulls(
        self,
        subset: Sequence[str] | str | None = None,
    ):
        self.expr = self.expr.drop_null(subset=subset)
        return self

    def drop(self, *fields: str):
        self.expr = self.expr.drop(*fields)
        return self

    def filter(self, *predicates):
        return DataFrame(None, expr=self.expr.filter(*predicates))

    def gather_every(self, n, offset=0):
        self.expr = self.expr.limit(n, offset)
        return self

    def write_parquet(self, path):
        return self.expr.to_parquet(path)

    def unpivot(self, on, index, variable_name="variable", value_name="value"):
        if isinstance(on, list):
            on = s.cols(*on)

        if isinstance(index, list):
            keep = [*index, variable_name, value_name]
        else:
            keep = [index, variable_name, value_name]

        if on is None:
            on = ~s.cols(*index) if isinstance(index, list) else ~s.cols(index)

        self.expr = self.expr.pivot_longer(
            on, names_to=variable_name, values_to=value_name
        ).drop(~s.cols(*keep))
        return self

    def sort(self, *fields, descending=False):
        if isinstance(descending, list):
            fields = [
                desc(field) if direction else asc(field)
                for field, direction in zip(fields, descending)
            ]
        else:
            fields = [desc(field) if descending else asc(field) for field in fields]

        self.expr = self.expr.order_by(*fields)
        return self

    def join(
        self,
        df_right,
        on=None,
        left_on=None,
        right_on=None,
        how="inner",
        suffix="_right",
    ):
        if on is not None:
            if not isinstance(on, list):
                on = [on]
            predicates = on
        elif left_on is not None and right_on is not None:
            if not isinstance(left_on, list):
                left_on = [left_on]

            if not isinstance(right_on, list):
                right_on = [right_on]

            predicates = list(zip(left_on, right_on))
        else:
            predicates = ()

        return DataFrame(
            None,
            expr=self.expr.join(
                df_right.expr, predicates, how=how, rname=f"{{name}}{suffix}"
            ),
        )

    def join_asof(
        self,
        df_right,
        on=None,
        left_on=None,
        right_on=None,
        by=None,
        by_left=None,
        by_right=None,
        strategy="backward",
    ):
        import operator as op

        if on is not None:
            left_col = self.expr[on]
            right_col = df_right.expr[on]
        elif left_on is not None and right_on is not None:
            left_col = self.expr[left_on]
            right_col = df_right.expr[right_on]
        else:
            raise ValueError()

        if strategy == "backward":
            on = op.ge(left_col, right_col)
        elif strategy == "forward":
            on = op.le(left_col, right_col)

        if by is not None:
            if not isinstance(by, list):
                by = [by]
            predicates = by
        elif by_left is not None and by_left is not None:
            if not isinstance(by_left, list):
                by_left = [by_left]

            if not isinstance(by_right, list):
                by_right = [by_right]

            predicates = list(zip(by_left, by_right))
        else:
            predicates = ()

        return DataFrame(
            None, expr=self.expr.asof_join(df_right.expr, on=on, predicates=predicates)
        )

    def write_csv(self, path):
        return self.expr.to_csv(path)

    def unique(self, subset, keep="first"):
        return DataFrame(None, expr=self.expr.distinct(on=subset, keep=keep))

    def to_arrow(self):
        return self.expr.to_pyarrow()

    def to_dict(self, as_series=True):
        orient = "series" if as_series else "list"
        return self.expr.execute().to_dict(orient=orient)

    def sample(self, fraction=None):
        return DataFrame(None, expr=self.expr.sample(fraction=fraction))

    def pipe(self, fun):
        return fun(self)

    def is_empty(self):
        return len(self.expr.execute()) == 0

    def rename(self, method):
        if isinstance(method, dict):
            method = {v: k for k, v in method.items()}

        return DataFrame(None, expr=self.expr.rename(method))
