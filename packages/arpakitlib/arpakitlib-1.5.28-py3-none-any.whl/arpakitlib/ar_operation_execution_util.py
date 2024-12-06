# from datetime import datetime
# from typing import Any
#
# from sqlalchemy import TIMESTAMP, TEXT
# from sqlalchemy.dialects.postgresql import JSONB
# from sqlalchemy.orm import Mapped, mapped_column
#
# from arpakitlib.ar_enumeration import EasyEnumeration
# from arpakitlib.ar_sqlalchemy_model_util import SimpleDBM
#
#
# class OperationDBM(SimpleDBM):
#     __tablename__ = "operation"
#
#     class Statuses(EasyEnumeration):
#         waiting_for_execution = "waiting_for_execution"
#         executing = "executing"
#         executed_without_error = "executed_without_error"
#         executed_with_error = "executed_with_error"
#
#     class Types(EasyEnumeration):
#         healthcheck_ = "healthcheck"
#
#     status: Mapped[str] = mapped_column(
#         TEXT, index=True, insert_default=Statuses.waiting_for_execution, nullable=False
#     )
#     type: Mapped[str] = mapped_column(
#         TEXT, index=True, insert_default=Types.healthcheck_, nullable=False
#     )
#     execution_start_dt: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
#     execution_finish_dt: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
#     input_data: Mapped[dict[str, Any]] = mapped_column(
#         JSONB,
#         insert_default={},
#         server_default="{}",
#         nullable=False
#     )
#     output_data: Mapped[dict[str, Any]] = mapped_column(JSONB, insert_default={}, server_default="{}", nullable=False)
#     error_data: Mapped[dict[str, Any]] = mapped_column(JSONB, insert_default={}, server_default="{}", nullable=False)
#
#     def raise_if_executed_with_error(self):
#         if self.status == self.Statuses.executed_with_error:
#             raise Exception(
#                 f"Operation (id={self.id}, type={self.type}) executed with error, error_data={self.error_data}"
#             )
#
#     def raise_if_error_data(self):
#         if self.status == self.Statuses.executed_with_error:
#             raise Exception(
#                 f"Operation (id={self.id}, type={self.type}) has error_data, error_data={self.error_data}"
#             )
