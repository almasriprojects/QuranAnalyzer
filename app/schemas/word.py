from pydantic import BaseModel
from typing import List


class WordRequest(BaseModel):
    word: str

    class Config:
        json_schema_extra = {
            "example": {
                "word": "مسلمين"
            }
        }


class BulkWordRequest(BaseModel):
    words: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "words": ["مسلمين", "مؤمنين", "صالحين"]
            }
        }


class WordAnalysis(BaseModel):
    الكلمة: str
    الوزن: str
    الفعل: str
    نوع_الكلمة: str = None
    العدد: str = None
    الجنس: str = None
    الزمن: str = None
    نوع_الاشتقاق: str = None
    معنى_الجذر: str = None
    الحركات: str = None
    مثال_الاستخدام: str = None

    class Config:
        json_schema_extra = {
            "example": {
                "الكلمة": "مسلمين",
                "الوزن": "مُفْعِلين",
                "الفعل": "سَلِمَ",
                "نوع_الكلمة": "اسم",
                "العدد": "جمع مذكر سالم",
                "الجنس": "مذكر",
                "الزمن": "غير منطبق",
                "نوع_الاشتقاق": "اسم فاعل",
                "معنى_الجذر": "السلامة والأمان",
                "الحركات": "مُسْلِمِين",
                "مثال_الاستخدام": "المسلمين يصلون في المسجد"
            }
        }


class BulkWordAnalysis(BaseModel):
    results: List[WordAnalysis]

    class Config:
        json_schema_extra = {
            "example": {
                "results": [
                    {
                        "الكلمة": "مسلمين",
                        "الوزن": "مُفْعِلين",
                        "الفعل": "سَلِمَ",
                        "نوع_الكلمة": "اسم",
                        "العدد": "جمع مذكر سالم",
                        "الجنس": "مذكر",
                        "الزمن": "غير منطبق",
                        "نوع_الاشتقاق": "اسم فاعل",
                        "معنى_الجذر": "السلامة والأمان",
                        "الحركات": "مُسْلِمِين",
                        "مثال_الاستخدام": "المسلمين يصلون في المسجد"
                    }
                ]
            }
        }
