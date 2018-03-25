drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  'text' text not null,
  available boolean not null,
  concert_date date not null
);

drop table if exists availabilities;
create table availabilities (
    id integer primary key not null,
    'mic' text not null,
    'bass' text not null,
    'drums' text not null,
    'keys' text not null,
    'guitar' text not null
);

drop table if exists logins;
create table logins (
    id integer primary key autoincrement,
    'user' text not null,
    'password' text not null
);