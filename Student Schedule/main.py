from Function import Course, School

# 合并重复课程，去掉同名课程的重复项
school = School(
    duration=45,  # 每节课时间为 45 分钟
    timetable=[
        (8, 00),   # 上午第一节课时间为 8:00 至 8:45
        (8, 55),
        (10, 00),
        (10, 55),
        (13, 30),  # 下午第一节课时间为 1:30 至 2:15
        (14, 25),
        (15, 20),
        (16, 15),
        (18, 00),
        (18, 55),
    ],
    start=(2024, 8, 26),  # 开学第一周当周周一至周日以内的任意日期
    courses=[
        Course(
            name="线性代数",
            teacher="李廷彬",
            classroom="北3306",
            weekday=1,
            weeks=Course.week(11, 16),
            indexes=[1, 2],
        ),
        Course(
            name="线性代数",
            teacher="李廷彬",
            classroom="北3306",
            weekday=2,
            weeks=Course.week(11, 16),
            indexes=[1, 2],
        ),
        Course(
            name="线性代数",
            teacher="李廷彬",
            classroom="北3306",
            weekday=3,
            weeks=Course.week(1, 12),
            indexes=[5, 6],
        ),
        Course(
            name="大学英语3",
            teacher="李静",
            classroom="北3401",
            weekday=1,
            weeks=Course.week(1, 12),
            indexes=[1, 2],
        ),
        Course(
            name="大学英语3",
            teacher="李静",
            classroom="北3401",
            weekday=4,
            weeks=Course.week(1, 12),
            indexes=[3, 4],
        ),
        Course(
            name="体育3",
            teacher="刘贵博",
            classroom="北操场",
            weekday=1,
            weeks=Course.week(1, 16),
            indexes=[5, 6],
        ),
        Course(
            name="马克思主义基本原理",
            teacher="王一涵",
            classroom="北3306",
            weekday=1,
            weeks=Course.week(1, 10),
            indexes=[7, 8],
        ),
        Course(
            name="马克思主义基本原理",
            teacher="王一涵",
            classroom="北3306",
            weekday=2,
            weeks=Course.week(1, 10),
            indexes=[5, 6],
        ),
        Course(
            name="大学物理II",
            teacher="田原野",
            classroom="北3306",
            weekday=2,
            weeks=Course.week(1, 10),
            indexes=[1, 2],
        ),
        Course(
            name="大学物理II",
            teacher="田原野",
            classroom="北3306",
            weekday=5,
            weeks=Course.week(1, 9),
            indexes=[5, 6],
        ),
        Course(
            name="离散数学",
            teacher="刘太辉",
            classroom="北3301",
            weekday=2,
            weeks=Course.week(1, 16),
            indexes=[7, 8],
        ),
        Course(
            name="离散数学",
            teacher="刘太辉",
            classroom="北3305",
            weekday=4,
            weeks=Course.week(1, 15),
            indexes=[5, 6],
        ),
        Course(
            name="数据结构I",
            teacher="薛京丽",
            classroom="北3601",
            weekday=3,
            weeks=Course.week(1, 13),
            indexes=[1, 2],
        ),
        Course(
            name="数据结构I",
            teacher="薛京丽",
            classroom="北3602",
            weekday=5,
            weeks=Course.week(1, 13),
            indexes=[7, 8],
        ),
        Course(
            name="大学物理实验II",
            teacher="田原野",
            classroom="北物理实验室",
            weekday=5,
            weeks=Course.week(8, 11),
            indexes=list(range(1, 5))  # 这将生成 [1, 2, 3, 4]

        ),
    ],
)


def merge_courses(courses):
    merged_courses = {}

    for course in courses:
        # 用 (课程名称, 教师, 课室, 星期几, 周数, 索引) 作为 key
        key = (course.name, course.teacher, course.classroom, course.weekday, tuple(course.weeks), tuple(course.indexes))

        # 如果 key 已经存在，合并 week 和 indexes 列表
        if key in merged_courses:
            merged_courses[key].weeks = sorted(set(merged_courses[key].weeks + course.weeks))
            merged_courses[key].indexes = sorted(set(merged_courses[key].indexes + course.indexes))
        else:
            merged_courses[key] = course


    return list(merged_courses.values())


# 合并重复课程
school.courses = merge_courses(school.courses)

# 生成ICS文件并保存为UTF-8编码
with open("Class_schedule.ics", "w", encoding="utf-8") as w:
    w.write(school.generate())
