from xerparser.model.classes.task import Task
from xerparser.model.classes.taskpred import TaskPred
from xerparser.model.classes.taskactv import TaskActv

class Tasks:
    """
    This class is a collection of tasks that controls functionalities to search, add, update and delete tasks
    """
    def __init__(self):
        self._tasks = []

    def add_task(self, params):
        task = Task(params)
        self._tasks.append(task)

    @property
    def tasks(self):
        return self.tasks

    @property
    def count(self):
        return len(self._tasks)

    @property
    def has_no_successor(self):
        objs = list(filter(lambda x: x.task_id not in [z.pred_task_id for z in TaskPred.obj_list], self._tasks))
        return objs

    def __repr__(self):
        return [x.task_code for x in self.tasks]

    def __str__(self):
        return str([str(x.task_code) for x in self.tasks])



    def find_by_id(self, id):
        obj = list(filter(lambda x: x.task_id == id, self._tasks))
        if len(obj) > 0:
            return obj[0]
        return obj

    @classmethod
    def find_by_code(cls, code):
        obj = list(filter(lambda x: x.task_code == code, cls.obj_list))
        if len(obj) > 0:
            return obj[0]
        return obj

    def duration_greater_than(self, duration):
        obj = list(filter(lambda x: x.target_drtn_hr_cnt > duration * float(self.calendar.day_hr_cnt), self._tasks))
        if obj:
            return obj
        return obj

    def float_less_than(self, Tfloat):
        objs = list(filter(lambda x: x.status_code != "TK_Complete", self._tasks))
        obj = list(filter(lambda x: x.total_float_hr_cnt < Tfloat * float(x.calendar.day_hr_cnt), objs))
        if obj:
            return obj
        return obj

    def float_greater_than(self, Tfloat):
        objs = list(filter(lambda x: x.status_code != "TK_Complete", self._tasks))
        obj = list(filter(lambda x: x.total_float_hr_cnt > Tfloat * float(x.calendar.day_hr_cnt), objs))
        if obj:
            return obj
        return obj

    def float_within_range(self, float1, float2):
        obj = None
        objs = list(filter(lambda x: x.status_code != "TK_Complete", self._tasks))
        if float1 < float2:
            obj = list(filter(lambda x: x.total_float_hr_cnt >= float1 * float(x.calendar.day_hr_cnt) and x.total_float_hr_cnt <= float2 * float(x.calendar.day_hr_cnt), objs))
            if obj:
                return obj
        return obj

    def float_within_range_exclusive(self, float1, float2):
        obj = None
        objs = list(filter(lambda x: x.status_code != "TK_Complete", self._tasks))
        if float1 < float2:
            obj = list(filter(lambda x: x.total_float_hr_cnt > float1 * float(x.calendar.day_hr_cnt) and x.total_float_hr_cnt < float2 * float(x.calendar.day_hr_cnt), objs))
            if obj:
                return obj
        return obj

    def activities_by_status(self, status):
        objs = list(filter(lambda x: x.status_code == status, self._tasks))
        return objs

    def activities_by_wbs_id(self, id):
        objs = list(filter(lambda x: x.wbs_id == id, self._tasks))
        return objs


    def activities_by_activity_code_id(self, id):
        objs = list(filter(lambda x: x.actv_code_id == id, TaskActv.obj_list))
        activities = []
        for obj in objs:
            activities.append(self.find_by_id(obj.task_id))
        return activities

    
    def no_predecessors(self):
        objs = list(filter(lambda x: x.task_id not in [z.task_id for z in TaskPred.obj_list], self._tasks))
        return objs

    def no_successors(self):
        objs = list(filter(lambda x: x.task_id not in [z.pred_task_id for z in TaskPred.obj_list], self._tasks))
        return objs

    def activities_with_hard_contratints(self):
        obj = list(filter(lambda x: x.cstr_type == "CS_MEO" or x.cstr_type == "CS_MSO", self._tasks))
        return obj

    def activities_by_type(self, type):
        obj = list(filter(lambda x: x.cstr_type == type, self._tasks))
        return obj