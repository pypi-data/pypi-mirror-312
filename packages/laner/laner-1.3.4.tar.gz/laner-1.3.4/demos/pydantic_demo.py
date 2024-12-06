# encoding: utf-8
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lane.chang on '07/07/2024'
    comment: 对pydantic扩展包使用的实例
"""
import json
from pydantic import Field  # 目前仅对pydantic的BaseModel进行了扩展，其他的沿用pydantic
from laner.pydantic import BaseModel
from typing import Union


class Province(BaseModel):
    """ 省信息
    """
    code: str = Field('', title='省code')
    name: str = Field('', title='省名称')


class City(BaseModel):
    """ 市信息
    """
    code: str = Field('', title='市code')
    name: str = Field('', title='市名称')


class Address(BaseModel):
    """ 地址
    """
    province: Province = Field(None, title='省信息')
    city: City = Field(None, title='市信息')


class School(BaseModel):
    """ 学校信息
    """
    name: str = Field('', title='学校名')
    address: Address = Field('', title='学校地址信息')


class User(BaseModel):
    """ 用户信息
    """
    name: str = Field('', title='用户姓名')
    phone: str = Field('', title='用户手机号')
    school: School = Field(None, title='学校信息')


class Question(BaseModel):
    """ 题目信息
    """
    title_desc: str = Field('', title='题目描述')
    score_reverse: bool = Field(False, title='分数是否逆向')


class Emphasis(BaseModel):
    """ 题目维度信息
    """
    title: str = Field('', title='题目维度名称')
    answer: dict = Field({}, title='答案配置')
    questions: list[Question] = Field([], title='题目列表')

    @property
    def answer_titles(self):
        """
        :return:
        """
        return list(self.answer.keys())

    @property
    def answer_scores(self):
        """
        :return:
        """
        return list(self.answer.values())

    @property
    def answer_reverse(self):
        """ 逆向答案
        :return:
        """
        return dict(zip(self.answer_titles, sorted(self.answer_scores, reverse=True)))


class Psychology(BaseModel):
    """
    """
    classify_code: str = Field('', title='案例编号')
    depression: Emphasis = Field(None, title='抑郁')
    anxiety: Emphasis = Field(None, title='焦虑')
    psychological_resilience: Emphasis = Field(None, title='心理韧性')
    agreeableness: Emphasis = Field(None, title='宜人性')
    accountability: Emphasis = Field(None, title='责任性')
    emotionormal: Emphasis = Field(None, title='情绪稳定')

    @property
    def emphasises(self) -> list[Emphasis]:
        """
        :return:
        """
        iter_objects = []
        if self.depression and self.depression.questions:
            iter_objects.append(self.depression)

        if self.anxiety and self.anxiety.questions:
            iter_objects.append(self.anxiety)

        if self.psychological_resilience and self.psychological_resilience.questions:
            iter_objects.append(self.psychological_resilience)

        if self.agreeableness and self.agreeableness.questions:
            iter_objects.append(self.agreeableness)

        if self.accountability and self.accountability.questions:
            iter_objects.append(self.accountability)

        if self.emotionormal and self.emotionormal.questions:
            iter_objects.append(self.emotionormal)

        return iter_objects


if __name__ == '__main__':

    user_info = {
        'name': 'lane',
        'phone': '13800000000',
        'school': {
            'name': '深圳师范学校',
            'address': {
                'province': {
                    'code': '440000',
                    'name': '广东省'
                },
                'city': {
                    'code': '0755',
                    'name': '深圳市'
                }
            }
        }
    }

    user = User()
    # 将信息匹配到自定义的模型中
    user.sets(user_info)
    # # 展示模型信息
    print(json.dumps(user.dict(), ensure_ascii=False, indent=4))

    print(user.school.address.province.code, user.school.address.province.name)
    print(user.school.address.city.code, user.school.address.city.name)

    question_info = {
      "classify_code": "V20732",
      "depression": {
        "title": "抑郁",
        "questions": []
      },
      "anxiety": {
        "title": "焦虑",
        "questions": []
      },
      "psychological_resilience": {
        "title": "心理韧性",
        "answer": {
          "从来不": 0,
          "很少": 1,
          "有时": 2,
          "经常": 3,
          "总是这样": 4
        },
        "questions": [
          {"title_desc": "我能适应变化"},
          {"title_desc": "无论发生什么我都能应付"},
          {"title_desc": "我能看到事情幽默的一面"},
          {"title_desc": "应对压力使我感到有力量"},
          {"title_desc": "经历艰难或疾病后，我往往会很快恢复"},
          {"title_desc": "我能实现自己的目标，尽管有阻碍"},
          {"title_desc": "在压力下，我能够集中注意力并清晰思考"},
          {"title_desc": "我不会因失败而气馁"},
          {"title_desc": "我认为自己是个强有力的人"},
          {"title_desc": "我能处理不快乐的情绪"}
        ]
      },
      "agreeableness": {
        "title": "宜人性",
        "questions": [
            {"title_desc": "我是宜人性第一题"},
        ]
      },
      "accountability": {
        "title": "责任性",
        "questions": []
      },
      "emotionormal": {
        "title": "情绪稳定",
        "questions": []
      }
    }

    psychology = Psychology(assign_attrs=question_info)

    for emphasis in psychology.emphasises:
        for question in emphasis.questions:
            print(emphasis.title, emphasis.answer, question.dict())
