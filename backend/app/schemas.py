from typing import List, Optional, Union, Any
from pydantic import BaseModel, Field


class GoalRequest(BaseModel):
    goal: str = Field(..., min_length=1, description="Name or description of the financial goal")
    target_amount: float = Field(..., gt=0, description="Target amount in Indian Rupees (INR)")
    months: int = Field(..., gt=0, description="Target duration in months")


class GoalResponse(BaseModel):
    goal: str
    target_amount: float
    months: int
    monthly_saving_required: float
    message: str
    note: str


class GoalAdviceResponse(BaseModel):
    goal: str
    target_amount: Optional[float] = None
    months: Optional[int] = None
    monthly_saving_required: Optional[float] = None
    advice: str
    note: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User query or financial question")


class ChatSource(BaseModel):
    source: str
    page: Optional[Union[int, str]] = None
    source_type: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[ChatSource] = []


class MutualFund(BaseModel):
    scheme_name: str
    scheme_code: Optional[Union[str, int]] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    amc_name: Optional[str] = None
    min_sip: Optional[float] = None
    min_lumpsum: Optional[float] = None
    expense_ratio: Optional[float] = None
    fund_size_cr: Optional[float] = None
    fund_age_yr: Optional[Union[int, float]] = None
    fund_manager: Optional[str] = None
    risk_level: Optional[Union[int, str]] = None
    rating: Optional[Union[int, str]] = None
    returns_1yr: Optional[float] = None
    returns_3yr: Optional[float] = None
    returns_5yr: Optional[float] = None
    nav: Optional[float] = None
    nav_date: Optional[str] = None
    plan_type: Optional[str] = None
    option_type: Optional[str] = None
    isin: Optional[str] = None
    sortino: Optional[Union[float, str]] = None
    sharpe: Optional[Union[float, str]] = None
    alpha: Optional[Union[float, str]] = None
    beta: Optional[Union[float, str]] = None
    sd: Optional[Union[float, str]] = None


class MutualFundsResponse(BaseModel):
    total_returned: int
    funds: List[MutualFund]
    note: str


class HistoricalNAVPoint(BaseModel):
    date: str
    nav: float


class HistoricalNAVResponse(BaseModel):
    scheme_code: str
    scheme_name: str
    category: Optional[str] = None
    sub_category: Optional[str] = None
    data_points: int
    history: List[HistoricalNAVPoint]
    note: Optional[str] = None


class DocumentMeta(BaseModel):
    filename: str
    source_type: str
    size_bytes: Optional[int] = None
    pages_or_chunks: Optional[Union[int, str]] = None


class DocumentsResponse(BaseModel):
    total_documents: int
    documents: List[DocumentMeta]


class HealthResponse(BaseModel):
    status: str
    environment: str
    chroma_records: int
    mutual_funds_count: int
    llm_provider: str
