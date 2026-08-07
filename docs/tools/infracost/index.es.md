---
title: Infracost – Estimación de costos de nube en tiempo real para Infraestructura como Código
description: Una guía práctica de Infracost, un CLI de código abierto que estima los costos de nube a partir de Terraform, CloudFormation y CDK antes del despliegue.
created: 2026-08-07
tags:
  - infracost
  - terraform
  - finops
  - cloud-cost
  - infrastructure-as-code
  - devtools
status: draft
---

# Infracost

Infracost es una herramienta de código abierto, pensada para desarrolladores, que incorpora **estimaciones de costos de nube en tiempo real** directamente en el flujo de trabajo de infraestructura como código (IaC). Si lo usas con un proyecto de Terraform, Terragrunt, CloudFormation o AWS CDK, produce un desglose mensual detallado de costos — antes de que se implemente un solo recurso.

Esta página cubre qué es Infracost, por qué los equipos lo adoptan, cómo instalarlo y usarlo, y las características clave que lo convierten en un compañero estándar de Terraform y otras cadenas de herramientas de IaC.

---

## ¿Qué es Infracost?

Infracost es una herramienta de línea de comandos (y un panel SaaS complementario) que analiza definiciones y planes de IaC, consulta datos de precios en vivo de AWS, Azure y Google Cloud, e informa exactamente cuánto costarán los recursos por mes. Funciona tanto con **código estático** como con **archivos de plan de Terraform**, lo que significa que puede mostrar el impacto en el costo de un cambio propuesto antes de aplicarlo.

El proyecto se lanzó en 2020 y rápidamente se convirtió en la capa de estimación de costos de facto para los flujos de trabajo de Terraform. La CLI principal es gratuita y de código abierto, mientras que el panel opcional Infracost Cloud añade visibilidad a nivel de equipo, presupuestos y análisis de tendencias históricas.

```
$ infracost breakdown --path .
✔ Extracting only cost-related params from terraform
  Evaluating usage file...
  Calculating cost estimates...

Project: my-project

 Name                                               Monthly Qty  Unit                        Monthly Cost
 ---------------------------------------------------------------------------------------------------------
 aws_instance.web_server
 ├─ Instance usage (Linux/UNIX, on-demand, m5.large)  730          hours                          $100.74
 └─ root_block_device
    └─ General Purpose SSD storage (gp3)               20          GB                              $1.60
 aws_s3_bucket.assets
 └─ Storage (standard)                                 50          GB                              $1.15
 ---------------------------------------------------------------------------------------------------------
 OVERALL TOTAL                                                                                     $103.49
```

---

## ¿Por qué Infracost?

La gestión tradicional de costos de nube es *reactiva*: una factura llega a fin de mes y los equipos se afanan por descubrir qué ocurrió. Infracost promueve **shift-left FinOps** — detectando las decisiones de infraestructura costosas en el momento en que se toman:

- **Durante la revisión de código** — los comentarios en las PR muestran la diferencia de costo (`+$50.12`) para que los revisores puedan rechazar cambios que exceden el presupuesto.
- **En el editor** — las extensiones de VS Code y JetBrains muestran costos en línea mientras escribes HCL.
- **En CI/CD** — los pipelines pueden fallar por regresiones de costos, etiquetas faltantes o violaciones de presupuesto antes del despliegue.
- **En la terminal** — un comando rápido `breakdown` responde "¿cuánto cuesta este módulo?" sin necesidad de calculadora ni hoja de cálculo.

Debido a que Infracost lee los mismos artefactos de código y plan que los ingenieros ya producen, no hay instrumentación adicional ni desviación respecto a lo que realmente está desplegado.

---

## Plataformas compatibles

| Herramienta IaC   | Nubes           | Notas                                                  |
|-------------------|-----------------|--------------------------------------------------------|
| Terraform HCL     | AWS, Azure, GCP | Cobertura completa de recursos y perfiles de uso       |
| Terragrunt        | AWS, Azure, GCP | Detecta proyectos de Terragrunt automáticamente        |
| Plan de Terraform | AWS, Azure, GCP | Salida de `terraform show -json`                       |
| CloudFormation    | AWS             | Compatibilidad con plantillas y stack sets             |
| AWS CDK           | AWS             | Mediante plantillas de CloudFormation sintetizadas     |

