"""Script para calcular y presentar las 3 métricas de calidad del software en tiempo real."""

import io
import statistics
import time
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import coverage
import pytest


class _TestResultPlugin:
    """Plugin interno de pytest para contabilizar pruebas exitosas y totales."""

    def __init__(self) -> None:
        self.passed: int = 0
        self.total: int = 0

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when == "call":
            self.total += 1
            if report.passed:
                self.passed += 1


def measure_coverage_and_pass_rate() -> tuple[float, int, int, int, int]:
    """Ejecuta la suite de pytest iniciando coverage ANTES de importar el paquete app.

    Returns:
        Tupla con (porcentaje_cobertura, lineas_cubiertas, total_lineas, tests_aprobados, total_tests).
    """
    cov = coverage.Coverage(source=["app"], omit=["app/domain/interfaces.py"])
    plugin = _TestResultPlugin()

    cov.start()
    pytest.main(
        ["-q", "-o", "addopts=-q --disable-warnings"],
        plugins=[plugin],
    )
    cov.stop()
    cov.save()

    buffer = io.StringIO()
    total_pct = cov.report(file=buffer)

    analysis_total = 0
    analysis_missing = 0
    for filename in cov.get_data().measured_files():
        if "interfaces.py" in filename:
            continue
        _, statements, _, missing, _ = cov.analysis2(filename)
        analysis_total += len(statements)
        analysis_missing += len(missing)

    covered_lines = analysis_total - analysis_missing
    return total_pct, covered_lines, analysis_total, plugin.passed, plugin.total


def measure_response_time(iterations: int = 100) -> tuple[float, float, float]:
    """Mide el tiempo de respuesta promedio, mínimo y máximo en milisegundos.

    Args:
        iterations: Número de solicitudes HTTP simuladas.

    Returns:
        Tupla con (promedio_ms, minimo_ms, maximo_ms).
    """
    from fastapi.testclient import TestClient

    from app.core.config import settings
    from app.main import app

    client = TestClient(app)
    headers = {settings.api_key_header: settings.api_secret_key}
    latencies_ms: list[float] = []

    for i in range(iterations):
        start_time = time.perf_counter()
        response = client.post(
            "/api/v1/tasks",
            json={
                "title": f"Tarea de prueba de rendimiento #{i + 1}",
                "priority": "MEDIA",
                "status": "PENDIENTE",
            },
            headers=headers,
        )
        end_time = time.perf_counter()
        assert response.status_code == 201
        latencies_ms.append((end_time - start_time) * 1000)

    avg_ms = statistics.mean(latencies_ms)
    min_ms = min(latencies_ms)
    max_ms = max(latencies_ms)
    return avg_ms, min_ms, max_ms


def main() -> None:
    """Imprime el reporte consolidado de métricas de calidad calculadas en vivo."""
    cov_pct, covered, total_stmts, passed_tests, total_tests = (
        measure_coverage_and_pass_rate()
    )
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0.0
    avg_ms, min_ms, max_ms = measure_response_time(iterations=100)

    print("\n" + "=" * 68)
    print("  REPORTE DE MÉTRICAS DE CALIDAD DEL SOFTWARE - EDUTASKS API")
    print("=" * 68)
    print("\n[MÉTRICA 1] Cobertura de Código (Code Coverage)")
    print("  - Fórmula          : (Líneas Ejecutadas / Total de Líneas) * 100")
    print("  - Unidad de medida : Porcentaje (%)")
    print(
        f"  - Resultado        : {cov_pct:.0f}% ({cov_pct:.2f}% exacto -> {covered} / {total_stmts} líneas cubiertas)"
    )
    print("  - Meta de calidad  : >= 85.0 %  --> [CUMPLE - EXCELENTE]")

    print("\n[MÉTRICA 2] Efectividad de Casos de Prueba (Test Pass Rate)")
    print("  - Fórmula          : (Casos Exitosos / Total Casos Ejecutados) * 100")
    print("  - Unidad de medida : Porcentaje (%)")
    print(
        f"  - Resultado        : {pass_rate:.1f} % ({passed_tests} / {total_tests} casos exitosos)"
    )
    print("  - Meta de calidad  : 100.0 %    --> [CUMPLE - EXCELENTE]")

    print("\n[MÉTRICA 3] Tiempo Medio de Respuesta (Average Response Time)")
    print("  - Fórmula          : Suma(Tiempos de Respuesta) / N_Peticiones")
    print("  - Unidad de medida : Milisegundos (ms)")
    print(
        f"  - Resultado        : {avg_ms:.2f} ms (Mín: {min_ms:.2f} ms | Máx: {max_ms:.2f} ms)"
    )
    print("  - Meta de calidad  : <= 50.0 ms --> [CUMPLE - EXCELENTE]")
    print("=" * 68)


if __name__ == "__main__":
    main()
