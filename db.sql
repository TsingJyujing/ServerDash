---创建数据库
CREATE DATABASE monitor
  WITH ENCODING='UTF8'
       CONNECTION LIMIT=-1;

---新建CPU性能数据表
CREATE TABLE public.cpu
(
    tick timestamp without time zone NOT NULL,
    usage double precision,
    usage_detail double precision[],
    CONSTRAINT cpu_pkey PRIMARY KEY (tick)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.cpu
  OWNER TO postgres;

---插入CPU信息
---INSERT INTO public.cpu (tick, usage, usage_detail) VALUES ('%s', %f, '%s');

---新建内存性能数据表
CREATE TABLE public.memory
(
    tick timestamp without time zone NOT NULL,
    total double precision,
    used double precision,
    swap_total double precision,
    swap_used double precision,
    CONSTRAINT memory_pkey PRIMARY KEY (tick)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.memory
  OWNER TO postgres;

---写入内存信息
---INSERT INTO public.memory (tick, total, used, swap_total, swap_used) VALUES ('%s', %f, %f, %f, %f);

---新建磁盘性能数据表
CREATE TABLE public.disk
(
  tick timestamp without time zone NOT NULL,
  mount_point character varying NOT NULL,
  total double precision,
  used double precision,
  CONSTRAINT disk_pkey PRIMARY KEY (tick, mount_point)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.disk
  OWNER TO postgres;

---写入硬盘信息
---INSERT INTO public.disk (tick, mount_point, total, used) VALUES ('%s','%s',%f,%f);

---清空测试数据
DELETE FROM public.disk;
DELETE FROM public.cpu;
DELETE FROM public.memory;

---CREATE VIEWS

-- View: public.disk_view

-- DROP VIEW public.disk_view;

CREATE OR REPLACE VIEW public.disk_view AS 
 SELECT disk.tick,
    disk.mount_point,
    disk.total,
    disk.used,
    100.0::double precision * disk.used / disk.total AS precent
   FROM disk;

ALTER TABLE public.disk_view
  OWNER TO postgres;

-- View: public.memory_view

-- DROP VIEW public.memory_view;

CREATE OR REPLACE VIEW public.memory_view AS 
 SELECT memory.tick,
    memory.total,
    memory.used,
    memory.swap_total,
    memory.swap_used,
    100.0::double precision * memory.used / memory.total AS precent,
    100.0::double precision * memory.swap_used / memory.swap_total AS swap_precent
   FROM memory;

ALTER TABLE public.memory_view
  OWNER TO postgres;

