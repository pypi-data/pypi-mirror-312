from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Type, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from pydantic import BaseModel
from sqlalchemy import func
from sqlmodel import select, desc, asc, and_, or_
from sqlmodel.ext.asyncio.session import AsyncSession

from vovo.persistence.models import Page, BaseMongoModel
from vovo.persistence.utils import set_timestamps, apply_operator, mongo_build_sort
from vovo.utils.orm import get_primary_keys

T = TypeVar("T", bound=BaseModel)


class GenericRepository(Generic[T], ABC):
    """Generic base repository."""

    @abstractmethod
    async def get(self, *args: Any, **kwargs: Any) -> T | None:
        """Get a single record by either positional or keyword arguments (or both).

        Args:
            *args (Any): Positional arguments representing values for filtering.
                         The order of arguments should match the expected field order.
            **kwargs (Any): Keyword arguments representing field names and their corresponding values
                            for filtering (e.g., id=1, name="John").

        Returns:
            Optional[T]: Record or None if not found.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_list(self, limit: int = 0, order_by: str | List[str] | None = None, **filters) -> list[T]:
        """Gets a list of records

        Args:
            limit (int): The maximum number of records to return. Default is 0,
                     where 0 means no limit (all records will be returned).
            order_by: 排序规则
            **filters: Filter conditions, several criteria are linked with a logical 'and'.

         Raises:
            ValueError: Invalid filter condition.

        Returns:
            List[T]: List of records.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_page_list(self, page_number: int, page_size: int, order_by: str | List[str] | None = None,
                            **filters: Any) -> Page[T]:
        """Get a paginated list of records."""
        raise NotImplementedError()

    @abstractmethod
    async def get_count(self, **filters: Any) -> int:
        """Get the count query with filters"""
        raise NotImplementedError()

    @abstractmethod
    async def add(self, record: T) -> T:
        """Creates a new record.

        Args:
            record (T): The record to be created.

        Returns:
            T: The created record.
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(self, record: T) -> T:
        """Updates an existing record.

        Args:
            record (T): The record to be updated incl. record id.

        Returns:
            T: The updated record.
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *args: Any, **kwargs: Any) -> None:
        """Deletes a record by either positional or keyword arguments.

        Args:
            *args (Any): Positional arguments representing values for filtering.
            **kwargs (Any): Keyword arguments representing field names and their corresponding values for filtering.
        """
        raise NotImplementedError()


