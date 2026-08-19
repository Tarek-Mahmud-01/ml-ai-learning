"""
Dependency injection — wires infrastructure adapters into use cases per request.
This is the "composition root". Routers depend on these providers only.
"""
from __future__ import annotations

from collections.abc import Iterator
from datetime import date

from fastapi import Depends
from sqlalchemy.orm import Session

from ..application.agent.hrm_agent import HrmAgent
from ..application.agent.tools import default_registry
from ..application.use_cases.chat_assistant import ChatAssistant
from ..application.use_cases.check_employee_month import CheckEmployeeMonth
from ..application.use_cases.import_bio_time import ImportBioTime
from ..application.use_cases.list_employees import ListEmployees
from ..application.use_cases.seed_month import SeedMonth
from ..application.use_cases.train_model import TrainModel
from ..domain.services.chat_intents import IntentResolver, RegexResolver
from ..domain.services.payroll_rules import PayrollRulesService
from ..infrastructure.config import settings
from ..infrastructure.db.session import SessionLocal
from ..infrastructure.io.biotime_reader import BioTimeSqlReader
from ..infrastructure.llm.agent_resolver import NullPlanner, OllamaAgentPlanner
from ..infrastructure.llm.ollama_agent_client import OllamaAgentClient
from ..infrastructure.llm.ollama_resolver import OllamaIntentResolver
from ..infrastructure.ml.sklearn_detector import (
    SklearnSupervisedTrainer,
    SklearnTrainer,
    load_detector,
)
from ..infrastructure.repositories.sql_repositories import (
    SqlAttendanceRepository,
    SqlAuditRepository,
    SqlConfigRepository,
    SqlConversationStore,
    SqlEmployeeRepository,
    SqlLabelRepository,
)


def get_session() -> Iterator[Session]:
    s = SessionLocal()
    try:
        yield s
    finally:
        s.close()


def employee_repo(s: Session = Depends(get_session)) -> SqlEmployeeRepository:
    return SqlEmployeeRepository(s)


def attendance_repo(s: Session = Depends(get_session)) -> SqlAttendanceRepository:
    return SqlAttendanceRepository(s)


def rules_service() -> PayrollRulesService:
    return PayrollRulesService()


def list_employees_uc(
    emp: SqlEmployeeRepository = Depends(employee_repo),
) -> ListEmployees:
    return ListEmployees(emp)


def check_month_uc(
    emp: SqlEmployeeRepository = Depends(employee_repo),
    att: SqlAttendanceRepository = Depends(attendance_repo),
    rules: PayrollRulesService = Depends(rules_service),
) -> CheckEmployeeMonth:
    detector = load_detector(settings.artifact_abspath)
    return CheckEmployeeMonth(emp, att, rules, detector)


def seed_uc(
    emp: SqlEmployeeRepository = Depends(employee_repo),
    att: SqlAttendanceRepository = Depends(attendance_repo),
    rules: PayrollRulesService = Depends(rules_service),
) -> SeedMonth:
    return SeedMonth(emp, att, rules)


def train_uc(
    att: SqlAttendanceRepository = Depends(attendance_repo),
) -> TrainModel:
    return TrainModel(att, SklearnTrainer(settings.artifact_abspath))


def import_uc(
    emp: SqlEmployeeRepository = Depends(employee_repo),
    att: SqlAttendanceRepository = Depends(attendance_repo),
    rules: PayrollRulesService = Depends(rules_service),
) -> ImportBioTime:
    return ImportBioTime(
        emp, att, rules, BioTimeSqlReader(),
        merge_seconds=settings.punch_merge_seconds,
        default_base_rate=settings.import_default_base_rate,
        default_ot_rate=settings.import_default_ot_rate,
    )


def intent_resolver() -> IntentResolver:
    """LLM resolver (local Ollama) with the regex parser as a safe fallback."""
    regex = RegexResolver()
    if settings.use_llm:
        return OllamaIntentResolver(regex, settings.ollama_url, settings.ollama_model)
    return regex


def agent_planner():
    """LLM plan-and-execute agent, or a no-op planner when the LLM is disabled."""
    if settings.use_llm:
        return OllamaAgentPlanner(settings.ollama_url, settings.ollama_model)
    return NullPlanner()


def chat_assistant_uc(
    emp: SqlEmployeeRepository = Depends(employee_repo),
    att: SqlAttendanceRepository = Depends(attendance_repo),
    rules: PayrollRulesService = Depends(rules_service),
    s: Session = Depends(get_session),
    resolver: IntentResolver = Depends(intent_resolver),
    planner=Depends(agent_planner),
) -> ChatAssistant:
    return ChatAssistant(
        employees=emp,
        attendance=att,
        labels=SqlLabelRepository(s),
        audit=SqlAuditRepository(s),
        config=SqlConfigRepository(s),
        rules=rules,
        detector=load_detector(settings.artifact_abspath),
        unsup_trainer=SklearnTrainer(settings.artifact_abspath),
        sup_trainer=SklearnSupervisedTrainer(settings.artifact_abspath),
        resolver=resolver,
        planner=planner,
        importer=ImportBioTime(
            emp, att, rules, BioTimeSqlReader(),
            merge_seconds=settings.punch_merge_seconds,
            default_base_rate=settings.import_default_base_rate,
            default_ot_rate=settings.import_default_ot_rate,
        ),
        import_path=settings.import_sql_path,
        clock=date.today,
        default_merge_seconds=settings.punch_merge_seconds,
        default_base_rate=settings.import_default_base_rate,
        default_ot_rate=settings.import_default_ot_rate,
    )


def hrm_agent_uc(
    executor: ChatAssistant = Depends(chat_assistant_uc),
    s: Session = Depends(get_session),
) -> HrmAgent:
    """The tool-calling agent: LLM loop + registry + shared executor + memory."""
    llm = OllamaAgentClient(settings.ollama_url, settings.ollama_model)
    return HrmAgent(
        llm=llm,
        registry=default_registry(),
        executor=executor,
        memory=SqlConversationStore(s),
        clock=date.today,
    )
