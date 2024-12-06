"""Base Model Definition."""
from typing import Optional
from pydantic import BaseModel, Field


class ScheduleDayResponse(BaseModel):
    """ScheduleDay Response Definition."""
    class Config:
        exclude = ['_model', '_hashCode']
    id: str = Field(alias='_id')
    dayID: int
    calendarID: int
    structureID: int
    periodScheduleID: int
    date: str
    requiresAttendance: bool
    isSchoolDay: bool
    duration: int
    trialID: int


class EnrollmentResponse(BaseModel):
    """Enrollment Response Definition."""
    enrollmentID: int
    personID: int
    calendarID: int
    structureID: int
    districtID: int
    endYear: int
    serviceType: str
    startDate: str
    endDate: Optional[str] = None
    grade: str
    structureName: str
    calendarName: str
    schoolID: int
    schoolName: str
    showOnPortal: bool
    futureShowOnPortal: bool
    calendarStartDate: str
    calendarEndDate: str


class StudentResponse(BaseModel):
    """Student Response Definition."""
    personID: int
    guardian: bool
    firstName: str
    lastName: str
    middleName: str
    suffix: Optional[str] = None
    alias: Optional[str] = None
    studentNumber: int
    hasPortalEnrollment: bool
    enrollments: list[EnrollmentResponse]
    futureEnrollments: list[EnrollmentResponse]
    scheduleDays: Optional[list[ScheduleDayResponse]] = None


class TermResponse(BaseModel):
    """Term Response Definition."""
    class Config:
        exclude = ['_model', '_hashCode']
    id: str = Field(alias='_id')
    termID: int
    termScheduleID: int
    seq: int
    startDate: str
    endDate: str
    termName: str
    structureID: int
    isPrimary: bool
    termScheduleName: str
    calendarID: int
    scheduleStructureName: str


class PlacementResponse(BaseModel):
    """Course Placement Response Definition."""
    class Config:
        exclude = ['_model', '_hashCode']
    id: str = Field(alias='_id')
    sectionID: int
    termID: int
    termName: str
    termSeq: int
    periodID: int
    trialID: int
    periodSequence: int
    term: TermResponse
    periodScheduleID: int
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    periodName: str
    periodScheduleName: str
    teacherDisplay: Optional[str] = None
    periodScheduleSequence: int
    structureID: int
    courseID: int
    courseNumber: str
    sectionNumber: int
    courseName: str
    termScheduleID: int
    startDate: str
    endDate: str
    roomID: Optional[int] = None
    roomName: Optional[str] = None
    unitAttendance: Optional[bool] = None
    attendance: bool
    isResponsive: bool


class GradingTaskResponse(BaseModel):
    """GradingTask Response Definition."""
    id: str = Field(alias='_id')
    personID: int
    courseID: int
    courseName: str
    progressScore: Optional[str] = None
    progressPercent: Optional[float] = None
    progressPointsEarned: Optional[float] = None
    progressTotalPoints: Optional[float] = None
    termName: str
    

class CourseResponse(BaseModel):
    """Course Response Definition."""
    class Config:
        exclude = ['_model', '_hashCode']
    id: str = Field(alias='_id')
    rosterID: int
    personID: int
    structureID: int
    calendarID: int
    schoolID: int
    courseID: int
    sectionID: int
    courseName: str
    courseNumber: str
    isResponsive: bool
    sectionNumber: str
    endYear: int
    schoolName: str
    trialID: int
    trialActive: bool
    roomName: Optional[str] = None
    teacherDisplay: Optional[str] = None
    hideStandardsOnPortal: bool
    sectionPlacements: list[PlacementResponse]
    gradingTasks: list[GradingTaskResponse]


class AssignmentResponse(BaseModel):
    """Assignment Response Definition."""
    objectSectionID: int
    parentObjectSectionID: Optional[int] = None
    type: int
    personID: int
    taskID: Optional[int] = None
    groupActivityID: int
    termIDs: list[int]
    assignmentName: str
    calendarID: int
    structureID: int
    sectionID: int
    dueDate: str
    assignedDate: str
    modifiedDate: Optional[str] = None
    courseName: str
    active: bool
    scoringType: Optional[str] = None
    score: Optional[str] = None
    scorePoints: Optional[str] = None
    scorePercentage: Optional[str] = None
    totalPoints: Optional[float] = None
    comments: Optional[str] = None
    feedback: Optional[str] = None
    late: Optional[bool] = None
    missing: Optional[bool] = None
    cheated: Optional[bool] = None
    dropped: Optional[bool] = None
    incomplete: Optional[bool] = None
    turnedIn: Optional[bool] = None
    wysiwygSubmission: Optional[bool] = None
    upload: Optional[bool] = None
    driveSubmission: Optional[bool] = None
    multiplier: Optional[float] = None
    hasStudentHTML: Optional[bool] = None
    hasTeacherHTML: Optional[bool] = None
    hasQuiz: Optional[bool] = None
    hasLTI: Optional[bool] = None
    hasLTIAcceptsScores: Optional[bool] = None
    hasFile: Optional[bool] = None
    hasExternalFile: Optional[bool] = None
    hasSubmission: Optional[bool] = None
    hasDiscussion: Optional[bool] = None
    hasRubric: Optional[bool] = None
    notGraded: Optional[bool] = None
    isValidRubric: Optional[bool] = None
    isValidMark: Optional[bool] = None
    includeCampusLearning: Optional[bool] = None


class GradeResponse(BaseModel):
    """Grade Response Definition."""
    calendarID: Optional[int] = None
    courseID: Optional[int] = None
    courseName: Optional[str] = None
    courseNumber: Optional[int] = None
    courses: list[CourseResponse]
    endYear: Optional[int] = None
    hideStandardsOnPortal: Optional[bool] = None
    id: Optional[int] = None
    isResponsive: Optional[bool] = None
    personID: Optional[int] = None
    roomName: Optional[str] = None
    rosterID: Optional[int] = None
    schoolID: int
    schoolName: Optional[str] = None
    sectionID: Optional[int] = None
    sectionNumber: Optional[int] = None
    sectionPlacements: Optional[list] = None
    structureID: int
    teacherDisplay: Optional[str] = None
    # terms: Optional[list[TermResponse]] = None
    trialActive: Optional[bool] = None
    trialID: Optional[int] = None


