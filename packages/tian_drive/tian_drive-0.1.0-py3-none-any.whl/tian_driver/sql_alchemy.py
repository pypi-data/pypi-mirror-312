"""Postgres driver."""

# pylint: disable=R0201

import os
from typing import Any, AnyStr, Dict, List, NoReturn, Optional, Tuple

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy import text

from tian_drivers.src.driver import Driver
from tian_core import Entity, singleton
from tian_core.error import DriverConfigError
from tian_glog import logger

from .migration import DatabaseMigrator


__all__ = ['Postgres']

@singleton
class SQLAlchemy(Driver):
    """Postgres connection Driver.

    Environment variables:
        DATABASE_URL: [1]
        DATABASE_USER: Database user name
        DATABASE_PASSWORD: Database user password
        DATABASE_HOST: default('localhost') Database host
        DATABASE_PORT: default('5432') database connection port
        DATABASE_NAME: default('postgres') Database name
        DATABASE_COMMIT: default('false') Auto commit transaction flag

    :type url: str
    :param url: Database connection url with standard format [1]

    :type user: str
    :param user: Database user name

    :type pwd: str
    :param pwd: Database user password

    :type host: str
    :param host: Database host

    :type port: str
    :param port: Database port number

    :type database: str
    :param database: Database name

    :type autocommit: bool
    :param autocommit: Auto commit transactions flag

    [1] Standard URL format: postgres://<user>:<password>@<host>:<port>/<database>
    """

    def __init__(
        self,
        url: Optional[AnyStr] = None,
        user: Optional[AnyStr] = None,
        pwd: Optional[AnyStr] = None,
        host: Optional[AnyStr] = None,
        port: Optional[AnyStr] = None,
        database: Optional[AnyStr] = None,
        autocommit: Optional[bool] = None
    ):
        super().__init__()
        self.__build_connection(url, user, pwd, host, port, database, autocommit)
        self._auto_migrate()

    def query(self, **kwargs) -> List[Tuple]:
        """Execute a query and return all values.

        :param kwargs: Parameters to execute query statement.
            sql: AnyStr -> SQL query statement
            args: Optional[Iterable[Any]] -> Object with query replacement values

        :return List[Tuple]: List of tuple records found by query
        """
        if 'sql' not in kwargs:
            raise DriverConfigError('Missing required parameter: sql')


        self._validate_params({'sql'}, set(kwargs.keys()))
        with self.__conn.connect() as connection:
            logger.info(f"Executing query: {kwargs['sql']} with args {kwargs.get('args', [])}")
            result = connection.execute(text(kwargs['sql']), kwargs.get('args', []))
            return result

        raise DriverConfigError('Missing required parameter: sql')

    def query_one(self, **kwargs) -> Tuple:
        """Execute a query and return just the first result.

        :param kwargs: Parameters to execute query statement.
            sql: AnyStr -> SQL query statement
            args: Optional[Iterable[Any]] -> Object with query replacement values

        :return Tuple: Tuple record found by query
        """
        self._validate_params({'sql'}, set(kwargs.keys()))

        with self.__conn.connect() as connection:
            # Use text() to safely handle the SQL query and parameters
            logger.info(f"Executing query: {kwargs['sql']} with args {kwargs.get('args', [])}")
            result = connection.execute(text(kwargs['sql']), kwargs.get('args', []))
            res = result.fetchone()  # Fetch the first result

        return res

    def query_none(self, **kwargs) -> NoReturn:
        """Execute a query and do not return any result value.

        :param kwargs: Parameters to execute query statement.
            sql: AnyStr -> SQL query statement
            args: Optional[Iterable[Any]] -> Object with query replacement values
        """
        self._validate_params({'sql'}, set(kwargs.keys()))
        with self.__conn.connect() as connection:
            logger.info(f"Executing query: {kwargs['sql']} with agrgs {kwargs['args']}")
            connection.execute(text(kwargs['sql']), kwargs.get('args', []))

    def begin(self) -> NoReturn:
        """Begin transaction in DB."""
        with self.__conn.connect() as connection:
            connection.begin()

    def commit(self) -> NoReturn:
        """Commit transaction in DB."""
        with self.__conn.connect() as connection:
            connection.commit()

    def rollback(self) -> NoReturn:
        """Rollback transaction."""
        with self.__conn.connect() as connection:
            connection.rollback()

    def close(self) -> NoReturn:
        """Close database connection."""
        logger.error("Closing connection")
        if self.__conn is not None:
            self.__conn.dispose()  # Use dispose() for SQLAlchemy connections
            logger.debug("Connection closed.")

    def get_real_driver(self) -> Any:
        """Get real driver connection instance."""
        return self.__conn

    def placeholder(self) -> AnyStr:
        """Return the next place holder param for prepared statements.

        :return AnyStr: Placeholder token
        """
        return ':param'  # Use named parameters for SQLAlchemy

    def reset_placeholder(self) -> NoReturn:
        """Reset place holder status (do nothing)"""
        pass

    # @staticmethod
    # def __execute(connection, sql: AnyStr, *args):
    #     """Execute query and attempt to replace with arguments.

    #     :param connection: SQLAlchemy connection object
    #     :param sql: Raw query to be executed
    #     :param args: List of arguments passed to be replaced in query
    #     """
    #     # Use text() to allow for parameter substitution
    #     query = text(sql)
    #     try:
    #         if not args:
    #             return connection.execute(query)

    #         return connection.execute(query, *args)
    #     except Exception as error:
    #         logger.error(f"Error executing query: {error}")
    #         raise error

    def __build_connection(
        self,
        url: Optional[AnyStr] = None,
        user: Optional[AnyStr] = None,
        pwd: Optional[AnyStr] = None,
        host: Optional[AnyStr] = None,
        port: Optional[AnyStr] = None,
        database: Optional[AnyStr] = None,
        autocommit: Optional[bool] = None,
    ) -> NoReturn:
        """start real driver connection from parameters.

        :param url: Database connection url
        :param user: Database user name
        :param pwd: Database user password
        :param host: Database host
        :param port: Database port number
        :param database: Database name
        :param autocommit: Auto commit transactions
        """

        self.__params = self.__prepare_connection_parameters(
            url, user, pwd, host, port, database, autocommit
        )

        params = self.__params
        commit = params['autocommit']
        del params['autocommit']

        if params['url'] is not None:
            print(params['url'])
            self.__conn =  create_engine(
                params['url'],
                # disable default reset-on-return scheme
                pool_reset_on_return=None,
                isolation_level='AUTOCOMMIT' if autocommit else None
            )
            return

        del params['url']

        connection_str = f"postgresql://{params['user']}:{params['pwd']}@{params['host']}:{params['port']}/{params['database']}"
        self.__conn: Engine = create_engine(connection_str, isolation_level='AUTOCOMMIT' if autocommit else None)


    def execute(self, sql: AnyStr, **kwargs) -> NoReturn:
        """Execute a SQL query with parameter binding.

        :param sql: The SQL query string to execute.
        :param kwargs: Optional keyword arguments for query parameter binding.
        :return: The result of the executed query, which could be a ResultProxy or None.
        """
        try:
            with self.__conn.connect() as connection:
                connection.begin()
                data = kwargs.get('data', None)
                if kwargs:
                    logger.info(f"Executing query: {sql} with args: {kwargs} len: {len(kwargs)}")
                    result = connection.execute(text(sql), data)

                else:
                    logger.info(f"Executing query: {sql}")
                    result = connection.execute(text(sql))
                connection.commit()
                return result
        except Exception as error:
            logger.error(f"Error executing query: {error}")
            connection.rollback()
            raise error

    @staticmethod
    def __prepare_connection_parameters(
        url: Optional[AnyStr] = None,
        user: Optional[AnyStr] = None,
        pwd: Optional[AnyStr] = None,
        host: Optional[AnyStr] = None,
        port: Optional[AnyStr] = None,
        database: Optional[AnyStr] = None,
        autocommit: Optional[bool] = None,
    ) -> Dict[AnyStr, Any]:
        """Validate connection parameters an try to fill it from env vars if they are not set.

        :param url: Database connection url
        :param user: Database user name
        :param pwd: Database user password
        :param host: Database host
        :param port: Database port number
        :param database: Database name
        :param autocommit: Auto commit transactions
        :return Dict[AnyStr, Any]: Connection parameters
        :raise DriverConfigError: If connection url and connection user are None at the same time
        """

        params = {
            'url': url,
            'user': user,
            'password': pwd,
            'host': host,
            'port': port,
            'database': database,
            'autocommit': autocommit
        }

        params = {key: value for key, value in params.items() if value is not None}

        envs = {
            'url': os.getenv('DATABASE_URL', None),
            'user': os.getenv('DATABASE_USER', 'thienhang'),
            'password': os.getenv('DATABASE_PASSWORD', 'thienhang'),
            'host': os.getenv('DATABASE_HOST', 'localhost'),
            'port': os.getenv('DATABASE_PORT', '5432'),
            'database': os.getenv('DATABASE_NAME', 'thienhang'),
            'autocommit': os.getenv('DATABASE_COMMIT', 'false').lower() == 'true'

        }

        envs.update(params)

        if envs['url'] is not None:
            envs['host'] = None
            envs['port'] = None
            envs['database'] = None

        if envs['url'] is None and envs['user'] is None:
            raise DriverConfigError('Invalid connection params. Not user detected.')


        # from sqlalchemy import URL

        # url_object = URL.create(
        #     "postgresql+pg8000",
        #     username="dbuser",
        #     password="kx@jj5/g",  # plain (unescaped) text
        #     host="pghost10",
        #     database="appdb",
        # )
        return envs

    def __repr__(self):
        """Postgres driver representation."""
        return f"Postgres({str(self.__params)})"

    def _validate_params(self, required: set, provided: set) -> NoReturn:
        """Validate if required parameters are provided.

        :param required: Set of required parameters
        :param provided: Set of provided parameters
        :raise DriverConfigError: If required parameters are not provided
        """

        missing = required - provided
        if missing:
            raise DriverConfigError(f"Missing required parameters: {missing}")

    def _auto_migrate(self) -> NoReturn:
        logger.warning("Running auto migration.")
        if os.getenv('DATABASE_MIGRATION', 'false').lower() != 'true':
            logger.info("Auto migration is disabled.")
            return
        migrator = DatabaseMigrator(self.__conn)
        migrator.run_migration()


