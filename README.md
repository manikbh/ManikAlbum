# ManikAlbum
## Photo Album
Online photo album management software, with a focus on editing and viewing/searching metadata for old scanned photo albums (with minimal or wrong EXIF data), with collaborative editing
## Development
Django-based website started December 2020.
## License
(c)2020 Manik Bhattacharjee

[GNU AGPLv3 licence](https://www.gnu.org/licenses/agpl-3.0.en.html)

## TODO list

- Select photos in myphotos and add them to album
- Select photos in myphotos or in album edit view 
  to set metadata for all
 - When one deletes a Photo, remove the file using signals (e.g. https://stackoverflow.com/questions/16041232/django-delete-filefield)
 - Create account/Edit account views
 - Create group
 - Access management views for photos, albums and groups
 - Dynamic search box for location
 - Better date widgets
 - Create/Edit metadata in Create/Update photo view
 - Mass upload of photos in or outside album, with progress bar, non-blocking for django and UI
 - Really write the tests
 - Make that nice with CSS
 - Implement undo function ?
 - Beware of editing conflict (timer in js to check data was not modified, or lock, or check on submit)
 