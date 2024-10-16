import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from hashlib import md5
from typing import Any

@dataclass
class Course:
    name: str
    teacher: str
    classroom: str
    weekday: int
    weeks: list[int]
    indexes: list[int]

    def title(self) -> str:
        return f"{self.name} - {self.classroom}"

    def description(self) -> str:
        return f"任课教师：{self.teacher}。"

    @staticmethod
    def week(start: int, end: int) -> list[int]:
        """生成一个从 start 到 end 的周数列表"""
        return list(range(start, end + 1))

@dataclass
class School:
    duration: int = 45  # 每节课的时长
    timetable: list[tuple[int, int]] = field(default_factory=list)  # 上课时间表
    start: tuple[int, int, int] = (2023, 8, 26)  # 开学日期
    courses: list[Course] = field(default_factory=list)  # 课程列表

    HEADERS = [
        "BEGIN:VCALENDAR",
        "METHOD:PUBLISH",
        "VERSION:2.0",
        "X-WR-CALNAME:课表",
        "X-WR-TIMEZONE:Asia/Shanghai",
        "CALSCALE:GREGORIAN",
        "BEGIN:VTIMEZONE",
        "TZID:Asia/Shanghai",
        "END:VTIMEZONE"
    ]

    FOOTERS = ["END:VCALENDAR"]

    def __post_init__(self) -> None:
        assert self.timetable, "请设置每节课的上课时间，以 24 小时制两元素元组方式输入小时、分钟"
        assert len(self.start) >= 3, "请设置开学第一周的日期，以元素元组方式输入年、月、日"
        assert self.courses, "请设置你的课表数组，每节课是一个 Course 实例"
        self.timetable.insert(0, (0, 0))  # 插入一个占位符
        self.start_dt = datetime(*self.start[:3])  # 开始日期
        self.start_dt -= timedelta(days=self.start_dt.weekday())  # 调整为开学周的周一

    def time(self, week: int, weekday: int, index: int, plus: bool = False) -> datetime:
        date = self.start_dt + timedelta(weeks=week - 1, days=weekday - 1)  # 计算课程日期
        lesson_time = date.replace(
            hour=self.timetable[index][0], minute=self.timetable[index][1]
        ) + timedelta(minutes=self.duration if plus else 0)  # 课程时长
        return lesson_time

    def generate(self) -> str:
        runtime = datetime.now()  # 当前时间，用于 DTSTAMP
        texts = []
        unique_events = set()  # 用于跟踪已添加的事件

        for course in self.courses:
            for week in course.weeks:
                for index in course.indexes:  # 对每个时间段生成不同的事件
                    event_key = (course.title(), week, course.weekday, index)  # 更精确的event_key
                    if event_key not in unique_events:  # 避免重复添加
                        unique_events.add(event_key)

                        texts.extend([
                            "BEGIN:VEVENT",
                            f"SUMMARY:{course.title()}",  # 课程标题
                            f"DESCRIPTION:{course.description()}",  # 课程描述
                            f"DTSTART;TZID=Asia/Shanghai:{self.time(week, course.weekday, index):%Y%m%dT%H%M%S}",
                            # 开始时间
                            f"DTEND;TZID=Asia/Shanghai:{self.time(week, course.weekday, index, True):%Y%m%dT%H%M%S}",
                            # 结束时间
                            f"DTSTAMP:{runtime:%Y%m%dT%H%M%SZ}",  # 当前时间的时间戳
                            f"UID:{md5(str(event_key).encode()).hexdigest()}",  # 唯一标识符
                            f"LOCATION:{course.classroom}",  # 教室位置
                            "END:VEVENT",
                        ])

        for line in self.HEADERS + texts + self.FOOTERS:
            first = True
            while line:
                if len(line) > 72:
                    texts.append(line[:72] + "=")  # 72字符后加换行符=
                    line = line[72:]
                else:
                    texts.append(line)
                    break

        return "\n".join(texts)  # 返回完整的ICS文本
