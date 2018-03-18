drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  'text' text not null,
  available boolean not null,
  concert_date date not null
);

drop table if exists availabilities;
create table availabilities (
    id integer primary key autoincrement,
    id_concert integer foreign key not null,
    'mic' text not null,
    'bass' text not null,
    'drums' text not null,
    'keys' text not null,
    'guitar' text not null
);