import time
import datetime
import psutil
import psycopg2
from DBUtils.PooledDB import PooledDB
import threading

dbPool = PooledDB(psycopg2, 5,
                  host="localhost",
                  port=5432,
                  database="monitor",
                  user="postgres",
                  password="979323")

sql_insert_cpu = "INSERT INTO public.cpu (tick, usage, usage_detail) VALUES ('%s', %f, '%s');"
sql_insert_memory = "INSERT INTO public.memory (tick, total, used, swap_total, swap_used) VALUES ('%s', %f, %f, %f, %f);"
sql_insert_disk = "INSERT INTO public.disk (tick, mount_point, total, used) VALUES ('%s','%s',%f,%f);"


def get_now_tick():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def doublelist2pgarray(list_input):
    return "{%s}" % (",".join(["%f" % value for value in list_input]))


class CPUMonitor(threading.Thread):
    def __init__(self, interval=5, sleep=0):
        super(CPUMonitor, self).__init__(name="CPULogger")
        self.interval = interval
        self.sleep = sleep
        self.conn = dbPool.connection()

    def write_data(self, cpu_usage, mean_usage):
        curs = self.conn.cursor()
        curs.execute(sql_insert_cpu % (get_now_tick(), mean_usage, doublelist2pgarray(cpu_usage)))
        self.conn.commit()
        curs.close()

    def run(self):
        while True:
            cpu_usage = psutil.cpu_percent(interval=self.interval, percpu=True)
            mean_usage = sum(cpu_usage) / len(cpu_usage)
            self.write_data(cpu_usage, mean_usage)
            print("CPU usage logged successfully at %s" % get_now_tick())
            time.sleep(self.sleep)


class MemoryMonitor(threading.Thread):
    def __init__(self, sleep=10):
        super(MemoryMonitor, self).__init__(name="MemoryLogger")
        self.sleep = sleep
        self.conn = dbPool.connection()

    def write_data(self, total, used, swap_total, swap_used):
        curs = self.conn.cursor()
        curs.execute(sql_insert_memory % (get_now_tick(), total, used, swap_total, swap_used))
        self.conn.commit()
        curs.close()

    def run(self):
        while True:
            meminfo = psutil.virtual_memory()
            swap_meminfo = psutil.swap_memory()
            self.write_data(meminfo.total, meminfo.used, swap_meminfo.total, swap_meminfo.used)
            print("Memory usage logged successfully at %s" % get_now_tick())
            time.sleep(self.sleep)


class DiskMonitor(threading.Thread):
    def __init__(self, sleep=10):
        super(DiskMonitor, self).__init__(name="DiskLogger")
        self.sleep = sleep
        self.conn = dbPool.connection()

    def write_data(self, mount_point, total, used):
        curs = self.conn.cursor()
        curs.execute(sql_insert_disk % (get_now_tick(), mount_point, total, used))
        self.conn.commit()
        curs.close()

    def run(self):
        while True:
            disk_parts = filter(lambda x: x.opts != 'cdrom', psutil.disk_partitions())
            for disk in disk_parts:
                disk_use = psutil.disk_usage(disk.mountpoint)
                self.write_data(disk.device, disk_use.total, disk_use.used)
            print("Disk usage logged successfully at %s" % get_now_tick())
            time.sleep(self.sleep)


class CleanDatabase(threading.Thread):
    def __init__(self, sleep=600):
        super(CleanDatabase, self).__init__(name="DatabaseCleaner")
        self.sleep = sleep
        self.conn = dbPool.connection()

    def remove_epired(self, table_name):
        curs = self.conn.cursor()
        curs.execute("DELETE FROM public.%s WHERE tick<=(now()- INTERVAL '30d');" % table_name)
        self.conn.commit()
        curs.close()

    def run(self):
        while True:
            [self.remove_epired(table_name) for table_name in ("cpu", "memory", "disk")]
            print("Expired data removed at " + get_now_tick())
            time.sleep(self.sleep)


def main():
    process_list = [
        CPUMonitor(interval=10, sleep=0),
        MemoryMonitor(sleep=5),
        DiskMonitor(sleep=60)]
    for process in process_list:
        process.start()
    for process in process_list:
        process.join()


if __name__ == "__main__":
    main()
