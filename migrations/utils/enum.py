from typing import Iterable, Sequence
from alembic import op


def set_enum_values(enum_name: str, new_values: Iterable[str], references: Iterable[Sequence[str]]):
    """

    @param enum_name: Системное наименование enum
    @param new_values: Новые значения enum
    @param references: Упоминания enum в моделях

    Example:
        set_enum_values('promo_type_enum', (
            'BEST_OFFER',
            'NEW_PRODUCT',
            'NO_PROMOTION',
        ), [('advertisement_sale_package', 'promo_type')])
    """
    query_str = f"""
            ALTER TYPE {enum_name} RENAME TO {enum_name}_old;
            CREATE TYPE {enum_name} AS ENUM({', '.join(f"'{value}'" for value in new_values)});
            """
    for reference in references:
        query_str += f"""
            ALTER TABLE {reference[0]} ALTER {reference[1]} DROP DEFAULT;
            ALTER TABLE {reference[0]} ALTER COLUMN {reference[1]} TYPE {enum_name} USING {reference[1]}::text::{enum_name};
        """
    query_str += f"""DROP TYPE {enum_name}_old;"""
    for q in query_str.split(';')[:-1]:
        op.execute(q)
