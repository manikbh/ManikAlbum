# ManikAlbum, an online collaborative editor of family photo albums
#    Copyright (C) 2020  Manik Bhattacharjee <manik.bhattacharjee <at> free.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, version 3 of the
#    License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from django.test import TestCase


# from .models import *

# Create your tests here.
class AccessTest(TestCase):
    """ Test image file, metadata and album access in multiple authenticated/unauthenticated contexts"""

    def test_accessFromOwner(self):
        self.assertIs(False, True)

    def test_accessFromImageAuthorized(self):
        self.assertIs(False, True)

    def test_accessFromAlbumAuthorized(self):
        self.assertIs(False, True)

    def test_accessFromGroupPhotoAuthorized(self):
        self.assertIs(False, True)

    def test_accessFromGroupAlbumAuthorized(self):
        self.assertIs(False, True)

    def test_accessFromUnidentifiedUserUnauthorized(self):
        self.assertIs(False, True)

    def test_authorizedAccessFromUnidentifiedUser(self):  # For public files and files with a urlKey access
        self.assertIs(False, True)

    def test_unauthorizedAccessFromUnidentifiedUser(self):  # Not public, no valid urlkey should not grant access
        self.assertIs(False, True)


class AuthorizeTest(TestCase):
    """ Test adding and removing authorizations to and from album, images and metadata"""

    #  TODO owner and admin can modify user access, users can be read-only or read-write authorized
    def test_addImageAdmins(self):  # Should work if you are the owner
        self.assertIs(False, True)

    def test_addImageUsers(self):  # Should work if you are the owner or admin
        self.assertIs(False, True)

    def test_addAlbumAdmins(self):  # add admins to an album only if you are admin or owner
        self.assertIs(False, True)

    def test_addAlbumUsers(self):  # add read or read/write access to users only if you are admin or owner
        self.assertIs(False, True)

    def test_addImageGroup(self):  # add read or read/write access to a group only if you are admin or owner
        self.assertIs(False, True)

    def test_addAlbumGroup(self):  # add read or read/write access to a group only if you are admin or owner
        self.assertIs(False, True)

    def test_ownerNotEditable(self):  # No one should be able to update album or photo owner (read-only)
        self.assertIs(False, True)  # Album test
        self.assertIs(False, True)  # Photo test

    def test_urlkeyNotEditable(self):  # No one should be able to manually change a urlkey (read-only)
        self.assertIs(False, True)  # Album test
        self.assertIs(False, True)  # Photo test


class LockTest(TestCase):
    def test_deleteLockedImage(self):  # Should fail, keeping image file, ImageField and all metadata
        self.assertIs(False, True)

    def test_deleteUnlockedImage(self):  # Image should be deleted from the DB, from the disk and from metadata objects
        self.assertIs(False, True)

    def test_deleteLockedAlbum(self):  # Should fail, keeping image file, ImageField and all metadata
        self.assertIs(False, True)

    def test_deleteUnlockedLocation(self):  # Image should be deleted from the DB, from the disk and from metadata objects
        self.assertIs(False, True)

    def test_updateLockedImageMetadata(self):  # Should fail for title, description and so on
        self.assertIs(False, True)

    def test_updateLockedAlbumMetadata(self):  # Should fail
        self.assertIs(False, True)

    def test_updateLockedLocation(self):  # Should fail to modify coordinates, description and so on
        self.assertIs(False, True)

    def test_checkLocked(self):  # Get info on the lock (who locked and when)
        self.assertIs(False, True)

    def test_setLock(self):  # Lock should work only if you are owner
        self.assertIs(False, True)

    def test_unsetLock(self):  # Only your own locks or those created on something you own
        self.assertIs(False, True)


class UndoTest(TestCase):
    def test_storedBackup(self):  # Check if a backup is available when updating metadata
        self.assertIs(False, True)

    def test_restoreMultipleBackups(self):  # Modify metadata and album, then check that multiple undo works. Redo ?
        self.assertIs(False, True)

    def test_notTooManyBackups(self):  # Old backups piling up (e.g. 10 max for each item, not older than a week)
        self.assertIs(False, True)


class ImageUploadTest(TestCase):
    def test_largeImage(self):  # Reject at form validation https://docs.djangoproject.com/fr/2.2/topics/http/file-uploads/
        self.assertIs(False, True)

    def test_hugeImage(self):  # Reject by web server (for Apache, set LimitRequestBody) to avoid receiving the whole file
        self.assertIs(False, True)

    def test_uploadsOverUserQuota(self):  # Too many files (per day ?), or too much space, or too many files (per user quota)
        self.assertIs(False, True)


class MetadataTest(TestCase):
    def test_editDateTimeMultipleFiles(self):
        self.assertIs(False, True)

    def test_editLocationMultipleFiles(self):
        self.assertIs(False, True)

    def test_editPersonMultipleFiles(self):
        self.assertIs(False, True)

    def test_resetLocation(self):
        self.assertIs(False, True)

    def test_addLocation(self):
        self.assertIs(False, True)

    def test_deleteLocation(self):  # Must not destroy images or albums that use it -> on_delete of the models
        self.assertIs(False, True)

    def test_deletePerson(self):  # Must not destroy images or albums that use it -> on_delete of the models
        self.assertIs(False, True)