Los recursos no compatibles se notifican como "skipped" con un mensaje y un enlace a la documentación de cobertura de recursos, por lo que la salida nunca miente silenciosamente sobre los costos.

---

## Instalación

### Homebrew (macOS / Linux)

```bash
brew install infracost
```

### Shell script (Linux / macOS)

```bash
curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh
```

### Windows (Scoop)

```powershell
scoop bucket add infracost https://github.com/infracost/infracost
scoop install infracost
```

### Docker

```bash
docker pull infracost/infracost
```

### Verificar la instalación

```bash
infracost --version
infracost --help
```

---

## Autenticación

Infracost requiere una clave de API porque consulta API de precios de nube en vivo. Regístrate gratis en [infracost.io/dashboard](https://www.infracost.io) y luego inicia sesión desde la CLI:

```bash
infracost auth login
```

Como alternativa, exporta la clave de API directamente para entornos CI:

```bash
export INFRACOST_API_KEY=my-api-key
```

Para los usuarios que no pueden enviar datos de precios a la API alojada de Infracost, la CLI admite una fuente de precios autohospedada (`INFRACOST_PRICING_API_ENDPOINT`) para entornos aislados.

---

## Uso básico

### 1. Desglose de costos de un directorio de Terraform

```bash
infracost breakdown --path . --format table
```

Esto evalúa el HCL en el directorio actual e imprime una tabla mensual de costos recurso por recurso. Los formatos compatibles incluyen `table`, `json`, `html`, `markdown`, `sarif` y `github-comment`.

### 2. Desglose de costos de un plan de Terraform

La imagen más precisa proviene del plan, ya que incluye contexto como `count`, `for_each` y lógica condicional:

```bash
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
infracost breakdown --terraform-plan-json plan.json --show-skipped
```

El flag `--show-skipped` lista los recursos que Infracost no pudo preciar para que puedas evaluar la cobertura.

### 3. Modo diff

El modo diff muestra el **cambio de costo** entre dos estados — normalmente el estado desplegado actual y el cambio propuesto:

```bash
infracost diff --path plan.json
```

Fragmento de salida de ejemplo:

```
Project: my-project

+ aws_instance.api_server
  +$75.00

- aws_instance.legacy_server
  -$58.49

Monthly cost change: +$16.51
```

### 4. Generar un comentario de pull request

Después de guardar un desglose en un archivo JSON, conviértelo a un formato de comentario de PR que el CI pueda pegar en GitHub, GitLab o Bitbucket:

```bash
infracost breakdown --path . --format json > infracost.json
infracost output --path infracost.json --format github-comment
```

---

## Características clave

### Integración con el editor en línea

La [extensión de Infracost para VS Code](https://marketplace.visualstudio.com/items?itemName=Infracost.infracost) muestra estimaciones de costos en línea junto a cada recurso en los archivos de Terraform, además de una barra lateral con el desglose completo de recursos. También presenta problemas de políticas FinOps (etiquetas faltantes, regresiones de costos) directamente en el editor. Los IDE de JetBrains son compatibles mediante una extensión similar.

### Integraciones de CI/CD

Infracost incluye integraciones nativas para GitHub Actions, GitLab CI, Bitbucket Pipelines y Azure DevOps. Un flujo de trabajo mínimo de GitHub Actions se ve así:

```yaml
name: Infracost
on: [pull_request]

jobs:
  infracost:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Infracost
        uses: infracost/actions/setup@v3
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}

      - name: Generate cost diff
        run: |
          infracost breakdown --path . --format json \
            --compare-to infracost_previous.json > infracost.json
```

El comentario de PR incluye el costo total proyectado, el diff por recurso y cualquier fallo de política.

### Perfiles de uso para estimaciones realistas

Las estimaciones predeterminadas asumen que los recursos se ejecutan 730 horas al mes a plena utilización. Muchos recursos (EC2, Lambda, RDS, Kubernetes) admiten archivos de uso específicos del cliente para que las estimaciones reflejen la realidad:

```bash
infracost breakdown --path . --usage-file usage.yml
```

Genera un archivo de uso inicial desde un proyecto con:

```bash
infracost breakdown --path . --sync-usage-file
```

Un archivo de uso se ve así:

```yaml
version: 0.1
resource_usage:
  aws_instance.web_server:
    monthly_hours: 438  # ~60% utilization
    operating_system: linux
    instances: 2
  aws_lambda_function.handler:
    monthly_requests: 1000000
    request_duration_ms: 250
```

### Política como código (OPA / Rego)

La aplicación de presupuestos y las reglas de etiquetado se expresan como políticas de OPA. Define las políticas en un directorio de políticas `.infracost` y luego ejecuta:

```bash
infracost policy --path infracost.json --policy-path policy/
```

Una política simple que bloquea cualquier cambio con un costo mensual superior a un umbral:

```rego
package infracost

deny[msg] {
  cost := input.projects[_].diff.totalMonthlyCost
  cost > 1000
  msg := sprintf("Monthly cost $%.2f exceeds $1000 budget", [cost])
}
```

Las políticas se integran con el mismo flujo de comentarios de PR, por lo que el CI puede bloquear las fusiones tanto por fallos de costo como de cumplimiento.

### Detección de ahorros

Más allá de los precios, Infracost señala oportunidades de ajuste de tamaño, recursos no utilizados y tipos de instancia mal configurados. Estos aparecen en la salida del desglose como elementos de «ahorro» con una reducción mensual estimada, y también se exponen en la salida JSON para paneles de FinOps.

### Infracost Cloud

El panel SaaS opcional añade:

- Tendencias históricas de costos por proyecto y entorno
- Presupuestos con alertas y políticas de umbral
- Analíticas a nivel de equipo y atribución del gasto
- Una biblioteca central de políticas gestionada por los equipos de plataforma

La clave de API utilizada por la CLI se autentica en la misma cuenta, por lo que los datos locales y de la nube permanecen sincronizados. Hay un nivel gratuito disponible para equipos pequeños.

### Salida multi-formato para informes

```bash
# JSON for programmatic consumption / FinOps pipelines
infracost breakdown --path . --format json > cost.json

# HTML report for stakeholders
infracost breakdown --path . --format html > report.html

# SARIF for GitHub code scanning
infracost breakdown --path . --format sarif > infracost.sarif
```

---

## Ejemplo: flujo de trabajo shift-left completo

```bash
# 1. Author Terraform
cat > main.tf <<'EOF'
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "m5.2xlarge"  # likely over-provisioned
  tags = {
    Name = "web"
  }
}
EOF

# 2. Check the cost immediately
infracost breakdown --path .

# 3. Generate the plan and compare to current state
terraform init
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
infracost diff --path plan.json
```

El desarrollador ve una partida de `+$400.00 / mes` *antes* de ejecutar `terraform apply`, y puede reducir el tipo de instancia o cambiar a una instancia spot.

---

## Archivo de configuración

Los valores predeterminados a nivel de proyecto se pueden almacenar en `infracost.yml`:

```yaml
version: 0.1
projects:
  - path: .
    name: my-project
    usage_file: usage.yml
    terraform_plan_flags:
      - -var-file=prod.tfvars
```

Esto mantiene los comandos de CI cortos y consistentes entre entornos.

---

## Limitaciones

- **Precio de lista, no contratos**: las estimaciones reflejan los precios de lista bajo demanda. Los descuentos negociados personalizados, los precios de EDP y los descuentos por uso comprometido deben contabilizarse por separado o mediante anulaciones de precios personalizadas.
- **Requiere acceso a la API de precios**: la CLI consulta la API de precios de Infracost, aunque existe un endpoint autohospedado para uso en entornos aislados.
- **La cobertura es amplia pero no universal**: los recursos no compatibles se omiten y se notifican, y las nuevas ofertas de nube pueden tardar en aparecer.
- **No es una plataforma de facturación completa**: Infracost estima el costo de la infraestructura; no reemplaza el panel de facturación del proveedor de nube para facturas reales, impuestos o créditos.

---

## Referencias

- Sitio oficial: <https://www.infracost.io>
- Repositorio de GitHub: <https://github.com/infracost/infracost>
- Documentación de cobertura de recursos: <https://www.infracost.io/docs/supported_resources/overview/>
- Extensión de VS Code: <https://marketplace.visualstudio.com/items?itemName=Infracost.infracost>
- Slack de la comunidad: enlazado desde el sitio web de Infracost