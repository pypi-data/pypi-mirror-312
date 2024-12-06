"""Grade Model Definition"""
from ic_parent_api.base import DataModel
from ic_parent_api.ic_api_client import GradingTaskResponse
from typing import Optional


class GradingTask(DataModel):
    """GradingTask Model Definition"""
    def __init__(self, gradingtask_resp: GradingTaskResponse):
        self._personid = gradingtask_resp.personID
        self._courseid = gradingtask_resp.courseID
        self._coursename = gradingtask_resp.courseName
        self._progressscore = gradingtask_resp.progressScore
        self._progresspercent = gradingtask_resp.progressPercent
        self._progresspointsearned = gradingtask_resp.progressPointsEarned
        self._progresstotalpoints = gradingtask_resp.progressTotalPoints
        self._termname = gradingtask_resp.termName


@property
def personid(self) -> int:
    return self._personid

@property
def courseid(self) -> int:
    return self._courseid

@property
def coursename(self) -> str:
    return self._coursename

@property
def progressscore(self) -> str:
    return self._progressscore

@property
def progresspercent(self) -> float:
    return self._progresspercent

@property
def progresspointsearned(self) -> float:
    return self._progresspointsearned

@property
def progresstotalpoints(self) -> float:
    return self._progresstotalpoints

@property
def termname(self) -> str:
    return self._termname