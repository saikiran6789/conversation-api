create table users (
  id uuid primary key default gen_random_uuid(),
  email varchar(255),
  created_at timestamptz default now()
);
