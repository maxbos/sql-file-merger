-- requires: example__schema

begin;

  create table example.user (
    id                  serial primary key,
    created_at          timestamptz not null default now()
  );

commit;
