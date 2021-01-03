# ManikAlbum
## Photo Album
Online photo album management software, with a focus on editing and viewing/searching metadata for old scanned photo albums (with minimal or wrong EXIF data), with collaborative editing
## Development
Django-based website started December 2020.
## License
(c)2020 Manik Bhattacharjee

[GNU AGPLv3 licence](https://www.gnu.org/licenses/agpl-3.0.en.html)

## TODO list

 - Add selected photos to album
 - Select photos in album edit view to set metadata for all
 - Allow image reordering in an album (uploaded timestamp, filename, moving one file, from datetime)
 - Search/select photos by location, by people
 - Map of all location, select region and timeframe to find photos that can be used to create an album
 - Create account/Edit account views
 - Create group
 - Access management views for photos, albums and groups, but also for location and people
 - Dynamic search box for location
 - Better date widgets
 - Create/Edit metadata in Create/Update photo view
 - Mass upload of photos in or outside album, with progress bar, non-blocking for django and UI
 - Really write the tests
 - Make that nice with CSS
 - Implement undo function ?
 - Beware of editing conflict (timer in js to check data was not modified, or lock, or check on submit)
 - Use Django REST for AJAX API ?
 - Use CSRF cookie in views for ajax requests (add photos to album, upload photos, update metadata of photos...)
 - Detect faces, identify faces to people
 - Be smart in location or people selection UI (put most used or more recently used locations on top, same for people)
 - Fuse two identified persons into one (if two users have created the same person with different names, allow to fuse them)
