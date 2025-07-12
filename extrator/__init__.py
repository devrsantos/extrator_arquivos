"""Pacote com funções de extração e utilidades."""

from .core import extrair_rar_partes, extrair_zip
from .utils import verifica_tem_pasta

__all__ = ["extrair_zip", "extrair_rar_partes", "verifica_tem_pasta"]
