-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.cpus (
  id integer GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  name character varying NOT NULL,
  CONSTRAINT cpus_pkey PRIMARY KEY (id)
);
CREATE TABLE public.gpus (
  id integer GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  name character varying NOT NULL,
  CONSTRAINT gpus_pkey PRIMARY KEY (id)
);
CREATE TABLE public.oses (
  id integer GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  name character varying NOT NULL,
  CONSTRAINT oses_pkey PRIMARY KEY (id)
);
CREATE TABLE public.payments (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  tariff_id integer,
  amount numeric,
  pay_date timestamp with time zone DEFAULT now(),
  pc_usage_id bigint,
  CONSTRAINT payments_pkey PRIMARY KEY (id),
  CONSTRAINT payments_tariff_id_fkey FOREIGN KEY (tariff_id) REFERENCES public.tariffs(id),
  CONSTRAINT payments_pc_usage_id_fkey FOREIGN KEY (pc_usage_id) REFERENCES public.pc_usages(id)
);
CREATE TABLE public.pc_software (
  id integer GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  pc_id integer NOT NULL,
  software_id integer NOT NULL,
  CONSTRAINT pc_software_pkey PRIMARY KEY (id),
  CONSTRAINT pc_software_pc_id_fkey FOREIGN KEY (pc_id) REFERENCES public.pcs(id),
  CONSTRAINT pc_software_software_id_fkey FOREIGN KEY (software_id) REFERENCES public.software(id)
);
CREATE TABLE public.pc_usage_types (
  id integer GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  title character varying NOT NULL,
  CONSTRAINT pc_usage_types_pkey PRIMARY KEY (id)
);
CREATE TABLE public.pc_usages (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  pc_id integer NOT NULL,
  pc_usage_type_id integer,
  user_id bigint,
  start_time timestamp without time zone NOT NULL,
  end_time timestamp without time zone,
  CONSTRAINT pc_usages_pkey PRIMARY KEY (id),
  CONSTRAINT pc_usages_pc_id_fkey FOREIGN KEY (pc_id) REFERENCES public.pcs(id),
  CONSTRAINT pc_usages_pc_usage_type_id_fkey FOREIGN KEY (pc_usage_type_id) REFERENCES public.pc_usage_types(id),
  CONSTRAINT pc_usages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id)
);
CREATE TABLE public.pcs (
  id integer GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  cpu_id integer,
  gpu_id integer,
  os_id integer,
  CONSTRAINT pcs_pkey PRIMARY KEY (id),
  CONSTRAINT pcs_cpu_id_fkey FOREIGN KEY (cpu_id) REFERENCES public.cpus(id),
  CONSTRAINT pcs_gpu_id_fkey FOREIGN KEY (gpu_id) REFERENCES public.gpus(id),
  CONSTRAINT pcs_os_id_fkey FOREIGN KEY (os_id) REFERENCES public.oses(id)
);
CREATE TABLE public.software (
  id integer GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  name character varying NOT NULL,
  CONSTRAINT software_pkey PRIMARY KEY (id)
);
CREATE TABLE public.tariffs (
  id integer GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  name character varying,
  price_per_hour numeric,
  hours_number integer,
  description character varying,
  CONSTRAINT tariffs_pkey PRIMARY KEY (id)
);
CREATE TABLE public.users (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  full_name character varying NOT NULL,
  phone_number character varying,
  email character varying NOT NULL UNIQUE,
  password_hash character varying NOT NULL,
  balance numeric DEFAULT 0,
  role character varying DEFAULT 'User'::character varying,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT users_pkey PRIMARY KEY (id)
);