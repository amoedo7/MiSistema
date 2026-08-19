<div align="center">

# MiSistema

**Qué sistema tenés y qué herramientas puede ejecutar, en un JSON común.**

[![CI](https://github.com/amoedo7/MiSistema/actions/workflows/ci.yml/badge.svg)](https://github.com/amoedo7/MiSistema/actions/workflows/ci.yml)

`Android / Termux` · `Windows` · `macOS` · `Linux` · `Python 3` · `HTML local`
</div>

---

## Qué detecta

MiSistema mira el entorno local y resume:

- sistema operativo y arquitectura;
- shell;
- Python;
- Node.js / npm;
- Java;
- Git;
- PowerShell;
- Docker;
- Bash / Zsh / Fish;
- gestores de paquetes comunes;
- espacio disponible;
- capacidades generales derivadas de lo encontrado.

No vuelca variables de entorno, tokens, claves ni archivos de configuración.

## Ejecutar

```bash
python misistema.py
```

Guardar reporte:

```bash
python misistema.py --output sistema.json
```

En Termux:

```bash
pkg install python
python misistema.py
```

## Dashboard local

[`viewer.html`](viewer.html) transforma `sistema.json` en un panel local con sistema, arquitectura, shell, runtimes y capacidades. El archivo no se sube a ningún servidor.

## Ejemplo

```json
{
  "schema": "desarrollamo.misistema.v1",
  "system": {"os": "Linux", "architecture": "aarch64"},
  "runtimes": {
    "python": {"available": true, "version": "3.13.5"},
    "node": {"available": true, "version": "v22.17.0"}
  },
  "capabilities": {
    "python_automation": true,
    "javascript_tooling": true
  }
}
```

MiSistema está pensado para complementar [`MiDispositivo`](https://github.com/amoedo7/MiDispositivo) y [`MiRed`](https://github.com/amoedo7/MiRed), y alimentar luego [`DiagnosticoAMO`](https://github.com/amoedo7/DiagnosticoAMO).

---

**DesarrollAMO** · herramientas que entienden el entorno antes de instalar nada.