class GenericSqlRepository(GenericRepository[T], ABC):

    def __init__(self, session: AsyncSession, model: Type[T]) -> None:
        """Creates a new repository instance.

        Args:
            session (AsyncSession): SQLModel async session.
            model (Type[T]): SQLModel class type.
        """
        self.session = session
        self.model = model

    async def get(self, *args: Any, **kwargs: Any) -> T | None:

        query = self._build_query(*args, **kwargs).limit(1)
        res = await self.session.exec(query)
        return res.first()

    async def get_list(self, limit: int = 0, order_by: str | List[str] | None = None, filters: dict = None,
                       **kwargs: Any) -> list[T]:
        """Gets a list of records from the database."""
        query = select(self.model)

        # Apply filters and ordering
        query = self._apply_filters_and_ordering(query, filters=filters, order_by=order_by, **kwargs)

        # Apply limit
        if limit > 0:
            query = query.limit(limit)

        res = await self.session.exec(query)

        return list(res.all())

    async def get_page_list(self, page_number: int = 1, page_size: int = 10, order_by: str | List[str] | None = None,
                            filters: dict = None, **kwargs: Any) -> Page[T]:
        """
                   获取分页列表的通用方法。

                   该方法根据分页参数、排序规则、过滤条件以及额外的简单过滤条件从数据库中获取分页列表。

                   Args:
                       page_number (int, optional):
                           当前页码，默认为 1。
                           表示要查询的页数，第一页为 1。

                       page_size (int, optional):
                           每页记录数，默认为 10。
                           表示每一页包含多少条记录。

                       order_by (str | List[str] | None, optional):
                           排序字段，可以为字符串或字符串列表，默认为 None。
                           如果字段名前有 `-` 表示降序排序，否则为升序。例如：`-created_at` 表示按 `created_at` 降序排列。

                       filters (dict, optional):
                           复杂过滤条件，支持 `and` 或 `or` 逻辑嵌套，默认为 None。
                           示例：
                           ```python
                           filters={
                               'or': [
                                   {"created_at": {">": start_of_day}},  # created_at 大于 start_of_day
                                   {"created_at": {"<": end_of_day}}     # created_at 小于 end_of_day
                               ]
                           }
                           ```

                       **kwargs (Any):
                           额外的简单过滤条件，通过 `AND` 逻辑组合应用。
                           每个条件的形式为 `{字段名: {操作符: 值}}`。
                           示例： `created_at={">": day}` 表示 `created_at > day`。
                           如果条件是 `None`，则自动转换为 `IS NULL` 过滤条件。

                   Returns:
                       Page[T]:
                           返回一个 `Page` 对象，其中包含分页结果、当前页码、每页记录数以及总记录数。
                           Page 对象的字段包括：
                           - `elements`: 当前页的数据列表
                           - `page_number`: 当前页码
                           - `page_size`: 每页记录数
                           - `total_records`: 总记录数

                   Raises:
                       ValueError:
                           如果过滤条件无效或者操作符不支持，则抛出 `ValueError`。

                   示例:
                       ```python
                       results = await self.get_page_list(
                           page_number=2,
                           page_size=5,
                           order_by='-created_at',
                           filters={
                               'or': [
                                   {"created_at": {">": start_of_day}},
                                   {"created_at": {"<": end_of_day}}
                               ]
                           },
                           sentiment=None,  # sentiment 为 NULL
                           created_at={">": day}  # created_at > day
                       )
                       ```
                   """

        # Calculate the total number of records
        total_records = await self.get_count(filters=filters, **kwargs)

        # Apply limit, offset, and ordering for pagination
        query = select(self.model).limit(page_size).offset((page_number - 1) * page_size)

        # Apply filters and ordering
        query = self._apply_filters_and_ordering(query, order_by=order_by, filters=filters, **kwargs)

        res = await self.session.exec(query)
        elements = list(res.all())

        return Page(elements=elements, page_number=page_number, page_size=page_size, total_records=total_records)

    async def get_count(self, filters: dict = None, **kwargs: Any) -> int:
        """Gets the count of records with optional filters."""
        query = select(func.count()).select_from(self.model)

        # Apply filters using the same logic as _apply_filters
        query = self._apply_filters(query, filters=filters, **kwargs)

        res = await self.session.exec(query)
        return res.one()

    async def add(self, record: T) -> T:
        """Adds a new record to the database."""
        set_timestamps(record, is_new=True)
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def add_entity_if_not_exists(
            self,
            entity: T,
            unique_keys: dict[str, Any]
    ) -> T:
        """
        通用方法：添加实体（如果不存在）。
        检查实体是否存在，如果已存在则返回；否则添加新实体。
        """
        existing_entity = await self.get(**unique_keys)
        if existing_entity:
            return existing_entity
        return await self.add(entity)

    async def add_or_update_entity(
            self,
            entity: T,
            unique_keys: dict[str, Any],
            update_fields: list[str]
    ) -> T:
        """
        通用方法：添加或更新实体。
        如果实体存在，根据指定字段更新；否则添加新实体。
        """
        existing_entity = await self.get(**unique_keys)
        if existing_entity:
            for field in update_fields:
                setattr(existing_entity, field, getattr(entity, field))
            await self.update(existing_entity)
            return existing_entity
        return await self.add(entity)

    async def add_batch(self, records: List[T]) -> None:
        """
        批量添加记录到数据库。

        Args:
            records (List[T]): 要添加的记录列表。
        """
        if not records:
            return

        for record in records:
            set_timestamps(record, is_new=True)

        self.session.add_all(records)
        await self.session.commit()

    async def update(self, record: T) -> T:
        set_timestamps(record)
        """Updates an existing record in the     database."""
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def delete(self, *args: Any, **kwargs: Any) -> None:
        """Deletes a record from the database using its key."""
        record = await self.get(*args, **kwargs)
        if record:
            await self.session.delete(record)
            await self.session.commit()

    def _build_query(self, *args: Any, **kwargs: Any):
        """Helper function to build query based on primary keys or filters."""
        if args:
            primary_keys = get_primary_keys(self.model)
            if len(args) != len(primary_keys):
                raise ValueError(f"Expected {len(primary_keys)} primary key values, got {len(args)}.")
            pk_filter = dict(zip(primary_keys, args))
            return select(self.model).filter_by(**pk_filter)
        elif kwargs:
            return select(self.model).filter_by(**kwargs)
        else:
            raise ValueError(
                "Either primary key arguments (*args) or filtering conditions (**kwargs) must be provided.")

    def _apply_filters_and_ordering(self, query, filters: dict = None, order_by: str | List[str] | None = None,
                                    **kwargs: Any):
        """Apply dynamic filters and ordering to a SQLAlchemy query."""

        # Apply both complex filters (filters dict) and simple filters (kwargs)
        query = self._apply_filters(query, filters=filters, **kwargs)

        # Apply ordering
        if order_by:
            if isinstance(order_by, str):
                order_by = [order_by]  # Ensure order_by is a list for consistent processing

            order_criteria = []
            for order in order_by:
                if order.startswith('-'):
                    field_name = order[1:]  # Remove the '-' to get the field name
                    try:
                        order_criteria.append(desc(getattr(self.model, field_name)))
                    except AttributeError:
                        raise ValueError(f"Invalid field for ordering: {field_name}")
                else:
                    try:
                        order_criteria.append(asc(getattr(self.model, order)))
                    except AttributeError:
                        raise ValueError(f"Invalid field for ordering: {order}")

            query = query.order_by(*order_criteria)

        return query

    def _apply_filters(self, query, filters: dict = None, **kwargs: Any):
        """Apply both complex filters (AND/OR) and simple keyword-based filters to a SQL query."""

        # 处理 filters 和 kwargs
        filter_conditions = self._build_filter_conditions(filters) if filters else None

        # 检查简单条件 (kwargs)
        simple_conditions = []
        for key, value in kwargs.items():
            if value is None:
                simple_conditions.append(getattr(self.model, key).is_(None))
            elif isinstance(value, dict):
                for operator, operand in value.items():
                    condition = apply_operator(getattr(self.model, key), operator, operand)
                    if condition is not None:
                        simple_conditions.append(condition)
            else:
                # 默认处理为等于条件
                simple_conditions.append(getattr(self.model, key) == value)

        if filter_conditions is not None:
            query = query.filter(filter_conditions)

        if simple_conditions:
            query = query.filter(and_(*simple_conditions))

        return query

    def _build_filter_conditions(self, filters: dict) -> Any:
        """Build complex filter conditions from nested dictionaries (AND/OR logic)."""

        def parse_conditions(conditions, logic_type):
            """Recursively parse conditions with specified logic (AND/OR)."""
            parsed_conditions = []
            for condition in conditions:
                if isinstance(condition, dict):
                    parsed_conditions.append(self._build_filter_conditions(condition))
                else:
                    parsed_conditions.append(condition)
            # Filter out None conditions and apply the logic
            parsed_conditions = [cond for cond in parsed_conditions if cond is not None]
            return and_(*parsed_conditions) if logic_type == 'and' else or_(*parsed_conditions)

        # Handle 'and'/'or' at the top level
        if 'and' in filters:
            return parse_conditions(filters['and'], 'and')
        elif 'or' in filters:
            return parse_conditions(filters['or'], 'or')
        else:
            # Base case: single conditions
            return and_(*self._parse_single_conditions(filters))

    def _parse_single_conditions(self, conditions: dict) -> list:
        """Parse a single-level condition dict like {"age": {">": 18}}."""
        parsed_conditions = []
        for field, value in conditions.items():
            if isinstance(value, dict):
                for operator, operand in value.items():
                    condition = apply_operator(getattr(self.model, field), operator, operand)
                    parsed_conditions.append(condition)
            else:
                parsed_conditions.append(getattr(self.model, field) == value)
        return parsed_conditions


