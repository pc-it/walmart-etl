from loguru import logger
from typing import Tuple, Dict, Optional

from .abstract import AbstractLoader
from src.orm.base import Session


class SqlLoader(AbstractLoader):

    @staticmethod
    def repr_db_data_filters_to_delete(value):
        return [
            statement.compile(compile_kwargs={"literal_binds": True}).string
            for statement in value
        ]

    def load(self, data_to_insert: Tuple[Dict], filters_to_delete: Optional[Tuple] = None, orm_model=None) -> bool:
        logger.info(f'{self}: Load data to the database.')
        model = self.orm_model or orm_model
        try:
            with Session() as session:

                if filters_to_delete is not None:
                    logger.info(f'{self}: Delete old data using {self.repr_db_data_filters_to_delete(value=filters_to_delete)}')
                    session.query(model).filter(*filters_to_delete).delete()
                logger.info(f'{self}: Insert {len(data_to_insert)} to the database.')
                session.bulk_insert_mappings(model, data_to_insert)
                logger.info(f'{self}: Commit changes.')
                session.commit()
                saved = True
        except Exception as e:
            logger.warning(f'{self}: Issue with db saving {e}.')
            raise e
        return saved
