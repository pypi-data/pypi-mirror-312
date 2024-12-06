"""Grade Model Definition"""
from ic_parent_api_btk.base import DataModel
from ic_parent_api_btk.models.placement import Placement
from ic_parent_api_btk.models.course import Course
from ic_parent_api_btk.models.term import Term
from ic_parent_api_btk.ic_api_client import GradeResponse
from typing import Optional


class Grade(DataModel):
    """Grade Model Definition"""
    def __init__(self, grade_resp: GradeResponse):
        # self._id = grade_resp.id
        self._calendarid = grade_resp.calendarID
        self._courseid = grade_resp.courseID
        self._coursename = grade_resp.courseName
        self._courses = grade_resp.courses
        self._endyear = grade_resp.endYear
        self._hidestandardsonportal = grade_resp.hideStandardsOnPortal
        self._isresponsive = grade_resp.isResponsive
        self._personid = grade_resp.personID
        self._roomname = grade_resp.roomName
        self._rosterid = grade_resp.rosterID
        self._schoolid = grade_resp.schoolID
        self._schoolname = grade_resp.schoolName
        self._sectionid = grade_resp.sectionID
        self._sectionnumber = grade_resp.sectionNumber
        self._sectionplacements = grade_resp.sectionPlacements
        self._structureid = grade_resp.structureID
        self._teacherdisplay = grade_resp.teacherDisplay
        # self._terms = grade_resp.terms
        self._trialactive = grade_resp.trialActive
        self._trialid = grade_resp.trialID

# @property
# def id(self) -> str:
#     return self._id

@property
def calendarid(self) -> int:
    return self._calendarid

@property
def courseid(self) -> int:
    return self._courseid

@property
def coursename(self) -> str:
    return self._coursename

@property
def coursenumber(self) -> int:
    return self._coursenumber

@property
def courses(self) -> list[Course]:
    return self._courses

@property
def endyear(self) -> int:
    return self._endyear

@property
def hidestandardsonportal(self) -> bool:
    return self._hidestandardsonportal

@property
def isresponsive(self) -> bool:
    return self._isresponsive

@property
def personid(self) -> int:
    return self._personid

@property
def roomname(self) -> str:
    return self._roomname

@property
def rosterid(self) -> int:
    return self._rosterid

@property
def schoolid(self) -> int:
    return self._schoolid

@property
def schoolname(self) -> str:
    return self._schoolname

@property
def sectionid(self) -> int:
    return self._sectionid

@property
def sectionnumber(self) -> int:
    return self._sectionnumber

@property
def sectionplacements(self) -> list[Placement]:
    return self._sectionplacements

@property
def structureid(self) -> int:
    return self._structureid

@property
def teacherdisplay(self) -> str:
    return self._teacherdisplay

@property
def terms(self) -> list[Term]:
    return self._terms

@property
def trialactive(self) -> bool:
    return self._trialactive

@property
def trialid(self) -> int:
    return self._trialid