class MongoDBRepository(GenericRepository[T], ABC):
    """Base repository for MongoDB with async CRUD operations."""

    ID_FIELD = "id"
    MONGO_ID_FIELD = "_id"

    def __init__(self, db: AsyncIOMotorDatabase, model: Type[T]):
        self.model = model
        self.collection: AsyncIOMotorCollection = db[model.get_collection_name()]

    async def get(self, *args: Any, **kwargs: Any) -> T | None:
        """Retrieve a single record based on query."""

        query = self._build_query(*args, **kwargs)
        document = await self.collection.find_one(query)
        return self._deserialize(document)

    async def get_list(self, limit: int = 0, order_by: str | List[str] | None = None, **filters) -> List[T]:
        """Retrieve a list of records."""

        query = self._build_query(**filters)
        cursor = self.collection.find(query)

        if order_by:
            cursor = cursor.sort(mongo_build_sort(order_by))

        if limit > 0:
            cursor = cursor.limit(limit)

        documents = await cursor.to_list()
        return [self._deserialize(doc) for doc in documents]

    async def get_page_list(
        self, page_number: int = 1, page_size: int = 10, order_by: str | List[str] | None = None, **filters: Any
    ) -> Page[T]:
        """Retrieve a paginated list of records."""

        query = self._build_query(**filters)
        cursor = self.collection.find(query)

        if order_by:
            cursor = cursor.sort(mongo_build_sort(order_by))

        total_records = await self.collection.count_documents(query)
        cursor = cursor.skip((page_number - 1) * page_size).limit(page_size)
        documents = await cursor.to_list(length=page_size)

        return Page(elements=[self._deserialize(doc) for doc in documents],
                    page_number=page_number,
                    page_size=page_size,
                    total_records=total_records)

    async def get_count(self, **filters: Any) -> int:
        """Count the number of records matching the filters."""

        query = self._build_query(**filters)
        return await self.collection.count_documents(query)

    async def add(self, record: T) -> T:
        """Insert a new record."""

        document = record.model_dump(by_alias=True)
        document[self.MONGO_ID_FIELD] = document.pop(self.ID_FIELD)
        await self.collection.insert_one(document)
        return self._deserialize(document)

    async def update(self, record: T) -> T:
        """Update an existing record."""

        query = {self.MONGO_ID_FIELD: record.id}
        update_data = {"$set": record.model_dump(by_alias=True, exclude={self.ID_FIELD})}
        result = await self.collection.update_one(query, update_data)
        if result.matched_count == 0:
            raise ValueError("No document matched the given ID.")
        return record

    async def delete(self, *args: Any, **kwargs: Any) -> None:
        """Delete a record."""

        query = self._build_query(*args, **kwargs)
        result = await self.collection.delete_one(query)
        if result.deleted_count == 0:
            raise ValueError("No document matched the given criteria.")

    def _build_query(self, *args: Any, **kwargs: Any) -> dict:
        """
        Build MongoDB query from positional and keyword arguments.
        """

        query = {}

        # Handle positional arguments
        field_order = self.model.get_field_order()
        if args:
            if len(args) > len(field_order):
                raise ValueError(f"Too many positional arguments. Expected at most {len(field_order)}, got {len(args)}.")

            for field, value in zip(field_order, args):
                if field == self.ID_FIELD:
                    try:
                        query[self.MONGO_ID_FIELD] = ObjectId(value)
                    except:
                        query[self.MONGO_ID_FIELD] = value
                else:
                    query[field] = value

        # Handle keyword arguments
        if self.ID_FIELD in kwargs:
            try:
                query[self.MONGO_ID_FIELD] = ObjectId(kwargs.pop(self.ID_FIELD))
            except:
                query[self.MONGO_ID_FIELD] = kwargs.pop(self.ID_FIELD)

        query.update(kwargs)
        return query

    def _deserialize(self, document: dict) -> T | None:
        if document:
            document[self.ID_FIELD] = document.pop(self.MONGO_ID_FIELD)
            return self.model(**document)
        return None
