import os
import shutil

class Backups:
    def __init__(self, db):
        """Initialize the Backups instance.

        :param db: Database instance to manage backups for
        :type db: Database
        """
        self.db = db
        self.root = db.root
        self.name = db.name

        self.max_backups = 5

    def backup(self):
        """Create a backup of the database.

        Creates a new backup file with an incremented ID and removes oldest backups
        if the maximum number of backups is exceeded.
        """
        backup_id = self.latest + 1

        shutil.copy(
            self.db_path,
            os.path.join(self.backup_path, str(backup_id))
        )

        backups = self.list
        backups.reverse()

        while len(backups) > self.max_backups:

            os.remove(
                os.path.join(
                    self.root,
                    ".backups",
                    self.name,
                    str(backups[0])
                    )
                )

            del backups[0]

    # def restore(self, backup_id):
    #     path = self.get_path_of_backup(backup_id)

    @property
    def db_path(self):
        """Get the path to the main database file.

        :return: Full path to the database file
        :rtype: str
        """
        return os.path.join(self.root, "%s.mpack" % self.name)

    @property
    def backup_path(self):
        """Get the path to the backup directory.

        :return: Full path to the backup directory
        :rtype: str
        """
        return os.path.join(self.root, ".backups", self.name)

    @property
    def list(self):
        """List all backups of the database.

        Creates backup directory if it doesn't exist.

        :return: List of backup IDs sorted in descending order
        :rtype: list[int]
        """
        if not os.path.exists(self.backup_path):
            os.makedirs(self.backup_path)
            return []

        backups = os.listdir(self.backup_path)
        backups = [int(i) for i in backups]
        backups.sort()
        backups.reverse()

        return backups

    @property
    def latest(self):
        """Get the most recent backup ID.

        :return: ID of the most recent backup, or 0 if no backups exist
        :rtype: int
        """
        backups = self.list

        if len(backups) > 0:
            return int(backups[0])
        else:
            return 0

    @property
    def last(self):
        """Get the oldest backup of the database.

        :return: ID of the oldest backup
        :rtype: int
        """
        backups = self.list

        return backups[0]

    def get_path_of_backup(self, backup_id):
        """Get the full path of a specific backup.

        :param backup_id: ID of the backup
        :type backup_id: int
        :return: Full path to the backup file
        :rtype: str
        """
        return os.path.join(self.backup_path, str(backup_id))
