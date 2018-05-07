drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  'text' text not null,
  available integer not null,
  concert_date date not null
);

drop table if exists availabilities;
create table availabilities (
    id integer primary key not null,
    'mic' integer not null,
    'bass' integer not null,
    'drums' integer not null,
    'keys' integer not null,
    'guitar' integer not null
);

create table logins (
    id integer primary key autoincrement,
    'user' text not null,
    'password' text not null
);