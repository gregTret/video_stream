# Video Server
Nothing too crazy, just a little Flask/Ngnix server I use to stream MP4/MKV files on my network. 
- MongoDB Documents for video descriptions/categories + posters as well as physical locations on drive.
- Flask to render HTML Documents + make queries to MongoDB 
- Ngnix to stream requested files

### Ports Used
```
Flask: 5000
Ngnix: 8080 + Streams on 5001
MongoDB: 27017
```
### Example MongoDB Document:
```
{
  "adult": Boolean,
  "genre_ids": [
    integer
  ],
  "id": integer,
  "original_language": String,
  "original_title": String,
  "overview": String,
  "popularity": Number,
  "poster_path": String,
  "release_date": String,
  "title": String,
  "video": String,
  "vote_average": Number,
  "vote_count": Integer,
  "recommended":Boolean
}
```

Todo List
- Add search by category
- Fix search bar CSS on mobile + create search result page
- Clean up server.py