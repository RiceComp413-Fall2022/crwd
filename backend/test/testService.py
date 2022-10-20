import unittest
import os

from datetime import datetime

from src.service import Service

class TestService(unittest.TestCase):

    backup_path = './test/test-backup.csv'

    def test_append_backup(self):
        '''Test append to csv'''
        # Reset backup file
        if os.path.exists(self.backup_path):
            os.remove(self.backup_path)

        # Create service and backup data
        service = Service(datetime.now(), self.backup_path)
        service.backup_to_csv(str(datetime.now()), 1)
        service.backup_to_csv(str(datetime.now()), 2)
        service.backup_to_csv(str(datetime.now()), 3)

        # Restore data to new service
        new_service = Service(datetime.now(), self.backup_path)
        new_service.restore_from_csv()

        # Read the data from the backed-up service
        data = new_service.data
        counts = [count for _, count in data]

        self.assertEqual([1, 2, 3], counts, "backup_to_csv() failed to save data.")
    
    def test_update_backup(self):
        '''Test append to csv'''
        # Reset backup file
        if os.path.exists(self.backup_path):
            os.remove(self.backup_path)

        # Create service and update total devices
        service = Service(datetime.now(), self.backup_path)
        service.update_total_devices(2)
        service.update_total_devices(4)
        service.update_total_devices(6)

        # Restore data to new service
        new_service = Service(datetime.now(), self.backup_path)
        new_service.restore_from_csv()

        # Read the data from the backed-up service
        data = new_service.data
        counts = [count for _, count in data]

        self.assertEqual([2, 4, 6], counts, "update_total_devices() failed to save data.")

    def test_restore_without_backup(self):
        '''Test restoring without a backup. This should not throw an error.'''
        # Reset backup file
        if os.path.exists(self.backup_path):
            os.remove(self.backup_path)
        
        # Restore data to new service (without error)
        new_service = Service(datetime.now(), self.backup_path)
        new_service.restore_from_csv()
