drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  'text' text not null,
  available boolean not null,
  concert_date date not null
);