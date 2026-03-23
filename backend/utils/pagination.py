from sqlalchemy.orm import Query


def apply_pagination(query: Query, limit: int | None, offset: int | None) -> Query:
    """Apply optional limit and offset to a SQLAlchemy query."""
    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)
    return query
