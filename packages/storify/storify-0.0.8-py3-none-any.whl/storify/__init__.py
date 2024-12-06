import os
import time
import copy
import logging

from .logger import Logger
from .database import Database

class Storify:
    def __init__(self, root="data", save_interval=60, log=None, verbose=False, models=[]):
        """Initialize the Storify instance.

        :param root: The root directory where databases will be stored
        :type root: str
        :default root: "data"
        
        :param save_interval: The interval in seconds for automatic saving of databases
        :type save_interval: int 
        :default save_interval: 60

        :param log: Logger instance for logging messages
        :type log: DummyLogger
        :default log: None

        :param models: A list of model classes to be used with the Storify instance
        :type models: list
        :default models: []
        """
        self.root = root
        self.save_interval = save_interval
        self.log = log if log is not None else Logger(level=logging.DEBUG if verbose else logging.INFO)
        self.models = models

        self.databases = []

        if not os.path.exists(self.root):
            os.mkdir(self.root)

        if not os.path.exists(os.path.join(self.root, ".backups")):
            os.mkdir(os.path.join(self.root, ".backups"))
 
    def get_db(self,
               name,
               root={}):
        """Get or create a database instance.

        :param name: Name of the database
        :type name: str
        :param root: Initial root data structure for new database
        :type root: dict
        :default root: {}
        :return: Database instance
        :rtype: Database
        """
        _root = copy.deepcopy(root)

        db = Database(name, self.root, self.log, rootdata=_root, models=self.models)
        self.databases.append(db)

        return db

    def db_exists(self, name):
        """Check if a database exists.

        :param name: Name of the database to check
        :type name: str
        :return: True if database exists, False otherwise
        :rtype: bool
        """
        return os.path.exists(
            os.path.join(self.root, name + ".mpack")
        )

    def rename_db(self, old_name, new_name):
        """Rename a database file.

        .. warning:: Dangerous to use if database is currently open!

        :param old_name: Current name of the database
        :type old_name: str
        :param new_name: New name for the database
        :type new_name: str
        """
        old_path = os.path.join(self.root, old_name + ".mpack")
        new_path = os.path.join(self.root, new_name + ".mpack")

        os.rename(old_path, new_path)

    def remove_db(self, name):
        """Remove a database file.

        .. warning:: May be ineffective if database is currently open!

        :param name: Name of the database to remove
        :type name: str
        """
        path = os.path.join(self.root, name + ".mpack")

        os.remove(path)

    def tick(self, force=False):
        """Tick all open databases.

        Flushes databases to disk if they haven't been flushed recently based on save_interval.

        :param force: Force flush all databases regardless of last flush time
        :type force: bool
        :default force: False
        """
        # Filter out defunct databases
        active_dbs = [db for db in self.databases if not db.defunct]

        for db in active_dbs:
            if force:
                db.flush()
            else:
                # Saves on a regular interval based off of self.save_interval
                if time.time() - db.last_flush > self.save_interval:
                    db.flush()

    def flush(self):
        """Flush all open databases to disk immediately.

        Forces an immediate flush of all active databases by calling tick with force=True.
        """
        self.tick(force=True)

    def __getitem__(self, name):
        """Get a database by name.

        :param name: Name of the database to get
        :type name: str
        :return: Database instance
        :rtype: Database
        """
        return self.get_db(name)

    def __delitem__(self, name):
        """Delete a database by name.

        :param name: Name of the database to delete
        :type name: str
        """
        self.remove_db(name)